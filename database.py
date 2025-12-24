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
                disclaimer_accepted INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Products table - ОБНОВЛЕННАЯ для веб-сайта
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL,
                thc_content INTEGER,
                price INTEGER NOT NULL,
                description TEXT,
                special_offer TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table - для заказов с сайта
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS web_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                items TEXT NOT NULL,
                address TEXT NOT NULL,
                location_lat REAL,
                location_lng REAL,
                delivery_time TEXT NOT NULL,
                comment TEXT,
                subtotal TEXT NOT NULL,
                delivery_cost TEXT NOT NULL,
                total TEXT NOT NULL,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ============ USER METHODS ============
    
    def add_user(self, user_id, username, first_name, last_name, language='en'):
        """Add or update user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, language)
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
    
    def has_accepted_disclaimer(self, user_id):
        """Check if user accepted disclaimer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT disclaimer_accepted FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        return bool(result and result[0]) if result else False
    
    def accept_disclaimer(self, user_id):
        """Mark user as accepted disclaimer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET disclaimer_accepted = 1 WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    # ============ PRODUCT METHODS ============
    
    def add_product(self, name, category, product_type, thc_content, price, 
                   description='', special_offer=''):
        """Add new product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (name, category, type, thc_content, price, description, special_offer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, product_type, thc_content, price, description, special_offer))
        
        product_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return product_id
    
    def get_all_products(self, include_hidden=False):
        """Get all products"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if include_hidden:
            cursor.execute('''
                SELECT id, name, category, type, thc_content, price, 
                       description, special_offer, is_active
                FROM products
                ORDER BY created_at DESC
            ''')
        else:
            cursor.execute('''
                SELECT id, name, category, type, thc_content, price, 
                       description, special_offer, is_active
                FROM products
                WHERE is_active = 1
                ORDER BY created_at DESC
            ''')
        
        products = cursor.fetchall()
        conn.close()
        
        return products
    
    def get_products_by_category(self, category):
        """Get products by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, type, thc_content, price, description, special_offer
            FROM products
            WHERE category = ? AND is_active = 1
            ORDER BY created_at DESC
        ''', (category,))
        
        products = cursor.fetchall()
        conn.close()
        
        return products
    
    def get_products_by_type(self, category, product_type):
        """Get products by category and type"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, type, thc_content, price, description, special_offer
            FROM products
            WHERE category = ? AND type = ? AND is_active = 1
            ORDER BY created_at DESC
        ''', (category, product_type))
        
        products = cursor.fetchall()
        conn.close()
        
        return products
    
    def get_product(self, product_id):
        """Get product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, category, type, thc_content, price, description, special_offer, is_active
            FROM products
            WHERE id = ?
        ''', (product_id,))
        
        product = cursor.fetchone()
        conn.close()
        
        return product
    
    def update_product(self, product_id, **kwargs):
        """Update product fields"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            values.append(value)
        
        values.append(product_id)
        query = f"UPDATE products SET {', '.join(fields)} WHERE id = ?"
        
        cursor.execute(query, values)
        
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
        result = cursor.fetchone()
        
        if result:
            new_status = 0 if result[0] else 1
            cursor.execute('UPDATE products SET is_active = ? WHERE id = ?', (new_status, product_id))
            conn.commit()
            conn.close()
            return new_status
        
        conn.close()
        return None
    
    # ============ WEB ORDER METHODS ============
    
    def save_web_order(self, order_data):
        """Save order from website"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO web_orders (
                order_id, customer_name, customer_phone, items, address,
                location_lat, location_lng, delivery_time, comment,
                subtotal, delivery_cost, total
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(order_data['orderId']),
            order_data['name'],
            order_data['phone'],
            json.dumps(order_data['items'], ensure_ascii=False),
            order_data['address'],
            order_data['location']['lat'],
            order_data['location']['lng'],
            order_data['time'],
            order_data.get('comment', ''),
            order_data['subtotal'],
            order_data['delivery'],
            order_data['total']
        ))
        
        conn.commit()
        conn.close()
    
    def get_web_orders(self, limit=50):
        """Get recent web orders"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT order_id, customer_name, customer_phone, total, status, created_at
            FROM web_orders
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        orders = cursor.fetchall()
        conn.close()
        
        return orders
    
    def get_web_order(self, order_id):
        """Get specific web order"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM web_orders WHERE order_id = ?
        ''', (order_id,))
        
        order = cursor.fetchone()
        conn.close()
        
        return order
    
    # ============ ANALYTICS METHODS ============
    
    def log_action(self, user_id, action, details=''):
        """Log user action"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analytics (user_id, action, details)
            VALUES (?, ?, ?)
        ''', (user_id, action, details))
        
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        users = cursor.fetchone()[0]
        
        # Active products
        cursor.execute('SELECT COUNT(*) FROM products WHERE is_active = 1')
        products = cursor.fetchone()[0]
        
        # Today's catalog views
        cursor.execute('''
            SELECT COUNT(*) FROM analytics 
            WHERE action = 'catalog_view' 
            AND DATE(created_at) = DATE('now')
        ''')
        views = cursor.fetchone()[0]
        
        # Web orders today
        cursor.execute('''
            SELECT COUNT(*) FROM web_orders 
            WHERE DATE(created_at) = DATE('now')
        ''')
        web_orders = cursor.fetchone()[0]
        
        # Total revenue today
        cursor.execute('''
            SELECT SUM(CAST(REPLACE(total, '฿', '') AS INTEGER)) 
            FROM web_orders 
            WHERE DATE(created_at) = DATE('now')
        ''')
        revenue_result = cursor.fetchone()[0]
        revenue = revenue_result if revenue_result else 0
        
        conn.close()
        
        return {
            'users': users,
            'products': products,
            'views': views,
            'web_orders': web_orders,
            'revenue': revenue
        }

# Initialize database
db = Database()
