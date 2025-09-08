import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='',       
        user='root',         
        password='', 
        database=''  
    )

def add_branch(branch_name, location):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO Branch (BranchName, Location)
            VALUES (%s, %s)
        ''', (branch_name, location))
        conn.commit()
        return c.lastrowid

def add_customer(first_name, last_name, email, phone, city, country, birth_day, birth_month, birth_year, branch_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO Customer (FirstName, LastName, Email, Phone, City, Country, BirthDay, BirthMonth, BirthYear, BranchID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (first_name, last_name, email, phone, city, country, birth_day, birth_month, birth_year, branch_id))
        conn.commit()
        return c.lastrowid

def add_employee(first_name, last_name, position, branch_id, manager_id=None):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO Employee (FirstName, LastName, Position, BranchID, ManagerID)
            VALUES (%s, %s, %s, %s, %s)
        ''', (first_name, last_name, position, branch_id, manager_id))
        conn.commit()
        return c.lastrowid

def add_account(account_type, balance, created_date, customer_id, branch_id, password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO Account (AccountType, Balance, CreatedDate, CustomerID, BranchID, Password)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (account_type, balance, created_date, customer_id, branch_id, password))
        conn.commit()
        return c.lastrowid

def add_card(card_type, expiry_date, account_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO Card (CardType, ExpiryDate, AccountID)
            VALUES (%s, %s, %s)
        ''', (card_type, expiry_date, account_id))
        conn.commit()
        return c.lastrowid

def add_transaction(date, amount, transaction_type, account_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO Transactions (Date, Amount, TransactionType, AccountID)
            VALUES (%s, %s, %s, %s)
        ''', (date, amount, transaction_type, account_id))
        conn.commit()
        return c.lastrowid

def add_loan(loan_type, amount, interest_rate, customer_id, account_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO Loan (LoanType, Amount, InterestRate, CustomerID, AccountID)
            VALUES (%s, %s, %s, %s, %s)
        ''', (loan_type, amount, interest_rate, customer_id, account_id))
        conn.commit()
        return c.lastrowid

def update_employee(employee_id, first_name=None, last_name=None, position=None, branch_id=None, manager_id=None):
    with get_connection() as conn:
        c = conn.cursor()
        fields = []
        values = []
        if first_name is not None:
            fields.append('FirstName=%s')
            values.append(first_name)
        if last_name is not None:
            fields.append('LastName=%s')
            values.append(last_name)
        if position is not None:
            fields.append('Position=%s')
            values.append(position)
        if branch_id is not None:
            fields.append('BranchID=%s')
            values.append(branch_id)
        if manager_id is not None:
            fields.append('ManagerID=%s')
            values.append(manager_id)
        if not fields:
            return
        values.append(employee_id)
        c.execute(f"UPDATE Employee SET {', '.join(fields)} WHERE EmployeeID=%s", tuple(values))
        conn.commit()

def delete_loan(loan_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM Loan WHERE LoanID=%s', (loan_id,))
        conn.commit()

def branch_exists(branch_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM Branch WHERE BranchID = %s', (branch_id,))
        return c.fetchone() is not None

def branch_exists_by_name_and_location(branch_name, location):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM Branch WHERE BranchName = %s AND Location = %s', (branch_name, location))
        return c.fetchone() is not None

def get_branch_id_by_name_and_location(branch_name, location):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT BranchID FROM Branch WHERE BranchName = %s AND Location = %s', (branch_name, location))
        row = c.fetchone()
        return row[0] if row else None

def get_all_customers():
    with get_connection() as conn:
        c = conn.cursor(dictionary=True)
        c.execute('SELECT * FROM Customer')
        return c.fetchall()

def get_all_accounts():
    with get_connection() as conn:
        c = conn.cursor(dictionary=True)
        c.execute('SELECT * FROM Account')
        return c.fetchall()

def get_all_employees():
    with get_connection() as conn:
        c = conn.cursor(dictionary=True)
        c.execute('SELECT * FROM Employee')
        return c.fetchall()

def get_card_by_account_id(account_id):
    with get_connection() as conn:
        c = conn.cursor(dictionary=True)
        c.execute('SELECT * FROM Card WHERE AccountID = %s', (account_id,))
        return c.fetchone()

def get_branch_by_id(branch_id):
    with get_connection() as conn:
        c = conn.cursor(dictionary=True)
        c.execute('SELECT * FROM Branch WHERE BranchID = %s', (branch_id,))
        return c.fetchone()

def get_transactions_by_account_id(account_id):
    with get_connection() as conn:
        c = conn.cursor(dictionary=True)
        c.execute('SELECT * FROM Transactions WHERE AccountID = %s', (account_id,))
        return c.fetchall()

def get_loans_by_account_id(account_id):
    with get_connection() as conn:
        c = conn.cursor(dictionary=True)
        c.execute('SELECT * FROM Loan WHERE AccountID = %s', (account_id,))
        return c.fetchall()

def load_employees():
    with get_connection() as conn:
        c = conn.cursor(dictionary=True)
        c.execute('SELECT * FROM Employee')
        employees = []
        for row in c.fetchall():
            employee = employee(row['FirstName'], row['LastName'], row['Position'], row['BranchID'])
            employees.append(employee)
        return employees 