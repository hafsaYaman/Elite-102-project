import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '6403007.Ankara',
        database  = 'users',
        autocommit=True)
    return connection

def create__table(con):
    sql = "CREATE DATABASE IF NOT EXISTS users"
    cursor = con.cursor()
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS users.customers (
        customer_id INT NOT NULL AUTO_INCREMENT,
        customer_name VARCHAR(100),
        email_address VARCHAR(255),
        credit_limit DECIMAL(18,2),
    PRIMARY KEY (customer_id),
    UNIQUE INDEX `email_address_uk` (email_address ASC) VISIBLE)
    """
    cursor.execute(sql)

def add_customer(con, customer_name, email_address, credit_limit):
    sql = 'INSERT INTO users.customers (customer_name, email_address, credit_limit) VALUES (%s, %s, %s)'
    data = [cqustomer_name, email_address, credit_limit]
    cursor = con.cursor()
    cursor.execute(sql, data)
    customer_id = cursor.lastrowid

    return customer_id

def get_customer(con, customer_id):
    sql = "SELECT * FROM users.customers WHERE customer_id = %s"
