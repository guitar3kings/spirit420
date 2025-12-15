TEXTS = {
    'ru': {
        # Main Menu
        'welcome': '🍵 Добро пожаловать в spirit420!\n\nВыберите действие:',
        'main_menu': '🏠 Главное меню',
        'catalog': '🍵 Каталог чая',
        'order': '🚚 Заказать доставку',
        'my_orders': '📦 Мои заказы',
        'info': 'ℹ️ О магазине',
        'language': '🌐 Язык',
        'back': '⬅️ Назад',
        
        # Catalog
        'select_category': '🍵 Выберите категорию чая:',
        'black_tea': '⚫ Черный чай',
        'green_tea': '🟢 Зеленый чай',
        'mix_tea': '🌸 Микс',
        'top_5': '⭐ ТОП-5 популярных',
        'download_catalog': '📋 Скачать прайс-лист',
        'no_products': 'В этой категории пока нет товаров',
        'product_info': '🍵 {name}\n💰 Цена: ฿{price}/50г\n\n📝 {description}',
        'order_this': '🛒 Заказать это',
        'more_details': '📄 Подробнее',
        
        # Order Process
        'order_start': '🛒 Оформление заказа\n\nЧто вы хотите заказать?\n\nВведите название чая или выберите из каталога:',
        'select_from_catalog': '📋 Выбрать из каталога',
        'order_added': '✅ Добавлено в заказ: {item}',
        'enter_zone': '📍 Выберите район доставки на Пхукете:',
        'other_zone': '📍 Другой район',
        'delivery_cost': '🚚 Стоимость доставки: ฿{cost}\n\nПродолжить?',
        'yes': '✅ Да',
        'no': '❌ Нет',
        'enter_address': '📍 Укажите точный адрес доставки:\n\nВы можете написать адрес или отправить геолокацию',
        'send_location': '📍 Отправить геолокацию',
        'enter_phone': '📱 Укажите номер телефона для связи:',
        'share_phone': '📱 Поделиться номером',
        'select_time': '🕐 Выберите удобное время доставки:',
        'today_afternoon': '🕐 Сегодня 14:00-18:00',
        'today_evening': '🕐 Сегодня 18:00-21:00',
        'tomorrow_morning': '📅 Завтра 10:00-14:00',
        'tomorrow_afternoon': '📅 Завтра 14:00-18:00',
        'tomorrow_evening': '📅 Завтра 18:00-21:00',
        'other_time': '⏰ Другое время',
        'enter_other_time': 'Введите желаемое время доставки:',
        'enter_comment': '💬 Добавьте комментарий к заказу (необязательно):\n\nИли нажмите "Пропустить"',
        'skip': '⏭️ Пропустить',
        'order_confirmation': '📋 Ваш заказ #{order_id}\n\n🍵 Товары:\n{items}\n\n📍 Адрес: {address}\n📞 Телефон: {phone}\n🕐 Время: {time}\n💬 Комментарий: {comment}\n\n💰 Товары: ฿{items_cost}\n🚚 Доставка: ฿{delivery_cost}\n━━━━━━━━━━━━━\n💵 ИТОГО: ฿{total}\n\n💳 Оплата: наличными курьеру / PromptPay',
        'confirm_order': '✅ Подтвердить заказ',
        'edit_order': '✏️ Изменить',
        'order_success': '✅ Заказ #{order_id} успешно оформлен!\n\nМы свяжемся с вами в ближайшее время.\n\nСтатус заказа можно отслеживать в разделе "Мои заказы"',
        'order_cancelled': '❌ Заказ отменен',
        
        # My Orders
        'my_orders_empty': 'У вас пока нет заказов',
        'my_orders_list': '📦 Ваши заказы:',
        'order_item': '📦 Заказ #{order_id} - {status}\n📅 {date}\n🍵 {items}\n💰 ฿{total}',
        'view_details': '👁️ Подробнее',
        'cancel_order': '❌ Отменить заказ',
        'order_details': '📦 Заказ #{order_id}\n\nСтатус: {status_emoji} {status}\n📅 Дата: {date}\n\n🍵 Товары:\n{items}\n\n📍 Адрес: {address}\n📞 Телефон: {phone}\n🕐 Время доставки: {time}\n💬 Комментарий: {comment}\n\n💰 Товары: ฿{items_cost}\n🚚 Доставка: ฿{delivery_cost}\n━━━━━━━━━━━━━\n💵 ИТОГО: ฿{total}',
        
        # Shop Info
        'shop_info': '🍵 spirit420\n\n📍 Адрес:\n{address}\n\n🕐 Часы работы:\n{hours}\n\n📞 Контакты:\nТелефон: {phone}\n\n💬 Есть вопросы? Напишите нам!',
        'show_map': '📍 Показать на карте',
        'call': '📞 Позвонить',
        'contact_manager': '💬 Связаться с менеджером',
        
        # Language Selection
        'select_language': '🌐 Выберите язык / Select language / เลือกภาษา',
        'language_changed': '✅ Язык изменен на русский',
        
        # Admin
        'new_order_admin': '🔔 НОВЫЙ ЗАКАЗ #{order_id}\n\n👤 Клиент: {user}\n📱 Телефон: {phone}\n\n🍵 Товары:\n{items}\n\n📍 Адрес: {address}\n🕐 Время: {time}\n💬 Комментарий: {comment}\n\n💰 Сумма: ฿{total}',
        'admin_menu': '👨‍💼 Админ-панель',
        'change_status': 'Изменить статус',
        
        # Errors
        'error': '❌ Произошла ошибка. Попробуйте еще раз.',
        'invalid_input': '❌ Некорректный ввод. Попробуйте еще раз.',
    },
    
    'en': {
        # Main Menu
        'welcome': '🍵 Welcome to spirit420!\n\nChoose an action:',
        'main_menu': '🏠 Main Menu',
        'catalog': '🍵 Tea Catalog',
        'order': '🚚 Order Delivery',
        'my_orders': '📦 My Orders',
        'info': 'ℹ️ About Us',
        'language': '🌐 Language',
        'back': '⬅️ Back',
        
        # Catalog
        'select_category': '🍵 Select tea category:',
        'black_tea': '⚫ Black Tea',
        'green_tea': '🟢 Green Tea',
        'mix_tea': '🌸 Mix',
        'top_5': '⭐ TOP-5 Popular',
        'download_catalog': '📋 Download Price List',
        'no_products': 'No products in this category yet',
        'product_info': '🍵 {name}\n💰 Price: ฿{price}/50g\n\n📝 {description}',
        'order_this': '🛒 Order This',
        'more_details': '📄 More Details',
        
        # Order Process
        'order_start': '🛒 Order Placement\n\nWhat would you like to order?\n\nEnter tea name or select from catalog:',
        'select_from_catalog': '📋 Select from Catalog',
        'order_added': '✅ Added to order: {item}',
        'enter_zone': '📍 Select delivery area in Phuket:',
        'other_zone': '📍 Other Area',
        'delivery_cost': '🚚 Delivery cost: ฿{cost}\n\nContinue?',
        'yes': '✅ Yes',
        'no': '❌ No',
        'enter_address': '📍 Enter exact delivery address:\n\nYou can write address or send location',
        'send_location': '📍 Send Location',
        'enter_phone': '📱 Enter contact phone number:',
        'share_phone': '📱 Share Phone',
        'select_time': '🕐 Select convenient delivery time:',
        'today_afternoon': '🕐 Today 2:00-6:00 PM',
        'today_evening': '🕐 Today 6:00-9:00 PM',
        'tomorrow_morning': '📅 Tomorrow 10:00 AM-2:00 PM',
        'tomorrow_afternoon': '📅 Tomorrow 2:00-6:00 PM',
        'tomorrow_evening': '📅 Tomorrow 6:00-9:00 PM',
        'other_time': '⏰ Other Time',
        'enter_other_time': 'Enter preferred delivery time:',
        'enter_comment': '💬 Add comment to order (optional):\n\nOr press "Skip"',
        'skip': '⏭️ Skip',
        'order_confirmation': '📋 Your Order #{order_id}\n\n🍵 Items:\n{items}\n\n📍 Address: {address}\n📞 Phone: {phone}\n🕐 Time: {time}\n💬 Comment: {comment}\n\n💰 Items: ฿{items_cost}\n🚚 Delivery: ฿{delivery_cost}\n━━━━━━━━━━━━━\n💵 TOTAL: ฿{total}\n\n💳 Payment: Cash to courier / PromptPay',
        'confirm_order': '✅ Confirm Order',
        'edit_order': '✏️ Edit',
        'order_success': '✅ Order #{order_id} placed successfully!\n\nWe will contact you shortly.\n\nYou can track order status in "My Orders"',
        'order_cancelled': '❌ Order cancelled',
        
        # My Orders
        'my_orders_empty': 'You have no orders yet',
        'my_orders_list': '📦 Your orders:',
        'order_item': '📦 Order #{order_id} - {status}\n📅 {date}\n🍵 {items}\n💰 ฿{total}',
        'view_details': '👁️ Details',
        'cancel_order': '❌ Cancel Order',
        'order_details': '📦 Order #{order_id}\n\nStatus: {status_emoji} {status}\n📅 Date: {date}\n\n🍵 Items:\n{items}\n\n📍 Address: {address}\n📞 Phone: {phone}\n🕐 Delivery time: {time}\n💬 Comment: {comment}\n\n💰 Items: ฿{items_cost}\n🚚 Delivery: ฿{delivery_cost}\n━━━━━━━━━━━━━\n💵 TOTAL: ฿{total}',
        
        # Shop Info
        'shop_info': '🍵 spirit420\n\n📍 Address:\n{address}\n\n🕐 Working hours:\n{hours}\n\n📞 Contacts:\nPhone: {phone}\n\n💬 Have questions? Contact us!',
        'show_map': '📍 Show on Map',
        'call': '📞 Call',
        'contact_manager': '💬 Contact Manager',
        
        # Language Selection
        'select_language': '🌐 Выберите язык / Select language / เลือกภาษา',
        'language_changed': '✅ Language changed to English',
        
        # Admin
        'new_order_admin': '🔔 NEW ORDER #{order_id}\n\n👤 Customer: {user}\n📱 Phone: {phone}\n\n🍵 Items:\n{items}\n\n📍 Address: {address}\n🕐 Time: {time}\n💬 Comment: {comment}\n\n💰 Total: ฿{total}',
        'admin_menu': '👨‍💼 Admin Panel',
        'change_status': 'Change Status',
        
        # Errors
        'error': '❌ An error occurred. Please try again.',
        'invalid_input': '❌ Invalid input. Please try again.',
    },
    
    'th': {
        # Main Menu
        'welcome': '🍵 ยินดีต้อนรับสู่ spirit420!\n\nเลือกการดำเนินการ:',
        'main_menu': '🏠 เมนูหลัก',
        'catalog': '🍵 แคตตาล็อกชา',
        'order': '🚚 สั่งซื้อจัดส่ง',
        'my_orders': '📦 คำสั่งซื้อของฉัน',
        'info': 'ℹ️ เกี่ยวกับเรา',
        'language': '🌐 ภาษา',
        'back': '⬅️ กลับ',
        
        # Catalog
        'select_category': '🍵 เลือกหมวดหมู่ชา:',
        'black_tea': '⚫ ชาดำ',
        'green_tea': '🟢 ชาเขียว',
        'mix_tea': '🌸 ชาผสม',
        'top_5': '⭐ ยอดนิยม 5 อันดับ',
        'download_catalog': '📋 ดาวน์โหลดรายการราคา',
        'no_products': 'ยังไม่มีสินค้าในหมวดหมู่นี้',
        'product_info': '🍵 {name}\n💰 ราคา: ฿{price}/50 กรัม\n\n📝 {description}',
        'order_this': '🛒 สั่งซื้อสินค้านี้',
        'more_details': '📄 รายละเอียดเพิ่มเติม',
        
        # Order Process
        'order_start': '🛒 การสั่งซื้อ\n\nคุณต้องการสั่งอะไร?\n\nป้อนชื่อชาหรือเลือกจากแคตตาล็อก:',
        'select_from_catalog': '📋 เลือกจากแคตตาล็อก',
        'order_added': '✅ เพิ่มในคำสั่งซื้อ: {item}',
        'enter_zone': '📍 เลือกพื้นที่จัดส่งในภูเก็ต:',
        'other_zone': '📍 พื้นที่อื่น',
        'delivery_cost': '🚚 ค่าจัดส่ง: ฿{cost}\n\nดำเนินการต่อ?',
        'yes': '✅ ใช่',
        'no': '❌ ไม่',
        'enter_address': '📍 ระบุที่อยู่จัดส่งที่แน่นอน:\n\nคุณสามารถเขียนที่อยู่หรือส่งตำแหน่ง',
        'send_location': '📍 ส่งตำแหน่ง',
        'enter_phone': '📱 ระบุหมายเลขโทรศัพท์ติดต่อ:',
        'share_phone': '📱 แชร์หมายเลขโทรศัพท์',
        'select_time': '🕐 เลือกเวลาจัดส่งที่สะดวก:',
        'today_afternoon': '🕐 วันนี้ 14:00-18:00',
        'today_evening': '🕐 วันนี้ 18:00-21:00',
        'tomorrow_morning': '📅 พรุ่งนี้ 10:00-14:00',
        'tomorrow_afternoon': '📅 พรุ่งนี้ 14:00-18:00',
        'tomorrow_evening': '📅 พรุ่งนี้ 18:00-21:00',
        'other_time': '⏰ เวลาอื่น',
        'enter_other_time': 'ระบุเวลาจัดส่งที่ต้องการ:',
        'enter_comment': '💬 เพิ่มความคิดเห็นสำหรับคำสั่งซื้อ (ไม่บังคับ):\n\nหรือกด "ข้าม"',
        'skip': '⏭️ ข้าม',
        'order_confirmation': '📋 คำสั่งซื้อของคุณ #{order_id}\n\n🍵 สินค้า:\n{items}\n\n📍 ที่อยู่: {address}\n📞 โทรศัพท์: {phone}\n🕐 เวลา: {time}\n💬 ความคิดเห็น: {comment}\n\n💰 สินค้า: ฿{items_cost}\n🚚 การจัดส่ง: ฿{delivery_cost}\n━━━━━━━━━━━━━\n💵 รวม: ฿{total}\n\n💳 การชำระเงิน: เงินสดให้คนขับ / PromptPay',
        'confirm_order': '✅ ยืนยันคำสั่งซื้อ',
        'edit_order': '✏️ แก้ไข',
        'order_success': '✅ สั่งซื้อ #{order_id} สำเร็จ!\n\nเราจะติดต่อคุณในไม่ช้า\n\nคุณสามารถติดตามสถานะคำสั่งซื้อใน "คำสั่งซื้อของฉัน"',
        'order_cancelled': '❌ ยกเลิกคำสั่งซื้อแล้ว',
        
        # My Orders
        'my_orders_empty': 'คุณยังไม่มีคำสั่งซื้อ',
        'my_orders_list': '📦 คำสั่งซื้อของคุณ:',
        'order_item': '📦 คำสั่งซื้อ #{order_id} - {status}\n📅 {date}\n🍵 {items}\n💰 ฿{total}',
        'view_details': '👁️ รายละเอียด',
        'cancel_order': '❌ ยกเลิกคำสั่งซื้อ',
        'order_details': '📦 คำสั่งซื้อ #{order_id}\n\nสถานะ: {status_emoji} {status}\n📅 วันที่: {date}\n\n🍵 สินค้า:\n{items}\n\n📍 ที่อยู่: {address}\n📞 โทรศัพท์: {phone}\n🕐 เวลาจัดส่ง: {time}\n💬 ความคิดเห็น: {comment}\n\n💰 สินค้า: ฿{items_cost}\n🚚 การจัดส่ง: ฿{delivery_cost}\n━━━━━━━━━━━━━\n💵 รวม: ฿{total}',
        
        # Shop Info
        'shop_info': '🍵 spirit420\n\n📍 ที่อยู่:\n{address}\n\n🕐 เวลาทำการ:\n{hours}\n\n📞 ติดต่อ:\nโทรศัพท์: {phone}\n\n💬 มีคำถาม? ติดต่อเรา!',
        'show_map': '📍 แสดงบนแผนที่',
        'call': '📞 โทร',
        'contact_manager': '💬 ติดต่อผู้จัดการ',
        
        # Language Selection
        'select_language': '🌐 Выберите язык / Select language / เลือกภาษา',
        'language_changed': '✅ เปลี่ยนภาษาเป็นไทยแล้ว',
        
        # Admin
        'new_order_admin': '🔔 คำสั่งซื้อใหม่ #{order_id}\n\n👤 ลูกค้า: {user}\n📱 โทรศัพท์: {phone}\n\n🍵 สินค้า:\n{items}\n\n📍 ที่อยู่: {address}\n🕐 เวลา: {time}\n💬 ความคิดเห็น: {comment}\n\n💰 รวม: ฿{total}',
        'admin_menu': '👨‍💼 แผงผู้ดูแลระบบ',
        'change_status': 'เปลี่ยนสถานะ',
        
        # Errors
        'error': '❌ เกิดข้อผิดพลาด กรุณาลองอีกครั้ง',
        'invalid_input': '❌ ข้อมูลไม่ถูกต้อง กรุณาลองอีกครั้ง',
    }
}

def get_text(lang, key, **kwargs):
    """Get text in specified language with formatting"""
    text = TEXTS.get(lang, TEXTS['en']).get(key, TEXTS['en'].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text