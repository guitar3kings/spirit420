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
                language TEXT DEFAULT 'ru',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_ru TEXT NOT NULL,
                name_en TEXT NOT NULL,
                name_th TEXT NOT NULL,
                category TEXT NOT NULL,
                price INTEGER NOT NULL,
                description_ru TEXT,
                description_en TEXT,
                description_th TEXT,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                items TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                delivery_time TEXT NOT NULL,
                comment TEXT,
                delivery_zone TEXT NOT NULL,
                delivery_cost INTEGER NOT NULL,
                items_cost INTEGER NOT NULL,
                total_cost INTEGER NOT NULL,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Add test products if database is empty
        self.add_test_products()
    
    def add_test_products(self):
        """Add test products to catalog"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if products exist
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        test_products = [
            # Black Tea
            ('Английский завтрак', 'English Breakfast', 'อิงลิชเบรกฟาสต์', 'black', 280, 
             'Классический крепкий черный чай для бодрого утра', 
             'Classic strong black tea for an energetic morning',
             'ชาดำแบบคลาสสิกสำหรับเช้าวันใหม่'),
            ('Ассам', 'Assam', 'อัสสัม', 'black', 320,
             'Насыщенный индийский чай с солодовыми нотами',
             'Rich Indian tea with malty notes',
             'ชาอินเดียเข้มข้นพร้อมกลิ่นมอลต์'),
            ('Эрл Грей', 'Earl Grey', 'เอิร์ลเกรย์', 'black', 300,
             'Чай с ароматом бергамота',
             'Tea with bergamot flavor',
             'ชาที่มีกลิ่นเบอร์กามอต'),
            
            # Green Tea
            ('Сенча', 'Sencha', 'เซนฉะ', 'green', 350,
             'Японский зеленый чай с травянистым вкусом',
             'Japanese green tea with grassy flavor',
             'ชาเขียวญี่ปุ่นรสหญ้า'),
            ('Те Гуань Инь', 'Tie Guan Yin', 'เถกวนอิน', 'green', 420,
             'Улун премиум класса с цветочным ароматом',
             'Premium oolong with floral aroma',
             'อู่หลงพรีเมียมที่มีกลิ่นหอมดอกไม้'),
            ('Жасминовый', 'Jasmine', 'มะลิ', 'green', 280,
             'Зеленый чай с цветками жасмина',
             'Green tea with jasmine flowers',
             'ชาเขียวกับดอกมะลิ'),
            
            # Mix
            ('Масала чай', 'Masala Chai', 'มาซาลาชาย', 'mix', 340,
             'Индийский пряный чай со специями',
             'Indian spiced tea',
             'ชาเครื่องเทศอินเดีย'),
            ('Фруктовый микс', 'Fruit Mix', 'ผลไม้ผสม', 'mix', 290,
             'Смесь сушеных ягод и фруктов',
             'Mix of dried berries and fruits',
             'ผลไม้แห้งและเบอร์รี่ผสม'),
            ('Имбирь-лимон-мед', 'Ginger-Lemon-Honey', 'ขิง-มะนาว-น้ำผึ้ง', 'mix', 310,
             'Согревающий напиток для здоровья',
             'Warming drink for health',
             'เครื่องดื่มอุ่นๆเพื่อสุขภาพ'),
        ]
        
        cursor.executemany('''
            INSERT INTO products (name_ru, name_en, name_th, category, price, 
                                 description_ru, description_en, description_th)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', test_products)
        
        conn.commit()
        conn.close()
    
    # User Methods
    def add_user(self, user_id, username, first_name, last_name, language='ru'):
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
        return result[0] if result else 'ru'
    
    def set_user_language(self, user_id, language):
        """Set user's language preference"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
        
        conn.commit()
        conn.close()
    
    # Product Methods
    def get_products_by_category(self, category):
        """Get all products in a category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name_ru, name_en, name_th, price, 
                   description_ru, description_en, description_th
            FROM products
            WHERE category = ? AND is_active = 1
        ''', (category,))
        
        products = cursor.fetchall()
        conn.close()
        
        return products
    
    def get_product(self, product_id):
        """Get product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name_ru, name_en, name_th, price,
                   description_ru, description_en, description_th
            FROM products
            WHERE id = ? AND is_active = 1
        ''', (product_id,))
        
        product = cursor.fetchone()
        conn.close()
        
        return product
    
    # Order Methods
    def create_order(self, user_id, items, address, phone, delivery_time, 
                    comment, delivery_zone, delivery_cost, items_cost):
        """Create new order"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        total_cost = items_cost + delivery_cost
        items_json = json.dumps(items, ensure_ascii=False)
        
        cursor.execute('''
            INSERT INTO orders (user_id, items, address, phone, delivery_time,
                              comment, delivery_zone, delivery_cost, items_cost, total_cost)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, items_json, address, phone, delivery_time, 
              comment, delivery_zone, delivery_cost, items_cost, total_cost))
        
        order_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return order_id
    
    def get_user_orders(self, user_id):
        """Get all orders for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, items, status, total_cost, created_at
            FROM orders
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        orders = cursor.fetchall()
        conn.close()
        
        return orders
    
    def get_order(self, order_id):
        """Get order by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, items, address, phone, delivery_time, comment,
                   delivery_zone, delivery_cost, items_cost, total_cost, status, created_at
            FROM orders
            WHERE id = ?
        ''', (order_id,))
        
        order = cursor.fetchone()
        conn.close()
        
        return order
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
        
        conn.commit()
        conn.close()
    
    def cancel_order(self, order_id):
        """Cancel order"""
        self.update_order_status(order_id, 'cancelled')

# Initialize database
db = Database()