import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# --- Part 1: Join and Filter ---

# 1. Boston Employees
query_1 = """
SELECT firstName, lastName
FROM employees 
JOIN offices ON employees.officeCode = offices.officeCode
WHERE city = 'Boston';
"""
df_boston = pd.read_sql(query_1, conn)

# 2. Ghost Locations (Zero Employees) - REQUIRED NAME: df_zero_emp
query_2 = """
SELECT city, offices.officeCode 
FROM offices 
LEFT JOIN employees ON offices.officeCode = employees.officeCode
WHERE employeeNumber IS NULL;
"""
df_zero_emp = pd.read_sql(query_2, conn)


# --- Part 2: Type of Join ---

# 1. Employee Records Audit
query_3 = """
SELECT firstName, lastName, city, state 
FROM employees 
LEFT JOIN offices ON employees.officeCode = offices.officeCode
ORDER BY firstName, lastName;
"""
df_employee = pd.read_sql(query_3, conn)

# 2. Inactive Customers - REQUIRED NAME: df_contacts
query_4 = """
SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
FROM customers
LEFT JOIN orders ON customers.customerNumber = orders.customerNumber
WHERE orderNumber IS NULL
ORDER BY contactLastName;
"""
df_contacts = pd.read_sql(query_4, conn)


# --- Part 3: Built-In Function ---

# Payment Audit (Sorting by Amount)
query_5 = """
SELECT contactFirstName, contactLastName, amount, paymentDate
FROM customers
JOIN payments ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(amount AS FLOAT) DESC;
"""
df_payment = pd.read_sql(query_5, conn)


# --- Part 4: Joining and Grouping ---

# 1. High Credit Reps
query_6 = """
SELECT employeeNumber, firstName, lastName, COUNT(customerNumber) AS num_customers
FROM employees
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employeeNumber
HAVING AVG(creditLimit) > 90000
ORDER BY num_customers DESC;
"""
df_credit = pd.read_sql(query_6, conn)

# 2. Top Selling Products - REQUIRED NAME: df_product_sold
query_7 = """
SELECT productName, COUNT(orderNumber) AS numorders, SUM(quantityOrdered) AS totalunits
FROM products
JOIN orderdetails ON products.productCode = orderdetails.productCode
GROUP BY productName
ORDER BY totalunits DESC;
"""
df_product_sold = pd.read_sql(query_7, conn)


# --- Part 5: Multiple Joins ---

# 1. Product Market Reach (109 rows expected)
query_8 = """
SELECT productName, products.productCode, COUNT(DISTINCT customerNumber) AS numpurchasers
FROM products
JOIN orderdetails ON products.productCode = orderdetails.productCode
JOIN orders ON orderdetails.orderNumber = orders.orderNumber
GROUP BY products.productCode
ORDER BY numpurchasers DESC;
"""
df_total_customers = pd.read_sql(query_8, conn)

# 2. Customers per Office - REQUIRED NAME: df_customers
query_9 = """
SELECT COUNT(c.customerNumber) AS n_customers, o.officeCode, o.city
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode;
"""
df_customers = pd.read_sql(query_9, conn)


# --- Part 6: Subquery ---

# Underperforming Products Staff (15 rows expected)
# We join 5 tables and filter by products with < 20 unique customers
query_10 = """
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord ON c.customerNumber = ord.customerNumber
JOIN orderdetails od ON ord.orderNumber = od.orderNumber
WHERE od.productCode IN (
    SELECT productCode 
    FROM orderdetails 
    GROUP BY productCode 
    HAVING COUNT(DISTINCT orderNumber) < 20
);
"""
df_under_20 = pd.read_sql(query_10, conn)

# Close the connection
conn.close()