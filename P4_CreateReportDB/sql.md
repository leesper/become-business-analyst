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
customer_by_ship_country.xlsx

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
top_customers.xlsx

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
top_customer_categories.xlsx

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
order_employees.xlsx

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
supplier_categories.xlsx

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
top_suppliers.xlsx

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
top_suppliers_categories.xlsx

### 4. 供应商每种产品种类的平均预订量是多少
```SQL
SELECT s.CompanyName, c.CategoryName, AVG(UnitsOnOrder) AS avg_units_order
FROM Suppliers s
JOIN Products p
ON s.SupplierID = p.SupplierID
JOIN Categories c
ON p.CategoryID = c.CategoryID
GROUP BY 1, 2
ORDER BY 3 
DESC;
```
supplier_avg_units.xlsx

## 产品
### 1. 产品需求量排前10名的有哪些
```SQL
SELECT p.ProductName, COUNT(*) AS ProductNum
FROM Orders o
JOIN OrderDetails od
ON o.OrderId = od.OrderID
JOIN Products p
ON od.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY ProductNum 
DESC 
LIMIT 10;
```
top_products.xlsx

### 2. 哪些产品的销售额在增长
```SQL
SELECT p.ProductName, STRFTIME('%Y-%m', o.OrderDate) AS OrderMonth, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalSales
FROM Products p
JOIN OrderDetails od
ON p.ProductID = od.ProductID
JOIN Orders o
ON od.OrderID = o.OrderId
GROUP BY 1, 2
ORDER BY 1, 2
```
order_date_sum.xlsx

### 3. 需求量排前10名的产品分别有多少供应商供货
```SQL
WIth TopProducts AS (SELECT ProductID FROM (SELECT p.ProductID, COUNT(*) AS ProductNum
FROM Orders o
JOIN OrderDetails od
ON o.OrderId = od.OrderID
JOIN Products p
ON od.ProductID = p.ProductID
GROUP BY p.ProductID
ORDER BY ProductNum 
DESC 
LIMIT 10) sub)

SELECT p.ProductName, COUNT(*) AS SupplierNum
FROM Products p
JOIN Suppliers s
ON p.SupplierID = s.SupplierID
JOIN TopProducts t
ON t.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY SupplierNum;
```
top_products_supplier.xlsx

### 4. 每种类型有多少个产品
```SQL
SELECT c.CategoryName, COUNT(*) AS ProductNum
FROM Categories c
JOIN Products p
ON c.CategoryID = p.CategoryID
GROUP BY 1
ORDER BY 2 DESC;
```
category_count.xlsx

## 雇员
### 1. 业绩最好的雇员姓名以及他的销售额
```SQL
SELECT PRINTF('%s %s', e.FirstName, e.LastName) AS Name, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalSales 
FROM Employees e
JOIN Orders o
ON o.EmployeeID = e.EmployeeID
JOIN OrderDetails od
ON od.OrderID = o.OrderId
GROUP BY 1
ORDER BY 2
DESC
LIMIT 1;
```
top_employee.xlsx

### 2. 业绩最好的雇员来自哪个国家
```SQL
SELECT EmployeeID, PRINTF('%s %s', FirstName, LastName) AS Name, Country
FROM Employees
WHERE EmployeeID = (SELECT EmployeeID FROM (SELECT e.EmployeeID, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalSales 
FROM Employees e
JOIN Orders o
ON o.EmployeeID = e.EmployeeID
JOIN OrderDetails od
ON od.OrderID = o.OrderId
GROUP BY 1
ORDER BY 2
DESC
LIMIT 1) t1)
```
top_employee_country.xlsx

### 3. 业绩最好的雇员销售哪些种类产品
```SQL
SELECT c.CategoryName, COUNT(*) AS ProductNum
FROM Categories c
JOIN Products p
ON c.CategoryID = p.CategoryID
JOIN OrderDetails od
ON od.ProductID = p.ProductID
JOIN Orders o
ON o.OrderId = od.OrderID
WHERE o.EmployeeID = (SELECT EmployeeID FROM (SELECT e.EmployeeID, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalSales 
FROM Employees e
JOIN Orders o
ON o.EmployeeID = e.EmployeeID
JOIN OrderDetails od
ON od.OrderID = o.OrderId
GROUP BY 1
ORDER BY 2
DESC
LIMIT 1) t1)
GROUP BY 1
ORDER BY 2 
DESC
```
top_employee_category_count.xlsx

### 4. 业绩最好的雇员服务了哪些客户公司
```SQL
SELECT DISTINCT(c.CompanyName)
FROM Customers c
JOIN Orders o
ON c.CustomerID = o.CustomerID
WHERE o.EmployeeID = (SELECT EmployeeID FROM (SELECT e.EmployeeID, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalSales 
FROM Employees e
JOIN Orders o
ON o.EmployeeID = e.EmployeeID
JOIN OrderDetails od
ON od.OrderID = o.OrderId
GROUP BY 1
ORDER BY 2
DESC
LIMIT 1) t1)
ORDER BY 1
```
top_employee_companies.csv