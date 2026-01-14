import sqlite3

def connect_db():
    return sqlite3.connect("payments.db", check_same_thread=False)

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        username TEXT,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        contact TEXT,
        amount REAL,
        paid TEXT,
        payment_date TEXT
    )
    """)

    cur.execute("SELECT * FROM admin")
    if not cur.fetchall():
        cur.execute("INSERT INTO admin VALUES (?, ?)", ("admin", "admin123"))

    conn.commit()
    conn.close()

def login_admin(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM admin WHERE username=? AND password=?",
        (username, password)
    )
    data = cur.fetchone()
    conn.close()
    return data

def add_member(name, contact, amount, paid, payment_date):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO members (name, contact, amount, paid, payment_date)
        VALUES (?, ?, ?, ?, ?)
    """, (name, contact, amount, paid, payment_date))
    conn.commit()
    conn.close()

def get_members():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members")
    data = cur.fetchall()
    conn.close()
    return data

def update_payment(member_id, paid):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE members SET paid=? WHERE id=?",
        (paid, member_id)
    )
    conn.commit()
    conn.close()

# ✏ Edit member details
def update_member(member_id, name, contact, amount):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE members
        SET name=?, contact=?, amount=?
        WHERE id=?
    """, (name, contact, amount, member_id))
    conn.commit()
    conn.close()

# 🗑 Delete member
def delete_member(member_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM members WHERE id=?", (member_id,))
    conn.commit()
    conn.close()
