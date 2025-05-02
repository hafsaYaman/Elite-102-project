import mysql.connector

def get_server_connection():
    """Connect without specifying a database, used to create database if not exists."""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='6403007.Ankara'
    )
    return connection

def get_connection():
    """Connect to the 'users' database (after it has been created)."""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='6403007.Ankara',
        database='users'
    )
    connection.autocommit = True
    return connection

def create_database():
    """Create the 'users' database if it doesn't exist."""
    con = get_server_connection()
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS users")
    con.close()

def create_table(con):
    """Create the 'customers' table inside 'users' database if it doesn't exist."""
    sql = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT NOT NULL AUTO_INCREMENT,
        customer_name VARCHAR(100),
        email_address VARCHAR(255),
        credit_limit DECIMAL(18,2),
        PRIMARY KEY (customer_id),
        UNIQUE INDEX email_address_uk (email_address ASC)
    )
    """
    cursor = con.cursor()
    cursor.execute(sql)

def add_customer(con, customer_name, email_address, credit_limit):
    sql = 'INSERT INTO customers (customer_name, email_address, credit_limit) VALUES (%s, %s, %s)'
    data = [customer_name, email_address, credit_limit]
    cursor = con.cursor()
    cursor.execute(sql, data)
    return cursor.lastrowid

def get_customer(con, customer_id):
    sql = "SELECT * FROM customers WHERE customer_id = %s"
    cursor = con.cursor()
    cursor.execute(sql, [customer_id])
    return cursor.fetchone()

def get_customer_by_email(con, email_address):
    sql = "SELECT * FROM customers WHERE email_address = %s"
    cursor = con.cursor()
    cursor.execute(sql, [email_address])
    return cursor.fetchone()

def main():
    create_database()
    con = get_connection()
    print("Connection open")
    
    create_table(con)
    print("Table created")

    # Insert customers
    id1 = add_customer(con, 'person lastname', '222@demo.com', 400)
    print(f"Inserted user {id1}")

    id2 = add_customer(con, 'hehe notaName', '768@demo.com', 12000)
    print(f"Inserted customer {id2}")

    id3 = add_customer(con, 'Business name', '999@demo.com', 2500)
    print(f"Inserted customer {id3}")

    # Fetch by ID
    customer = get_customer(con, id3)
    print("Customer by ID:", customer)

    # Fetch by email
    customer = get_customer_by_email(con, '999@demo.com')
    print("Customer by Email:", customer)

    con.close()

if __name__ == '__main__':
    main()
