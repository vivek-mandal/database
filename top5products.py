import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('retailer_3.db')
cursor = conn.cursor()

# Query to find top 5 products sold at each location
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

# Execute the query
cursor.execute(query)
results = cursor.fetchall()

# Display the results
print("Top 5 Products Sold at Each Location")
print("------------------------------------------------------")
print(f"{'Store':<20} {'Product':<30} {'Total Sold':<10}")
print("------------------------------------------------------")
for row in results:
    print(f"{row[0]:<20} {row[1]:<30} {row[2]:<10}")

conn.close()
