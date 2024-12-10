import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('retailer_2.db')
cursor = conn.cursor()

# Query to get total sales (quantity and amount) for Coke and Pepsi
query = '''
SELECT 
    SUM(CASE WHEN p.Name = 'Coke' THEN od.Quantity ELSE 0 END) AS TotalCokeQuantity,
    SUM(CASE WHEN p.Name = 'Coke' THEN od.Quantity * od.Price ELSE 0 END) AS TotalCokeAmount,
    SUM(CASE WHEN p.Name = 'Pepsi' THEN od.Quantity ELSE 0 END) AS TotalPepsiQuantity,
    SUM(CASE WHEN p.Name = 'Pepsi' THEN od.Quantity * od.Price ELSE 0 END) AS TotalPepsiAmount
FROM OrderDetails od
JOIN Products p ON od.UPC = p.UPC;
'''

# Execute the query
cursor.execute(query)
result = cursor.fetchone()

# Display the results and comparison
coke_quantity, coke_amount, pepsi_quantity, pepsi_amount = result
print(f"Total Coke Sales: Quantity = {coke_quantity}, Amount = ${coke_amount:.2f}")
print(f"Total Pepsi Sales: Quantity = {pepsi_quantity}, Amount = ${pepsi_amount:.2f}")

if coke_amount > pepsi_amount:
    print("Coke has higher sales revenue than Pepsi.")
elif pepsi_amount > coke_amount:
    print("Pepsi has higher sales revenue than Coke.")
else:
    print("Coke and Pepsi have equal sales revenue.")

conn.close()
