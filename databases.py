import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '6403007.Ankara',
        database  = 'users',
        autocommit=True)
    return connection

def create_table(con):
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
    data = [customer_name, email_address, credit_limit]
    cursor = con.cursor()
    cursor.execute(sql, data)
    customer_id = cursor.lastrowid

    return customer_id

def get_customer(con, customer_id):
    sql = "SELECT * FROM users.customers WHERE customer_id = %s"
    data = [customer_id]
    cursor = con.cursor()
    cursor.execute(sql, data)
    result = cursor.fetchone()

    return result

def get_customer_by_email(con, email_address):
    sql = "SELECT * FROM demo.customers WHERE email_address = %s"
    data = [email_address]
    cursor = con.cursor()
    cursor.execute(sql, data)
    result = cursor.fetchone()

    return result

def main():
    con = get_connection()
    print("connection open")
    create_table(con)
    print("table created")
    customer_id = add_customer(con, 'person lastname', '222@demo.com', 400)
    print(f"Inserted user {customer_id}")
    customer_id = add_customer(con, 'hehe notaName', '768@demo.com', 12000)
    print(f"Inserted customer {customer_id}")
    
    customer_id = add_customer(con, 'Business name', '999@demo.com', 2500)
    print(f"Inserted customer {customer_id}")
    customer = get_customer(con, customer_id)
    print(customer)

    customer = get_customer_by_email(con, '789@demo.com')
    print(customer)


    con.close()


if (__name__ == '__main__'):
    main()