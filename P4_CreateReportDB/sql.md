## 客户

### 1. 哪些公司的采购订单是从超过10个国家运输来的？
```SQL
SELECT c.CompanyName, COUNT(o.ShipCountry) AS ShipCountryNum
FROM Customers c
JOIN Orders o
ON c.CustomerID = o.CustomerID
GROUP BY c.CompanyName
HAVING COUNT(o.ShipCountry) > 10
ORDER BY ShipCountryNum
DESC;
```
customer_by_ship_country.csv

### 2. 采购金额最大的前10名客户公司名称和订单总金额
```SQL
SELECT c.CompanyName, SUM(d.UnitPrice * d.Quantity * (1 - d.Discount)) AS TOTAL_COST
FROM Customers c
JOIN Orders o
ON c.CustomerID = o.CustomerID
JOIN OrderDetails d
ON o.OrderId = d.OrderID
GROUP BY c.CompanyName
ORDER BY TOTAL_COST
DESC
LIMIT 10
```
top_customers.csv

### 3. 采购金额最大的前10名客户公司采购了哪些产品种类，以及每个产品种类的采购额
```SQL
WITH TopCustomers AS (
SELECT CustomerID
FROM (SELECT c.CustomerID, SUM(d.UnitPrice * d.Quantity * (1 - d.Discount)) AS TOTAL_COST
		FROM Customers c
		JOIN Orders o
		ON c.CustomerID = o.CustomerID
		JOIN OrderDetails d
		ON o.OrderId = d.OrderID
		GROUP BY c.CustomerID
		ORDER BY TOTAL_COST
		DESC
		LIMIT 10) sub)

SELECT CompanyName, CategoryName, SUM(d.UnitPrice * d.Quantity * (1 - d.Discount)) AS TotalCost
FROM Customers c
JOIN Orders o
ON c.CustomerID = o.CustomerID
JOIN OrderDetails d
ON o.OrderId = d.OrderID
JOIN Products p
ON d.ProductID = p.ProductID
JOIN Categories cs
ON p.CategoryID = cs.CategoryID
JOIN TopCustomers t1
ON c.CustomerID = t1.CustomerID
GROUP BY CompanyName, CategoryName
ORDER BY CompanyName, TotalCost 
DESC;
```
top_customer_categories.csv

### 4. 哪些客户公司负责处理订单的雇员超过15个人
```SQL
SELECT c.CompanyName, COUNT(e.EmployeeID) AS EmployeesNum
FROM Customers c
JOIN Orders o
ON c.CustomerID = o.CustomerID
JOIN Employees e
ON e.EmployeeID = o.EmployeeID
GROUP BY c.CompanyName
HAVING COUNT(e.EmployeeID) > 15
ORDER BY EmployeesNum
DESC;
```
order_employees.csv

## 供应商
### 1. 供应商提供的产品种类数量
```SQL
SELECT s.CompanyName, COUNT(p.CategoryID) AS CategoryNum
FROM Suppliers s
JOIN Products p
ON s.SupplierID = p.SupplierID
GROUP BY s.CompanyName
ORDER BY CategoryNum
DESC;
```
supplier_categories.csv

### 2. 贡献最大的10大供应商公司名及其订单总金额
```SQL
SELECT s.CompanyName, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalCost
FROM Suppliers s
JOIN Products p
ON s.SupplierID = p.SupplierID
JOIN OrderDetails od
ON od.ProductID = p.ProductID
GROUP BY s.CompanyName
ORDER BY TotalCost 
DESC
LIMIT 10;
```
top_suppliers.csv

### 3. 贡献最大的10大供应商供应了哪些产品种类，以及每个产品种类订单总金额
```SQL
WITH TopSuppliers AS (SELECT SupplierID FROM (SELECT s.SupplierID, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalCost
FROM Suppliers s
JOIN Products p
ON s.SupplierID = p.SupplierID
JOIN OrderDetails od
ON od.ProductID = p.ProductID
GROUP BY s.CompanyName
ORDER BY TotalCost 
DESC
LIMIT 10) sub)

SELECT s.CompanyName, ct.CategoryName, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalCost
FROM Suppliers s
JOIN Products p
ON s.SupplierID = p.SupplierID
JOIN OrderDetails od
ON od.ProductID = p.ProductID
JOIN Orders o
ON o.OrderId = od.OrderID
JOIN Categories ct
ON ct.CategoryID = p.CategoryID
JOIN TopSuppliers ts
ON ts.SupplierID = s.SupplierID
GROUP BY CompanyName, CategoryName
ORDER BY CompanyName, TotalCost 
DESC;
```
top_suppliers_categories.csv

### 4. 供应商每种产品种类的平均仓储量和平均预订量是多少
```SQL
SELECT s.CompanyName, c.CategoryName, AVG(UnitsInStock) AS avg_units_stock, AVG(UnitsOnOrder) AS avg_units_order
FROM Suppliers s
JOIN Products p
ON s.SupplierID = p.SupplierID
JOIN Categories c
ON p.CategoryID = c.CategoryID
GROUP BY 1, 2
ORDER BY 4 
DESC;
```
supplier_avg_units.csv

## 产品
### 1. 哪些产品需求量最大
### 2. 哪些产品的销售额在增长
### 3.
### 4.

## 雇员
### 1.
### 2.
### 3.
### 4.