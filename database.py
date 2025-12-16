import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_name='spirit420.db'):
        self.db_name = db_name
        self.init_db()
        
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language TEXT DEFAULT 'en',
                accepted_disclaimer INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                product_type TEXT NOT NULL,
                thc_content INTEGER NOT NULL,
                price INTEGER NOT NULL,
                description TEXT,
                special_offer TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Add initial products if database is empty
        self.add_initial_products()
    
    def add_initial_products(self):
        """Add initial product catalog"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if products exist
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        initial_products = [
            # SORTS
            ('Miami', 'sorts', 'sativa', 27, 250, '', ''),
            ('Dosi Dos', 'sorts', 'indica', 27, 250, '', ''),
            ('Frozen Joke', 'sorts', 'indica', 27, 250, '', ''),
            ('Rainbow Inferno', 'sorts', 'sativa', 27, 300, '', ''),
            ('LA', 'sorts', 'sativa', 24, 150, '', ''),
            ('Super Boof', 'sorts', 'hybrid', 27, 300, '', ''),
            ('Tropicana Chery', 'sorts', 'indica', 27, 300, '', ''),
            ('Lemon Haze', 'sorts', 'sativa', 25, 150, '', ''),
            ('Orange Haze', 'sorts', 'sativa', 27, 250, '', ''),
            ('Diamond Runt', 'sorts', 'indica', 27, 250, '', ''),
            
            # PREROLLED JOINTS
            ('Frozen Joke', 'joints', 'indica', 27, 200, '1 pcs', ''),
            ('Double Kush Cake', 'joints', 'hybrid', 26, 200, '1 pcs', ''),
            ('Double Kush Cake', 'joints', 'sativa', 26, 100, '1 pcs', 'buy 3 get 4 special deal'),
        ]
        
        cursor.executemany('''
            INSERT INTO products (name, category, product_type, thc_content, price, 
                                 description, special_offer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', initial_products)
        
        conn.commit()
        conn.close()
    
    # User Methods
    def add_user(self, user_id, username, first_name, last_name, language='en'):
        """Add or update user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, language)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, language))
        
        conn.commit()
        conn.close()
    
    def get_user_language(self, user_id):
        """Get user's language preference"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else 'en'
    
    def set_user_language(self, user_id, language):
        """Set user's language preference"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
        
        conn.commit()
        conn.close()
    
    def accept_disclaimer(self, user_id):
        """Mark user as accepted disclaimer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET accepted_disclaimer = 1 WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    def has_accepted_disclaimer(self, user_id):
        """Check if user accepted disclaimer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT accepted_disclaimer FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result and result[0] == 1
    
    # Product Methods
    def get_products_by_category(self, category):
        """Get all active products in a category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, product_type, thc_content, price, description, special_offer
            FROM products
            WHERE category = ? AND is_active = 1
            ORDER BY price DESC, name
        ''', (category,))
        
        products = cursor.fetchall()
        conn.close()
        
        return products
    
    def get_all_products(self, include_hidden=False):
        """Get all products (for admin)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if include_hidden:
            cursor.execute('''
                SELECT id, name, category, product_type, thc_content, price, 
                       description, special_offer, is_active
                FROM products
                ORDER BY category, name
            ''')
        else:
            cursor.execute('''
                SELECT id, name, category, product_type, thc_content, price, 
                       description, special_offer, is_active
                FROM products
                WHERE is_active = 1
                ORDER BY category, name
            ''')
        
        products = cursor.fetchall()
        conn.close()
        
        return products
    
    def get_product(self, product_id):
        """Get product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, category, product_type, thc_content, price,
                   description, special_offer, is_active
            FROM products
            WHERE id = ?
        ''', (product_id,))
        
        product = cursor.fetchone()
        conn.close()
        
        return product
    
    def add_product(self, name, category, product_type, thc_content, price, description='', special_offer=''):
        """Add new product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (name, category, product_type, thc_content, price, 
                                 description, special_offer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, product_type, thc_content, price, description, special_offer))
        
        product_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return product_id
    
    def update_product(self, product_id, name, category, product_type, thc_content, price, 
                      description='', special_offer=''):
        """Update product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products 
            SET name = ?, category = ?, product_type = ?, thc_content = ?, 
                price = ?, description = ?, special_offer = ?
            WHERE id = ?
        ''', (name, category, product_type, thc_content, price, description, special_offer, product_id))
        
        conn.commit()
        conn.close()
    
    def delete_product(self, product_id):
        """Delete product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        
        conn.commit()
        conn.close()
    
    def toggle_product_visibility(self, product_id):
        """Toggle product visibility"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT is_active FROM products WHERE id = ?', (product_id,))
        current = cursor.fetchone()[0]
        new_status = 0 if current == 1 else 1
        
        cursor.execute('UPDATE products SET is_active = ? WHERE id = ?', (new_status, product_id))
        
        conn.commit()
        conn.close()
        
        return new_status
    
    # Stats Methods
    def log_action(self, user_id, action):
        """Log user action"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO stats (user_id, action) VALUES (?, ?)', (user_id, action))
        
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get basic statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        users = cursor.fetchone()[0]
        
        # Total products
        cursor.execute('SELECT COUNT(*) FROM products WHERE is_active = 1')
        products = cursor.fetchone()[0]
        
        # Catalog views today
        cursor.execute('''
            SELECT COUNT(*) FROM stats 
            WHERE action = "catalog_view" 
            AND DATE(created_at) = DATE('now')
        ''')
        views = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'users': users,
            'products': products,
            'views': views
        }

# Initialize database
db = Database()