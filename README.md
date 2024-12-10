# Retailer Database Queries

This project demonstrates various SQL queries executed on a SQLite database named `retailer_2.db`. These queries analyze sales data for a retailer, focusing on products, stores, and customers.

## Setup Instructions

1. Ensure you have Python 3.x installed.
2. Install the required Python libraries by running:
   ```bash
   pip install -r requirements.txt


## Database Schema
- **Products**: Stores product details (name, size, brand, type).  
- **Stores**: Stores information about retail locations.  
- **Customers**: Stores customer details.  
- **Vendors**: Stores vendor information.  
- **Orders**: Stores order details.  
- **OrderDetails**: Stores information about individual items in an order.  
- **Inventory**: Tracks inventory for each store.  

## Queries and Scripts

### 1. Coke vs Pepsi Sales (Quantity and Amount)
**Script**: `compare_coke_pepsi_amount.py`  
**Description**: Calculates the total quantity and sales amount of Coke and Pepsi across all stores and compares them.  
**SQL Query**:  
```sql
SELECT 
    SUM(CASE WHEN p.Name = 'Coke' THEN od.Quantity ELSE 0 END) AS TotalCokeQuantity,
    SUM(CASE WHEN p.Name = 'Coke' THEN od.Quantity * od.Price ELSE 0 END) AS TotalCokeAmount,
    SUM(CASE WHEN p.Name = 'Pepsi' THEN od.Quantity ELSE 0 END) AS TotalPepsiQuantity,
    SUM(CASE WHEN p.Name = 'Pepsi' THEN od.Quantity * od.Price ELSE 0 END) AS TotalPepsiAmount
FROM OrderDetails od
JOIN Products p ON od.UPC = p.UPC;
```
**Execution**:  
```bash
python compare_coke_pepsi_amount.py
```

### 2. Coke and Pepsi Sales by Store
**Script**: `coke_pepsi_sales.py`  
**Description**: Retrieves the total sales (quantity) of Coke and Pepsi for each store.  
**SQL Query**:  
```sql
SELECT 
    s.Location AS StoreName,
    SUM(CASE WHEN p.Name = 'Coke' THEN od.Quantity ELSE 0 END) AS CokeSales,
    SUM(CASE WHEN p.Name = 'Pepsi' THEN od.Quantity ELSE 0 END) AS PepsiSales
FROM OrderDetails od
JOIN Products p ON od.UPC = p.UPC
JOIN Inventory i ON od.UPC = i.UPC
JOIN Stores s ON i.StoreID = s.StoreID
GROUP BY s.Location;
```
**Execution**:  
```bash
python coke_pepsi_sales.py
```

### 3. Stores Where Coke Outsells Pepsi
**Script**: `coke_vs_pepsi.py`  
**Description**: Identifies the number of stores where Coke outsells Pepsi.  
**SQL Query**:  
```sql
SELECT COUNT(*) AS StoresWhereCokeOutsellsPepsi
FROM (
    SELECT s.Location AS StoreName,
           SUM(CASE WHEN p.Name = 'Coke' THEN od.Quantity ELSE 0 END) AS CokeSales,
           SUM(CASE WHEN p.Name = 'Pepsi' THEN od.Quantity ELSE 0 END) AS PepsiSales
    FROM OrderDetails od
    JOIN Products p ON od.UPC = p.UPC
    JOIN Inventory i ON od.UPC = i.UPC
    JOIN Stores s ON i.StoreID = s.StoreID
    GROUP BY s.Location
    HAVING CokeSales > PepsiSales
) AS Subquery;
```
**Execution**:  
```bash
python coke_vs_pepsi.py
```

### 4. Top 5 Products Sold This Year
**Script**: `top5_products_this_year.py`  
**Description**: Lists the top 5 products sold in the current year based on quantity.  
**SQL Query**:  
```sql
SELECT 
    p.Name AS ProductName,
    SUM(od.Quantity) AS TotalSold
FROM OrderDetails od
JOIN Products p ON od.UPC = p.UPC
JOIN Orders o ON od.OrderID = o.OrderID
WHERE strftime('%Y', o.Date) = strftime('%Y', 'now')
GROUP BY p.Name
ORDER BY TotalSold DESC
LIMIT 5;
```
**Execution**:  
```bash
python top5_products_this_year.py
```

### 5. Top 5 Products Sold at Each Location
**Script**: `top_products.py`  
**Description**: Lists the top 5 products sold at each store location based on quantity.  
**SQL Query**:  
```sql
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
```
**Execution**:  
```bash
python top_products.py
```

### 6. Top 5 Products Sold in Each State
**Script**: `top5_products_state.py`  
**Description**: Lists the top 5 products sold in each state based on quantity.  
**SQL Query**:  
```sql
WITH RankedProducts AS (
    SELECT 
        s.State AS StateName,
        p.Name AS ProductName,
        SUM(od.Quantity) AS TotalSold,
        ROW_NUMBER() OVER (PARTITION BY s.State ORDER BY SUM(od.Quantity) DESC) AS Rank
    FROM OrderDetails od
    JOIN Products p ON od.UPC = p.UPC
    JOIN Inventory i ON od.UPC = i.UPC
    JOIN Stores s ON i.StoreID = s.StoreID
    GROUP BY s.State, p.Name
)
SELECT StateName, ProductName, TotalSold
FROM RankedProducts
WHERE Rank <= 5
ORDER BY StateName, Rank;
```
**Execution**:  
```bash
python top5_products_state.py
```

### 7. Top 3 Types of Products Bought with Pepsi
**Script**: `top3_with_pepsi.py`  
**Description**: Identifies the top 3 types of products customers buy in addition to Pepsi.  
**SQL Query**:  
```sql
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
AND p.Name != 'Pepsi'
GROUP BY p.Type
ORDER BY PurchaseCount DESC
LIMIT 3;
```
**Execution**:  
```bash
python top3_with_pepsi.py
```

## Customizing Queries
The scripts are designed to answer specific business questions but can be modified based on your needs.

### Examples:
- To analyze sales for a different product: Replace "Pepsi" or "Coke" in the SQL query with the desired product name.
- To find top-selling products in a specific state: Add a WHERE clause filtering by state.



