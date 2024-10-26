import sqlite3

class DatabaseHandler:
    def __init__(self, db_name="app_database.db"):
        self.connection = sqlite3.connect(db_name)
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
                image_path TEXT
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
        
        self.connection.commit()

    # Add user to database
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
    
    # Product display from database
    def get_products(self):
        self.cursor.execute('''
            SELECT * FROM products
        ''')
        return self.cursor.fetchall()

    def add_product(self, name, price, image_path):
        self.cursor.execute('''
            INSERT INTO products (name, price, image_path)
            VALUES (?, ?, ?)
        ''', (name, price, image_path))
        self.connection.commit()

    def add_order(self, user_id, product_id, quantity, total_price):
        self.cursor.execute('''
            INSERT INTO orders (user_id, product_id, quantity, total_price)
            VALUES (?, ?, ?, ?)
        ''', (user_id, product_id, quantity, total_price))
        self.connection.commit()
    
    def close(self):
        self.connection.close()