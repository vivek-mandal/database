import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('retailer_2.db')
cursor = conn.cursor()

# Query to find top 3 types of products bought in addition to Pepsi
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

# Execute the query
cursor.execute(query)
results = cursor.fetchall()

# Display the results
print("Top 3 Types of Products Bought with Pepsi")
print("------------------------------------------------------")
print(f"{'Product Type':<20} {'Purchase Count':<10}")
print("------------------------------------------------------")
for row in results:
    print(f"{row[0]:<20} {row[1]:<10}")

conn.close()
