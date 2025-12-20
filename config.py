import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
OWNER_ID = int(os.getenv('OWNER_ID', ADMIN_ID))  # Thai owner ID

# Shop Information
SHOP_NAME = "spirit420"
SHOP_PHONE = os.getenv('SHOP_PHONE')
SHOP_ADDRESS_RU = os.getenv('SHOP_ADDRESS_RU')
SHOP_ADDRESS_EN = os.getenv('SHOP_ADDRESS_EN')
SHOP_ADDRESS_TH = os.getenv('SHOP_ADDRESS_TH')
SHOP_LAT = float(os.getenv('SHOP_LAT', '7.884528'))
SHOP_LON = float(os.getenv('SHOP_LON', '98.365056'))

# Working Hours
WORKING_HOURS_RU = "Пн-Вс: 11:00 - 02:00"
WORKING_HOURS_EN = "Mon-Sun: 11:00 AM - 2:00 AM"
WORKING_HOURS_TH = "จันทร์-อาทิตย์: 11:00 - 02:00"

# Shop Description
SHOP_DESCRIPTION_RU = "Лицензированный магазин каннабиса, Пхукет"
SHOP_DESCRIPTION_EN = "Licensed cannabis shop, Phuket"
SHOP_DESCRIPTION_TH = "ร้านกัญชาที่ได้รับใบอนุญาต ภูเก็ต"

# Contact Info
LINE_ID = os.getenv('LINE_ID', '@spirit420')
WHATSAPP = os.getenv('WHATSAPP', '+66611483677')

# Product Categories
CATEGORIES = {
    'sorts': {'ru': '🌱 Сорта', 'en': '🌱 Sorts', 'th': '🌱 สายพันธุ์'},
    'joints': {'ru': '🚬 Преролы', 'en': '🚬 Prerolled Joints', 'th': '🚬 พรีโรล'}
}

# Product Types
PRODUCT_TYPES = {
    'indica': {'emoji': '🌙', 'ru': 'Indica', 'en': 'Indica', 'th': 'อินดิกา'},
    'sativa': {'emoji': '☀️', 'ru': 'Sativa', 'en': 'Sativa', 'th': 'ซาติวา'},
    'hybrid': {'emoji': '🌓', 'ru': 'Hybrid', 'en': 'Hybrid', 'th': 'ไฮบริด'}
}