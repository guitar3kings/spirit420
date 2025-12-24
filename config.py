import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '8592268723:AAERL30weAwcS6vCxejXvWKS-kZ72_ZPOpk')
ADMIN_ID = int(os.getenv('ADMIN_ID', '393004597'))

# Website URL (ЗАМЕНИ на свой URL от Vercel!)
# Пример: https://spirit420-website-abc123.vercel.app
WEBSITE_URL = os.getenv('WEBSITE_URL', 'https://spirit420-website.vercel.app')

# Shop Information
SHOP_NAME = "spirit420"
WHATSAPP = "+66611483677"
LINE_ID = "@spirit420"

SHOP_ADDRESS_RU = os.getenv('SHOP_ADDRESS_RU', 'Phuket Town, Thailand')
SHOP_ADDRESS_EN = os.getenv('SHOP_ADDRESS_EN', 'Phuket Town, Thailand')
SHOP_ADDRESS_TH = os.getenv('SHOP_ADDRESS_TH', 'ภูเก็ตทาวน์ ประเทศไทย')

SHOP_LAT = float(os.getenv('SHOP_LAT', '7.8804'))
SHOP_LON = float(os.getenv('SHOP_LON', '98.3923'))

# Shop Description
SHOP_DESCRIPTION_RU = "Уютное пространство для ценителей качества в самом сердце Пхукета."
SHOP_DESCRIPTION_EN = "A cozy space for quality enthusiasts in the heart of Phuket."
SHOP_DESCRIPTION_TH = "พื้นที่แสนสบายสำหรับผู้ชื่นชอบคุณภาพ ใจกลางภูเก็ต"

# Working Hours
WORKING_HOURS_RU = "Пн-Вс: 10:00 - 21:00"
WORKING_HOURS_EN = "Mon-Sun: 10:00 AM - 9:00 PM"
WORKING_HOURS_TH = "จันทร์-อาทิตย์: 10:00 - 21:00"

# Product Categories
CATEGORIES = {
    'sorts': {
        'ru': '🌱 Сорта',
        'en': '🌱 Sorts',
        'th': '🌱 สายพันธุ์'
    },
    'joints': {
        'ru': '🚬 Преролы',
        'en': '🚬 Prerolled Joints',
        'th': '🚬 พรีโรล'
    }
}

# Product Types
PRODUCT_TYPES = {
    'sativa': {
        'emoji': '☀️',
        'ru': 'Sativa',
        'en': 'Sativa',
        'th': 'Sativa'
    },
    'indica': {
        'emoji': '🌙',
        'ru': 'Indica',
        'en': 'Indica',
        'th': 'Indica'
    },
    'hybrid': {
        'emoji': '🌓',
        'ru': 'Hybrid',
        'en': 'Hybrid',
        'th': 'Hybrid'
    }
}
