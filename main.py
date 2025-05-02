import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='6403007.Ankara',
        database='users',
        autocommit=True)
    return connection

def show_main_menu():
    print("Menu: ")
    print("Type 1 to create new customer.")
    print("Type 2 to edit customer.")
    print("Type 3 to delete customer.")
    print("Type 4 to deposit money")
    print("Type 5 to withdraw money")
    print('x. exit')

def edit_customer(customer_id):
    con = get_connection()
    customer_name = input("Customer Name: ")
    credit_limit = int(input("Credit limit: "))

    sql = "UPDATE customers SET customer_name = %s, credit_limit = %s WHERE customer_id = %s"
    data = [customer_name, credit_limit, customer_id]
    cursor = con.cursor()
    cursor.execute(sql, data)

    if cursor.rowcount == 0:
        print("No customer found with that ID.")
    else:
        print("Customer updated successfully.")

def insert_users(user_name, email_address, admin_flag, password):
    sql = """
    INSERT INTO customers
    (customer_name, email_address, credit_limit, password)
    VALUES (%s, %s, %s, %s)
    """
    data = [user_name, email_address, admin_flag, password]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    return cursor.lastrowid

def create_user():
    user_name = input("Name: ")
    email_address = input("Email Address: ")
    password = input("Password: ")
    admin_flag = 0

    user_id = insert_users(user_name, email_address, admin_flag, password)
    print("Account Created")

    balance = 0.0
    active_flag = True
    accountscol = None
    insert_account(user_id, balance, active_flag, accountscol)
    print("Bank account created.")

    return user_id

def insert_account(user_id, balance, active_flag, accountscol):
    sql = """
    INSERT INTO accounts
    (user_id, balance, active_flag, accountscol)
    VALUES (%s, %s, %s, %s)
    """
    data = [user_id, balance, active_flag, accountscol]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    return cursor.lastrowid

def create_customer():
    while True:
        email_address = input("Email Address: ")
        if get_customer_by_email(email_address) is not None:
            print("That email is unavailable. Please try another email.")
            continue
        else:
            break

    customer_name = input("Customer Name: ")

    while True:
        try:
            credit_limit = float(input("Credit Limit: "))
            if credit_limit <= 0:
                print("Credit limit must be a positive number. Please enter a valid amount.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the credit limit.")

    customer_id = add_customer(customer_name, email_address, credit_limit)
    print(f"Customer added successfully with ID: {customer_id}")
    return customer_id

def get_customer_by_email(email_address):
    sql = "SELECT * FROM customers WHERE email_address = %s"
    data = [email_address]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    return cursor.fetchone()

def add_customer(customer_name, email_address, credit_limit):
    sql = "INSERT INTO customers (customer_name, email_address, credit_limit) VALUES (%s, %s, %s)"
    data = [customer_name, email_address, credit_limit]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    return cursor.lastrowid

def add_money_to_account(customer_id, amount):
    if amount <= 0:
        print("Amount to add must be greater than 0.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    sql_check = "SELECT * FROM accounts WHERE user_id = %s"
    cursor.execute(sql_check, (customer_id,))
    account = cursor.fetchone()

    if account is None:
        print(f"No account found for customer ID {customer_id}.")
        return

    current_balance = account[2]
    new_balance = current_balance + amount

    sql_update = "UPDATE accounts SET balance = %s WHERE user_id = %s"
    cursor.execute(sql_update, (new_balance, customer_id))

    print(f"Added ${amount} to customer {customer_id}'s account. New balance: ${new_balance:.2f}")
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    sql_check = "SELECT * FROM customers WHERE customer_id = %s"
    cursor.execute(sql_check, (customer_id,))
    customer = cursor.fetchone()

    if not customer:
        print(f"No customer found with ID {customer_id}.")
        return

    confirm = input(f"Are you sure you want to delete customer '{customer[1]}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Deletion cancelled.")
        return

    sql_delete = "DELETE FROM customers WHERE customer_id = %s"
    cursor.execute(sql_delete, (customer_id,))
    conn.commit()
    conn.close()

    print(f"Customer ID {customer_id} deleted successfully.")

def login():
    print("Login")
    email_address = input("Email Address: ")
    password = input("Enter Password: ")
    user = get_customer_by_email(email_address)

    if user and user[4] == password:
        return user[0]
    else:
        print("Invalid email or password.")
        return None

def make_deposit():
    try:
        customer_id = int(input("Enter Customer ID: "))
        amount = float(input("Enter amount to deposit: "))
        add_money_to_account(customer_id, amount)
    except ValueError:
        print("Invalid input. Please enter numeric values.")

def main():
    user_id = login()
    if user_id is None:
        add_account = input("Would you like to open an account?: ")
        if add_account.lower() == 'yes':
            user_id = create_user()
        else:
            print("Goodbye.")
            return

    while True:
        show_main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            create_customer()
        elif choice == '2':
            customer_id = int(input("Enter customer ID to edit: "))
            edit_customer(customer_id)
        elif choice == '3':
            customer_id = int(input("Enter customer ID to delete: "))
            delete_customer(customer_id)
        elif choice == '4':
            make_deposit()
        elif choice.lower() == 'x':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
