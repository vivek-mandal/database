import sqlite3

# Connect to the database
conn = sqlite3.connect('retailer_2.db')
cursor = conn.cursor()

# Add data to the Products table
products = [
    ('123457', 'Sprite', '500ml', 'Coca-Cola', 'Beverage'),
    ('123458', 'Mountain Dew', '500ml', 'PepsiCo', 'Beverage'),
    ('123459', 'Lays Chips', '200g', 'PepsiCo', 'Snack')
]

cursor.executemany('''
INSERT INTO Products (UPC, Name, Size, Brand, Type) 
VALUES (?, ?, ?, ?, ?)
''', products)

# Add data to the Stores table
stores = [
    (3, 'Suburb', '10am - 8pm'),
    (4, 'City Center', '11am - 11pm')
]

cursor.executemany('''
INSERT INTO Stores (StoreID, Location, Hours) 
VALUES (?, ?, ?)
''', stores)

# Add data to the Customers table
customers = [
    (3, 'Alice Wonderland', 'alice@example.com', 1),
    (4, 'Bob Builder', 'bob@example.com', 0)
]

cursor.executemany('''
INSERT INTO Customers (CustomerID, Name, Email, MembershipStatus) 
VALUES (?, ?, ?, ?)
''', customers)

# Commit changes and close the connection
conn.commit()
print("Data added successfully!")
conn.close()
