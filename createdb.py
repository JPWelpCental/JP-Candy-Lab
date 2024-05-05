import sqlite3
import os

"""
Part A
+-----------------+       +-----------------+       +-----------------+
|       inv       |       |    trans_log    |       |       mem       |
+-----------------+       +-----------------+       +-----------------+
| item_id (PK)    |      /| order_id (PK)   |\      | mem_id          |
| item_name       |     / | customer_name   | \     | email (PK)      |
| desc            |-------| date            |-------| pw              |
| price           |     \ | order_desc      | /     |                 |
| avail_qty       |      \| is_member       |/      |                 |
| img_filename    |       | total_payable   |       |                 |
+-----------------+       +-----------------+       +-----------------+

"""

# Function to create tables in the database
def create_tables():
    conn = sqlite3.connect('JPCandyLab.db')
    c = conn.cursor()

    # Create inv table
    c.execute('''CREATE TABLE IF NOT EXISTS inv (
                    item_id INTEGER PRIMARY KEY,
                    item_name TEXT,
                    description TEXT,
                    price REAL,
                    avail_qty INTEGER,
                    img_filename TEXT
                )''')

    # Create mem table
    c.execute('''CREATE TABLE IF NOT EXISTS mem (
                    mem_id TEXT,
                    email TEXT PRIMARY KEY,
                    pw TEXT
                )''')

    # Create trans_log table
    c.execute('''CREATE TABLE IF NOT EXISTS trans_log (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT,
                    date TEXT,
                    order_desc TEXT,
                    is_member INTEGER,
                    total_payable REAL
                )''')

    conn.commit()
    conn.close()

# Function to read from inventory.txt and insert records into inv table
def init_inv():
    conn = sqlite3.connect('JPCandyLab.db')
    c = conn.cursor()

    with open('text+instructions/inventory.txt', 'r') as file:
        for line in file:
            item_id, item_name, description, price, avail_qty, img_filename = line.strip().split(',')
            c.execute('''INSERT INTO inv (item_id, item_name, description, price, avail_qty, img_filename)
                            VALUES (?, ?, ?, ?, ?, ?)''', (item_id, item_name, description, price, avail_qty, img_filename))

    conn.commit()
    conn.close()

# Function to read from member.txt and insert records into mem table
def init_mem():
    conn = sqlite3.connect('JPCandyLab.db')
    c = conn.cursor()

    with open('text+instructions/member.txt', 'r') as file:
        next(file)  # Skip the first line
        for line in file:
            mem_id, email, pw = line.strip().split(',')
            c.execute('''INSERT INTO mem (mem_id, email, pw)
                            VALUES (?, ?, ?)''', (mem_id, email, pw))

    conn.commit()
    conn.close()

# Function to insert records into inv table
def insert_inv(item_id, item_name, description, price, avail_qty, img_filename):
    conn = sqlite3.connect('JPCandyLab.db')
    c = conn.cursor()
    c.execute('''INSERT INTO inv (item_id, item_name, description, price, avail_qty, img_filename)
                    VALUES (?, ?, ?, ?, ?, ?)''', (item_id, item_name, description, price, avail_qty, img_filename))
    conn.commit()
    conn.close()

# Function to insert records into mem table
def insert_mem(mem_id, email, pw):
    conn = sqlite3.connect('JPCandyLab.db')
    c = conn.cursor()
    c.execute('''INSERT INTO mem (mem_id, email, pw)
                    VALUES (?, ?, ?)''', (mem_id, email, pw))
    conn.commit()
    conn.close()

# Function to insert records into trans_log table
def insert_trans_log(customer_name, date, order_desc, is_member, total_payable):
    conn = sqlite3.connect('JPCandyLab.db')
    c = conn.cursor()
    c.execute('''INSERT INTO trans_log (customer_name, date, order_desc, is_member, total_payable)
                    VALUES (?, ?, ?, ?, ?)''', (customer_name, date, order_desc, is_member, total_payable))
    conn.commit()
    conn.close()

# Function to update records in inv table
def update_inv(item_id,avail_qty):
    conn = sqlite3.connect('JPCandyLab.db')
    c = conn.cursor()
    c.execute('''UPDATE inv SET avail_qty = ?
                    WHERE item_id = ?''', (avail_qty, item_id))
    conn.commit()
    conn.close()

# Function to get all records from inv table
def get_inv():
    conn = sqlite3.connect('JPCandyLab.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM inv''')
    invs = c.fetchall()
    conn.close()
    return invs

# Function to get mem from mem table
def get_mem(email, pw):
    conn = sqlite3.connect('JPCandyLab.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM mem WHERE email = ? AND pw = ?''', (email, pw))
    mem = c.fetchone()
    conn.close()
    return mem

def main():
    if os.path.exists('JPCandyLab.db'):
        os.remove('JPCandyLab.db')
    create_tables()
    init_inv()
    init_mem()

if __name__ == '__main__':
    main()