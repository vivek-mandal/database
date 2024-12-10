import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('retailer_2.db')
cursor = conn.cursor()

# Query to get Nestle Water and Pepsi sales by store
query = '''
SELECT 
    s.Location AS StoreName,
    SUM(CASE WHEN p.Name = 'Nestle Water' THEN od.Quantity ELSE 0 END) AS CokeSales,
    SUM(CASE WHEN p.Name = 'Pepsi' THEN od.Quantity ELSE 0 END) AS PepsiSales
FROM OrderDetails od
JOIN Products p ON od.UPC = p.UPC
JOIN Inventory i ON od.UPC = i.UPC
JOIN Stores s ON i.StoreID = s.StoreID
GROUP BY s.Location;
'''

# Execute the query
cursor.execute(query)
results = cursor.fetchall()

# Display the results
print("Coke and Pepsi Sales by Store")
print("------------------------------------------------------")
print(f"{'Store':<20} {'Coke Sales':<15} {'Pepsi Sales':<15}")
print("------------------------------------------------------")
for row in results:
    print(f"{row[0]:<20} {row[1]:<15} {row[2]:<15}")

conn.close()
