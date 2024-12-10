import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('retailer_2.db')
cursor = conn.cursor()


# Populate Products table
product_names = [
    "Pepsi", "Coke", "Sprite", "Fanta", "Mountain Dew", 
    "Lays Chips", "Doritos", "Pringles", "Oreos", "KitKat",
    "Colgate Toothpaste", "Dove Soap", "Axe Deodorant", "Pantene Shampoo", "Head & Shoulders Shampoo",
    "Tide Detergent", "Surf Excel", "Harpic", "Dettol", "Lifebuoy",
    "Nestle Water", "Aquafina", "Evian", "Dasani", "Perrier",
    "Samsung TV", "Sony TV", "LG TV", "Apple MacBook", "Dell Laptop",
    "Nike Shoes", "Adidas Shoes", "Puma Shoes", "Reebok Shoes", "Asics Shoes",
    "Levi's Jeans", "Wrangler Jeans", "Zara Shirt", "H&M Jacket", "Gucci Belt"
]  # Add more product names if needed
brands = ["PepsiCo", "Coca-Cola", "Nestle", "Procter & Gamble", "Unilever", "Samsung", "Sony", "LG", "Apple", "Nike"]
product_types = ["Beverage", "Snack", "Cleaning", "Personal Care", "Electronics", "Apparel"]

for i, name in enumerate(product_names, start=1):
    upc = f"{100000000000 + i}"  # Generate unique UPC
    size = f"{random.randint(1, 5)}L" if random.choice([True, False]) else f"{random.randint(100, 500)}g"
    brand = random.choice(brands)
    prod_type = random.choice(product_types)
    cursor.execute("INSERT INTO Products (UPC, Name, Size, Brand, Type) VALUES (?, ?, ?, ?, ?)",
                   (upc, name, size, brand, prod_type))

# Populate Stores table
locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
for i, location in enumerate(locations, start=1):
    hours = "9 AM - 9 PM"
    cursor.execute("INSERT INTO Stores (StoreID, Location, Hours) VALUES (?, ?, ?)",
                   (i, location, hours))

# Populate Customers table
for i in range(1, 21):
    name = f"Customer_{i}"
    email = f"customer{i}@example.com"
    membership_status = random.choice([True, False])
    cursor.execute("INSERT INTO Customers (CustomerID, Name, Email, MembershipStatus) VALUES (?, ?, ?, ?)",
                   (i, name, email, membership_status))

# Populate Vendors table
vendor_names = [
    "PepsiCo", "Coca-Cola Company", "Nestle", "Procter & Gamble", "Unilever",
    "Samsung Electronics", "Sony Corporation", "LG Electronics", "Apple Inc.", "Nike Inc."
]
for i, name in enumerate(vendor_names, start=1):
    cursor.execute("INSERT INTO Vendors (VendorID, Name) VALUES (?, ?)", (i, name))

# Populate Orders and OrderDetails tables
start_date = datetime.now() - timedelta(days=100)
for i in range(1, 51):
    customer_id = random.randint(1, 20)
    order_date = (start_date + timedelta(days=random.randint(1, 100))).strftime('%Y-%m-%d')
    total_amount = round(random.uniform(20, 200), 2)
    cursor.execute("INSERT INTO Orders (OrderID, CustomerID, Date, TotalAmount) VALUES (?, ?, ?, ?)",
                   (i, customer_id, order_date, total_amount))
    
    # Ensure unique UPCs in OrderDetails
    upcs_used = set()
    for _ in range(random.randint(2, 5)):  # Add 2-5 products per order
        upc = f"{100000000000 + random.randint(1, len(product_names))}"
        while upc in upcs_used:  # Avoid duplicate UPCs
            upc = f"{100000000000 + random.randint(1, len(product_names))}"
        upcs_used.add(upc)
        quantity = random.randint(1, 10)
        price = round(random.uniform(1, 50), 2)
        cursor.execute("INSERT INTO OrderDetails (OrderID, UPC, Quantity, Price) VALUES (?, ?, ?, ?)",
                       (i, upc, quantity, price))

# Populate Inventory table
for i in range(1, 6):  # 5 stores
    for j in range(1, len(product_names) + 1):  # Products
        upc = f"{100000000000 + j}"
        quantity = random.randint(10, 100)
        cursor.execute("INSERT INTO Inventory (StoreID, UPC, Quantity) VALUES (?, ?, ?)",
                       (i, upc, quantity))

print("Data populated successfully.")
conn.commit()
conn.close()
