import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('retailer_2.db')
cursor = conn.cursor()

# Clear all existing data while preserving schema
tables = ["OrderDetails", "Orders", "Inventory", "Products", "Stores", "Customers", "Vendors"]
for table in tables:
    cursor.execute(f"DELETE FROM {table}")

print("Existing data deleted successfully.")

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
]
brands = ["PepsiCo", "Coca-Cola", "Nestle", "Procter & Gamble", "Unilever", "Samsung", "Sony", "LG", "Apple", "Nike"]
product_types = ["Beverage", "Snack", "Cleaning", "Personal Care", "Electronics", "Apparel"]

products = []
for i, name in enumerate(product_names, start=1):
    upc = f"{100000000000 + i}"  # Generate unique UPC
    size = f"{random.randint(1, 5)}L" if random.choice([True, False]) else f"{random.randint(100, 500)}g"
    brand = random.choice(brands)
    prod_type = random.choice(product_types)
    products.append((upc, name, size, brand, prod_type))

cursor.executemany("INSERT INTO Products (UPC, Name, Size, Brand, Type) VALUES (?, ?, ?, ?, ?)", products)

# Populate Stores table
locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
stores = []
for i, location in enumerate(locations, start=1):
    hours = "9 AM - 9 PM"
    stores.append((i, location, hours))

cursor.executemany("INSERT INTO Stores (StoreID, Location, Hours) VALUES (?, ?, ?)", stores)

# Populate Customers table
customers = []
for i in range(1, 21):
    name = f"Customer_{i}"
    email = f"customer{i}@example.com"
    membership_status = random.choice([True, False])
    customers.append((i, name, email, membership_status))

cursor.executemany("INSERT INTO Customers (CustomerID, Name, Email, MembershipStatus) VALUES (?, ?, ?, ?)", customers)

# Populate Vendors table
vendor_names = [
    "PepsiCo", "Coca-Cola Company", "Nestle", "Procter & Gamble", "Unilever",
    "Samsung Electronics", "Sony Corporation", "LG Electronics", "Apple Inc.", "Nike Inc."
]
vendors = [(i, name) for i, name in enumerate(vendor_names, start=1)]
cursor.executemany("INSERT INTO Vendors (VendorID, Name) VALUES (?, ?)", vendors)

# Populate Inventory table
inventory = []
for store_id, location in enumerate(locations, start=1):
    available_products = random.sample(products, k=random.randint(15, 25))  # Each store stocks 15-25 products
    for product in available_products:
        upc = product[0]
        quantity = random.randint(50, 300)
        inventory.append((store_id, upc, quantity))

cursor.executemany("INSERT INTO Inventory (StoreID, UPC, Quantity) VALUES (?, ?, ?)", inventory)

# Populate Orders and OrderDetails tables
start_date = datetime.now() - timedelta(days=100)
orders = []
order_details = []

for i in range(1, 101):  # 100 orders
    customer_id = random.randint(1, 20)
    store_id = random.randint(1, len(locations))  # Assign order to a random store
    order_date = (start_date + timedelta(days=random.randint(1, 100))).strftime('%Y-%m-%d')
    total_amount = 0
    orders.append((i, customer_id, order_date, total_amount))

    # Select products from the store's inventory
    store_inventory = [inv for inv in inventory if inv[0] == store_id]
    selected_products = random.sample(store_inventory, k=random.randint(2, 5))
    for product in selected_products:
        upc = product[1]
        quantity = random.randint(1, 10) * random.randint(1, store_id)  # Add variability by store
        price = round(random.uniform(10, 100), 2)
        total_amount += quantity * price
        order_details.append((i, upc, quantity, price))

    # Update the total amount for the order
    orders[-1] = (i, customer_id, order_date, round(total_amount, 2))

cursor.executemany("INSERT INTO Orders (OrderID, CustomerID, Date, TotalAmount) VALUES (?, ?, ?, ?)", orders)
cursor.executemany("INSERT INTO OrderDetails (OrderID, UPC, Quantity, Price) VALUES (?, ?, ?, ?)", order_details)

print("Data repopulated successfully with realistic variability.")
conn.commit()
conn.close()
