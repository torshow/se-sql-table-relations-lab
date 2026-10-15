# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# Boston employees: join employees to offices, keep only Boston
df_boston = pd.read_sql('SELECT firstName, jobTitle FROM employees JOIN offices ON employees.officeCode = offices.officeCode WHERE city = \'Boston\' ORDER BY firstName', conn)

# Offices with zero employees
# then HAVING keeps only the ones with a count of 0
df_zero_emp = pd.read_sql('SELECT offices.officeCode, offices.city FROM offices LEFT JOIN employees ON offices.officeCode = employees.officeCode GROUP BY offices.officeCode HAVING COUNT(employees.employeeNumber) = 0', conn)

# All employees with their office city/state
df_employee = pd.read_sql('SELECT firstName, lastName, city, state FROM employees LEFT JOIN offices ON employees.officeCode = offices.officeCode ORDER BY firstName, lastName', conn)

# Customers who have never placed an order
df_contacts = pd.read_sql('SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber FROM customers WHERE customerNumber NOT IN (SELECT customerNumber FROM orders) ORDER BY contactLastName', conn)

# Payments sorted by amount
df_payment = pd.read_sql('SELECT contactFirstName, contactLastName, amount, paymentDate FROM customers JOIN payments ON customers.customerNumber = payments.customerNumber ORDER BY CAST(amount AS REAL) DESC', conn)


# Employees whose customers average over 90k credit limit 
df_credit = pd.read_sql('SELECT employeeNumber, firstName, lastName, COUNT(customerNumber) AS n_customers FROM employees JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber GROUP BY employeeNumber HAVING AVG(creditLimit) > 90000 ORDER BY n_customers DESC', conn)

# Top-selling products: number of orders and total units per product
df_product_sold = pd.read_sql('SELECT productName, COUNT(orderNumber) AS numorders, SUM(quantityOrdered) AS totalunits FROM products JOIN orderdetails ON products.productCode = orderdetails.productCode GROUP BY products.productCode ORDER BY totalunits DESC', conn)

# Number of different customers who bought each product
df_total_customers = pd.read_sql('SELECT productName, products.productCode, COUNT(DISTINCT orders.customerNumber) AS numpurchasers FROM products JOIN orderdetails ON products.productCode = orderdetails.productCode JOIN orders ON orderdetails.orderNumber = orders.orderNumber GROUP BY products.productCode ORDER BY numpurchasers DESC', conn)

# Number of customers per office 
df_customers = pd.read_sql('SELECT COUNT(customers.customerNumber) AS n_customers, offices.officeCode, offices.city FROM customers JOIN employees ON customers.salesRepEmployeeNumber = employees.employeeNumber JOIN offices ON employees.officeCode = offices.officeCode GROUP BY offices.officeCode', conn)

# Employees who sold products ordered by fewer than 20 customers.
df_under_20 = pd.read_sql('SELECT DISTINCT employees.employeeNumber, employees.firstName, employees.lastName, offices.city, offices.officeCode FROM employees JOIN offices ON employees.officeCode = offices.officeCode JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber JOIN orders ON customers.customerNumber = orders.customerNumber JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber WHERE orderdetails.productCode IN (SELECT orderdetails.productCode FROM orderdetails JOIN orders ON orderdetails.orderNumber = orders.orderNumber GROUP BY orderdetails.productCode HAVING COUNT(DISTINCT orders.customerNumber) < 20) ORDER BY employees.lastName', conn)
conn.close()