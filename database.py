import sqlite3

class DatabaseHandler:
    def __init__(self, db_name="app_database.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.ensure_rating_column()

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
                quantity INTEGER NOT NULL DEFAULT 999,
                image_path TEXT,
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
        self.cursor.execute('''
            SELECT id FROM users
            WHERE username = ?
        ''', (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
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

    def add_to_cart(self, user_id, product_id, name, price, quantity):
        self.cursor.execute('''
            INSERT INTO cart (user_id, product_id, name, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, product_id, name, price, quantity))
        self.connection.commit()
        self.decrease_product_quantity(product_id, quantity)
        
    def decrease_product_quantity(self, product_id, quantity):
        self.cursor.execute('''
            UPDATE products
            SET quantity = quantity - ?
            WHERE id = ?
        ''', (quantity, product_id))
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

    def update_product_rating(self, product_id, rating):
        self.cursor.execute('''
            UPDATE products
            SET rating = ?
            WHERE id = ?
        ''', (rating, product_id))
        self.connection.commit()

    def insert_message(self, user_id, message):
        self.cursor.execute('''
            INSERT INTO messages (user_id, message)
            VALUES (?, ?)
        ''', (user_id, message))
        self.connection.commit()

    def get_messages(self):
        self.cursor.execute('''
            SELECT users.username, messages.message, messages.timestamp
            FROM messages
            JOIN users ON messages.user_id = users.id
            ORDER BY messages.timestamp DESC
        ''')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()