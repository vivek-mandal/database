import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('retailer_2.db')
cursor = conn.cursor()

# Query to find the top 5 products sold this year
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
LIMIT 5;
'''

# Execute the query
cursor.execute(query)
results = cursor.fetchall()

# Display the results
print("Top 5 Products Sold This Year")
print("------------------------------------------------------")
print(f"{'Product':<30} {'Total Sold':<10}")
print("------------------------------------------------------")
for row in results:
    print(f"{row[0]:<30} {row[1]:<10}")

conn.close()
