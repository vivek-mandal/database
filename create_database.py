import sqlite3

# Create a connection to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('retailer_2.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE Products (
    UPC TEXT PRIMARY KEY,
    Name TEXT NOT NULL,
    Size TEXT NOT NULL,
    Brand TEXT NOT NULL,
    Type TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE Stores (
    StoreID INTEGER PRIMARY KEY,
    Location TEXT NOT NULL,
    Hours TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE Customers (
    CustomerID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Email TEXT,
    MembershipStatus BOOLEAN
);
''')

cursor.execute('''
CREATE TABLE Vendors (
    VendorID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE Orders (
    OrderID INTEGER PRIMARY KEY,
    CustomerID INTEGER NOT NULL,
    Date TEXT NOT NULL,
    TotalAmount REAL NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
''')

cursor.execute('''
CREATE TABLE OrderDetails (
    OrderID INTEGER NOT NULL,
    UPC TEXT NOT NULL,
    Quantity INTEGER NOT NULL,
    Price REAL NOT NULL,
    PRIMARY KEY (OrderID, UPC),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (UPC) REFERENCES Products(UPC)
);
''')

cursor.execute('''
CREATE TABLE Inventory (
    StoreID INTEGER NOT NULL,
    UPC TEXT NOT NULL,
    Quantity INTEGER NOT NULL,
    PRIMARY KEY (StoreID, UPC),
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID),
    FOREIGN KEY (UPC) REFERENCES Products(UPC)
);
''')

print("Database and tables created successfully.")
conn.commit()
conn.close()
