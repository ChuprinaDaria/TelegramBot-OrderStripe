import sqlite3
import logging

logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT, order_details TEXT, amount REAL, status TEXT, currency TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, username TEXT, phone_number TEXT)''')
    conn.commit()
    conn.close()
    logger.info("База даних успішно ініціалізована.")

def add_order(user_id, username, order_details, amount, status, currency):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (user_id, username, order_details, amount, status, currency) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, username, order_details, amount, status, currency))
    conn.commit()
    conn.close()
    logger.info(f"Додано нове замовлення для користувача {username} (ID: {user_id}) на суму {amount} {currency} зі статусом {status}.")

def get_orders_by_user(user_id):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
    orders = c.fetchall()
    conn.close()
    logger.info(f"Отримано замовлення для користувача з ID: {user_id}. Кількість замовлень: {len(orders)}")
    return orders

def add_user(user_id, username, phone_number):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (user_id, username, phone_number) VALUES (?, ?, ?)",
              (user_id, username, phone_number))
    conn.commit()
    conn.close()
    logger.info(f"Додано/оновлено користувача: ID={user_id}, Ім'я={username}, Телефон={phone_number}")

def get_user(user_id):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        logger.info(f"Отримано користувача з ID: {user_id}. Ім'я: {user[1]}, Телефон: {user[2]}")
    else:
        logger.warning(f"Користувача з ID: {user_id} не знайдено.")
    return user