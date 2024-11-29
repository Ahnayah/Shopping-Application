import sqlite3
import os

class DatabaseHandler:
    def __init__(self, db_path="__pycache__/app_database.db"):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                image_path TEXT NOT NULL,
                rating REAL DEFAULT 0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                staff_username TEXT NOT NULL,
                reply TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (message_id) REFERENCES messages (id)
            )
        ''')
        self.connection.commit()

    def ensure_rating_column(self):
        self.cursor.execute("PRAGMA table_info(products)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if 'rating' not in columns:
            self.cursor.execute('''
                ALTER TABLE products ADD COLUMN rating REAL DEFAULT 0
            ''')
            self.connection.commit()

    def add_user(self, username, password):
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (username, password))
            self.connection.commit()
        except sqlite3.IntegrityError:
            return False
        return True
    
    def get_user_id(self, username):
        self.cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def validate_user(self, username, password):
        try:
            self.cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = self.cursor.fetchone()
            if result and result[0] == password:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"Error validating user: {e}")
            return False
    
    def get_total_orders(self):
        self.cursor.execute('''
            SELECT COUNT(*) FROM orders
        ''')
        return self.cursor.fetchone()[0]

    def get_products(self):
        self.cursor.execute('''
            SELECT id, name, price, quantity, image_path, rating FROM products
            ORDER BY rating DESC
        ''')
        return self.cursor.fetchall()

    def add_product(self, name, price, quantity, image_path):
        self.cursor.execute('''
            INSERT INTO products (name, price, quantity, image_path)
            VALUES (?, ?, ?, ?)
        ''', (name, price, quantity, image_path))
        self.connection.commit()

    def update_product_quantity(self, product_name, quantity):
        self.cursor.execute('''
            UPDATE products
            SET quantity = ?
            WHERE name = ?
        ''', (quantity, product_name))
        self.connection.commit()
    
    def restock_product(self, product_name, quantity):
        self.cursor.execute('''
            UPDATE products
            SET quantity = quantity + ?
            WHERE name = ?
        ''', (quantity, product_name))
        self.connection.commit()

    def remove_product(self, product_id):
        self.cursor.execute('''
            DELETE FROM products WHERE id = ?
        ''', (product_id,))
        self.connection.commit()

    def get_cart_items(self, user_id):
        self.cursor.execute('''
            SELECT name, price, quantity FROM cart WHERE user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()

    def clear_cart(self, user_id):
        self.cursor.execute('''
            DELETE FROM cart WHERE user_id = ?
        ''', (user_id,))
        self.connection.commit()

    def add_to_cart(self, user_id, product_id, name, price, quantity):
        self.cursor.execute('''
            INSERT INTO cart (user_id, product_id, name, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, product_id, name, price, quantity))
        self.connection.commit()

    def update_product_rating(self, product_id, rating):
        self.cursor.execute('''
            UPDATE products
            SET rating = ?
            WHERE id = ?
        ''', (rating, product_id))
        self.connection.commit()

    def insert_message(self, user_id, message):
        self.cursor.execute('''
            INSERT INTO messages (user_id, message) VALUES (?, ?)
        ''', (user_id, message))
        self.connection.commit()

    def get_messages(self):
        self.cursor.execute('''
            SELECT m.id, u.username, m.message, m.timestamp
            FROM messages m
            JOIN users u ON m.user_id = u.id
            ORDER BY m.timestamp DESC
        ''')
        return self.cursor.fetchall()

    def insert_response(self, message_id, staff_username, reply):
        self.cursor.execute('''
            INSERT INTO replies (message_id, staff_username, reply) VALUES (?, ?, ?)
        ''', (message_id, staff_username, reply))
        self.connection.commit()

    def get_replies(self, user_id, limit=10, offset=0):
        self.cursor.execute('''
            SELECT m.id, m.message, r.reply, r.timestamp
            FROM messages m
            LEFT JOIN replies r ON m.id = r.message_id
            WHERE m.user_id = ?
            ORDER BY m.timestamp DESC, r.timestamp DESC
            LIMIT ? OFFSET ?
        ''', (user_id, limit, offset))
        return self.cursor.fetchall()

    def get_responses(self, user_id, limit=10, offset=0):
        self.cursor.execute('''
            SELECT responses.response, responses.timestamp, responses.staff_username
            FROM responses
            JOIN messages ON responses.message_id = messages.id
            WHERE messages.user_id = ?
            ORDER BY responses.timestamp DESC
            LIMIT ? OFFSET ?
        ''', (user_id, limit, offset))
        return self.cursor.fetchall()

    def save_order(self, user_id):
        cart_items = self.get_cart_items(user_id)
        for item in cart_items:
            name, price, quantity = item
            product_id = self.get_product_id_by_name(name)
            total_price = price * quantity
            self.cursor.execute('''
                INSERT INTO orders (user_id, product_id, quantity, total_price)
                VALUES (?, ?, ?, ?)
            ''', (user_id, product_id, quantity, total_price))
        self.connection.commit()

    def get_product_id_by_name(self, name):
        self.cursor.execute('''
            SELECT id FROM products WHERE name = ?
        ''', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def check_products(self):
        self.cursor.execute('SELECT * FROM products')
        products = self.cursor.fetchall()
        return products

    def update_product_price(self, product_name, new_price):
        try:
            self.cursor.execute('UPDATE products SET price = ? WHERE name = ?', (new_price, product_name))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating product price: {e}")
            return False
        
    def close(self):
        self.connection.close()

    def get_message_id_by_timestamp_and_user(self, timestamp, username):
        self.cursor.execute('''
            SELECT m.id
            FROM messages m
            JOIN users u ON m.user_id = u.id
            WHERE m.timestamp = ? AND u.username = ?
        ''', (timestamp, username))
        result = self.cursor.fetchone()
        return result[0] if result else None