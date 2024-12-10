from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = 'Database'  # Needed for session management

def create_user(username, password):
    """Insert a new user into the Users table."""
    conn = sqlite3.connect('retailer_2.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise ValueError("Username already exists.")
    finally:
        conn.close()

def authenticate_user(username, password):
    """Verify if the username and password are correct."""
    conn = sqlite3.connect('retailer_2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    # Check if password matches
    if result and result[0] == password:
        return True
    return False

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            if not authenticate_user(username, password):  # Check if user exists
                create_user(username, password)  # Create new user if they don't exist
                flash("New user created! Welcome.", "success")
            session["username"] = username  # Save username in session
            return redirect(url_for("sales"))  # Redirect to the sales page
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("login.html")  # Render login page

def get_tables_and_data():
    conn = sqlite3.connect('retailer_3.db')
    cursor = conn.cursor()

    # Query to fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Fetch data for each table
    tables_data = {}
    for table_name in tables:
        table_name = table_name[0]  # Extract the table name
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()

        # Fetch column names
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]

        tables_data[table_name] = {"columns": columns, "data": data}

    conn.close()
    return tables_data

# Function to get total Coke and Pepsi sales
def get_total_coke_and_pepsi_sales():
    conn = sqlite3.connect('retailer_3.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        SUM(CASE WHEN p.Name = 'Nestle Water' THEN od.Quantity ELSE 0 END) AS TotalCokeQuantity,
        SUM(CASE WHEN p.Name = 'Nestle Water' THEN od.Quantity * od.Price ELSE 0 END) AS TotalCokeAmount,
        SUM(CASE WHEN p.Name = 'Pepsi' THEN od.Quantity ELSE 0 END) AS TotalPepsiQuantity,
        SUM(CASE WHEN p.Name = 'Pepsi' THEN od.Quantity * od.Price ELSE 0 END) AS TotalPepsiAmount
    FROM OrderDetails od
    JOIN Products p ON od.UPC = p.UPC;
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    return {
        "TotalCokeQuantity": result[0],
        "TotalCokeAmount": result[1],
        "TotalPepsiQuantity": result[2],
        "TotalPepsiAmount": result[3],
        "Comparison": (
            "Nestle Water has higher sales revenue than Pepsi."
            if result[1] > result[3]
            else "Pepsi has higher sales revenue than Nestle Water."
            if result[3] > result[1]
            else "Nestle Water and Pepsi have equal sales revenue."
        ),
    }

# Function to get Coke and Pepsi sales by store
def get_coke_and_pepsi_sales_by_store():
    conn = sqlite3.connect('retailer_3.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        s.Location AS StoreName,
        SUM(CASE WHEN p.Name = 'Coke' THEN od.Quantity ELSE 0 END) AS CokeSales,
        SUM(CASE WHEN p.Name = 'Pepsi' THEN od.Quantity ELSE 0 END) AS PepsiSales
    FROM OrderDetails od
    JOIN Products p ON od.UPC = p.UPC
    JOIN Inventory i ON od.UPC = i.UPC
    JOIN Stores s ON i.StoreID = s.StoreID
    GROUP BY s.Location;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [{"StoreName": row[0], "CokeSales": row[1], "PepsiSales": row[2]} for row in results]

# Function to get top 5 products by location
def get_top_products_by_location():
    conn = sqlite3.connect('retailer_3.db')
    cursor = conn.cursor()

    query = '''
    WITH RankedProducts AS (
        SELECT 
            s.Location AS StoreName,
            p.Name AS ProductName,
            SUM(od.Quantity) AS TotalSold,
            ROW_NUMBER() OVER (PARTITION BY s.Location ORDER BY SUM(od.Quantity) DESC) AS Rank
        FROM OrderDetails od
        JOIN Products p ON od.UPC = p.UPC
        JOIN Inventory i ON od.UPC = i.UPC
        JOIN Stores s ON i.StoreID = s.StoreID
        GROUP BY s.Location, p.Name
    )
    SELECT StoreName, ProductName, TotalSold
    FROM RankedProducts
    WHERE Rank <= 5
    ORDER BY StoreName, Rank;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    # Format results as a dictionary by store
    top_products = {}
    for row in results:
        store = row[0]
        if store not in top_products:
            top_products[store] = []
        top_products[store].append({"ProductName": row[1], "TotalSold": row[2]})

    return top_products

# Function to get top 5 products sold this year
def get_top_products_this_year():
    conn = sqlite3.connect('retailer_3.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        p.Name AS ProductName,
        SUM(od.Quantity) AS TotalSold
    FROM OrderDetails od
    JOIN Products p ON od.UPC = p.UPC
    JOIN Orders o ON od.OrderID = o.OrderID
    WHERE strftime('%Y', o.Date) = strftime('%Y', 'now') -- Filter for current year
    GROUP BY p.Name
    ORDER BY TotalSold DESC
    LIMIT 10;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return [{"ProductName": row[0], "TotalSold": row[1]} for row in results]
def get_top_products_with_pepsi():
    conn = sqlite3.connect('retailer_3.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        p.Type AS ProductType,
        COUNT(*) AS PurchaseCount
    FROM OrderDetails od
    JOIN Products p ON od.UPC = p.UPC
    WHERE od.OrderID IN (
        SELECT DISTINCT od2.OrderID
        FROM OrderDetails od2
        JOIN Products p2 ON od2.UPC = p2.UPC
        WHERE p2.Name = 'Pepsi'
    )
    AND p.Name != 'Pepsi' -- Exclude Pepsi itself
    GROUP BY p.Type
    ORDER BY PurchaseCount DESC
    LIMIT 3;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return [{"ProductType": row[0], "PurchaseCount": row[1]} for row in results]

@app.route("/logout")
def logout():
    session.pop("username", None)  # Clear session
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/database")
def database():
    tables_data = get_tables_and_data()
    return render_template("tables.html", tables=tables_data)

@app.route("/sales")
def sales():
    # Fetch all reports
    total_sales = get_total_coke_and_pepsi_sales()
    sales_by_store = get_coke_and_pepsi_sales_by_store()
    top_products_this_year = get_top_products_this_year()
    top_products = get_top_products_by_location()
    top_products_with_pepsi = get_top_products_with_pepsi()


    return render_template(
        "sales.html",
        total_sales=total_sales,
        sales_by_store=sales_by_store,
        top_products_this_year=top_products_this_year,
        top_products=top_products,
        top_products_with_pepsi=top_products_with_pepsi

    )

if __name__ == "__main__":
    app.run(debug=True)
