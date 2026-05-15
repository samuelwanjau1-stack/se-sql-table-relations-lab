import sqlite3
import pandas as pd

# 1. Connect to the database
conn = sqlite3.connect('data.sqlite')

print("--- Part 1: Join and Filter ---")
# Boston Employees - Assigned to df_boston
query_1 = """
SELECT firstName, lastName, jobTitle 
FROM employees 
JOIN offices ON employees.officeCode = offices.officeCode
WHERE city = 'Boston';
"""
df_boston = pd.read_sql(query_1, conn)
print(df_boston)

# Ghost Locations
query_2 = """
SELECT city, offices.officeCode 
FROM offices 
LEFT JOIN employees ON offices.officeCode = employees.officeCode
WHERE employeeNumber IS NULL;
"""
df_ghost = pd.read_sql(query_2, conn)
print("\nGhost Offices:", df_ghost)


print("\n--- Part 2: Type of Join ---")
# Employee Records Audit - Assigned to df_employee
query_3 = """
SELECT firstName, lastName, city, state 
FROM employees 
LEFT JOIN offices ON employees.officeCode = offices.officeCode
ORDER BY firstName, lastName;
"""
df_employee = pd.read_sql(query_3, conn)
print(df_employee)

# Customers with No Orders
query_4 = """
SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
FROM customers
LEFT JOIN orders ON customers.customerNumber = orders.customerNumber
WHERE orderNumber IS NULL
ORDER BY contactLastName;
"""
df_inactive = pd.read_sql(query_4, conn)
print("\nInactive Customers:", df_inactive)


print("\n--- Part 3: Built-In Function (Sorting) ---")
# Payment Audit - Assigned to df_payment
query_5 = """
SELECT contactFirstName, contactLastName, amount, paymentDate
FROM customers
JOIN payments ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(amount AS FLOAT) DESC;
"""
df_payment = pd.read_sql(query_5, conn)
print(df_payment)


print("\n--- Part 4: Joining and Grouping ---")
# High Credit Reps - Assigned to df_credit
query_6 = """
SELECT employeeNumber, firstName, lastName, COUNT(customerNumber) AS num_customers
FROM employees
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employeeNumber
HAVING AVG(creditLimit) > 90000
ORDER BY num_customers DESC;
"""
df_credit = pd.read_sql(query_6, conn)
print(df_credit)

# Top Selling Products
query_7 = """
SELECT productName, COUNT(orderNumber) AS numorders, SUM(quantityOrdered) AS totalunits
FROM products
JOIN orderdetails ON products.productCode = orderdetails.productCode
GROUP BY productName
ORDER BY totalunits DESC;
"""
df_top_selling = pd.read_sql(query_7, conn)
print("\nTop Selling Products:", df_top_selling)


print("\n--- Part 5: Multiple Joins ---")
# Product Market Reach
query_8 = """
SELECT productName, products.productCode, COUNT(DISTINCT customerNumber) AS numpurchasers
FROM products
JOIN orderdetails ON products.productCode = orderdetails.productCode
JOIN orders ON orderdetails.orderNumber = orders.orderNumber
GROUP BY products.productCode
ORDER BY numpurchasers DESC;
"""
df_reach = pd.read_sql(query_8, conn)
print(df_reach)

# Customers per Office - Assigned to df_total_customers
query_9 = """
SELECT COUNT(c.customerNumber) AS n_customers, o.officeCode, o.city
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode;
"""
df_total_customers = pd.read_sql(query_9, conn)
print("\nVolume per Office:", df_total_customers)


print("\n--- Part 6: Subquery ---")
# Underperforming Products Staff - Assigned to df_under_20
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
print(df_under_20)

# Close the connection
conn.close()