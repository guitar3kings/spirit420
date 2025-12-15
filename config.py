import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

# Shop Information
SHOP_NAME = "spirit420"
SHOP_PHONE = os.getenv('SHOP_PHONE')
SHOP_ADDRESS_RU = os.getenv('SHOP_ADDRESS_RU')
SHOP_ADDRESS_EN = os.getenv('SHOP_ADDRESS_EN')
SHOP_ADDRESS_TH = os.getenv('SHOP_ADDRESS_TH')
SHOP_LAT = float(os.getenv('SHOP_LAT', '7.8804'))
SHOP_LON = float(os.getenv('SHOP_LON', '98.3923'))

# Working Hours
WORKING_HOURS_RU = "Пн-Вс: 10:00 - 21:00"
WORKING_HOURS_EN = "Mon-Sun: 10:00 AM - 9:00 PM"
WORKING_HOURS_TH = "จันทร์-อาทิตย์: 10:00 - 21:00"

# Delivery Zones (in THB)
DELIVERY_ZONES = {
    'zone1': {'name_ru': 'Пхукет-таун центр', 'name_en': 'Phuket Town Center', 'name_th': 'ภูเก็ตทาวน์', 'price': 0},
    'zone2': {'name_ru': 'Чалонг, Раваи (начало)', 'name_en': 'Chalong, Rawai (near)', 'name_th': 'ฉลอง ราไวย์', 'price': 100},
    'zone3': {'name_ru': 'Патонг, Карон, Ката', 'name_en': 'Patong, Karon, Kata', 'name_th': 'ป่าตอง กะรน กะตะ', 'price': 150},
    'zone4': {'name_ru': 'Банг Тао, Сурин, Камала', 'name_en': 'Bang Tao, Surin, Kamala', 'name_th': 'บางเทา สุรินทร์ กมลา', 'price': 200},
    'zone5': {'name_ru': 'Другие районы', 'name_en': 'Other areas', 'name_th': 'พื้นที่อื่นๆ', 'price': 250}
}

# Minimum Order
MIN_ORDER_AMOUNT = 500

# Order Statuses
ORDER_STATUS = {
    'new': {'emoji': '⏳', 'ru': 'Принят', 'en': 'Received', 'th': 'ได้รับแล้ว'},
    'confirmed': {'emoji': '✅', 'ru': 'Подтвержден', 'en': 'Confirmed', 'th': 'ยืนยันแล้ว'},
    'preparing': {'emoji': '📦', 'ru': 'Готовится', 'en': 'Preparing', 'th': 'กำลังเตรียม'},
    'delivery': {'emoji': '🚗', 'ru': 'В пути', 'en': 'On the way', 'th': 'กำลังจัดส่ง'},
    'completed': {'emoji': '✔️', 'ru': 'Доставлен', 'en': 'Delivered', 'th': 'จัดส่งแล้ว'},
    'cancelled': {'emoji': '❌', 'ru': 'Отменен', 'en': 'Cancelled', 'th': 'ยกเลิกแล้ว'}
}