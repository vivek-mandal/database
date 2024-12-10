import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('retailer_2.db')
cursor = conn.cursor()

# Query to fetch the first order
query = '''
SELECT * FROM Orders
LIMIT 1;
'''

cursor.execute(query)
result = cursor.fetchone()

if result:
    print("First Order Data:")
    print(f"OrderID: {result[0]}")
    print(f"CustomerID: {result[1]}")
    print(f"Date: {result[2]}")
    print(f"TotalAmount: {result[3]}")
else:
    print("No data found in the Orders table.")

# Close the connection
conn.close()
