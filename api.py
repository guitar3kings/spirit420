from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db
import os

app = Flask(__name__)

# Enable CORS для всех доменов (или укажи конкретный домен Vercel)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Или укажи: ["https://твой-сайт.vercel.app"]
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'spirit420 API is running',
        'endpoints': {
            'products': '/api/products',
            'orders': '/api/orders'
        }
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all active products"""
    try:
        products = db.get_all_products(include_hidden=False)
        
        # Format products for website
        products_list = []
        for product in products:
            product_id, name, category, product_type, thc, price, description, special, is_active = product
            
            products_list.append({
                'id': product_id,
                'name': name,
                'category': category,
                'type': product_type,
                'thc': thc,
                'price': price,
                'description': description,
                'special': special,
                'desc': description  # для совместимости с текущим форматом сайта
            })
        
        return jsonify({
            'success': True,
            'products': products_list,
            'count': len(products_list)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/orders', methods=['POST'])
def save_order():
    """Save order from website"""
    try:
        order_data = request.get_json()
        
        if not order_data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['orderId', 'name', 'phone', 'items', 'address', 'location', 'time', 'total']
        for field in required_fields:
            if field not in order_data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Save to database
        db.save_web_order(order_data)
        
        return jsonify({
            'success': True,
            'orderId': order_data['orderId'],
            'message': 'Order saved successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics (for future admin dashboard)"""
    try:
        stats = db.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'spirit420-api'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
