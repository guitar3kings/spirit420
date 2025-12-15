import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (Application, CommandHandler, MessageHandler, 
                         CallbackQueryHandler, ContextTypes, filters, ConversationHandler)
from datetime import datetime

from config import *
from texts import get_text
from database import db

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(SELECTING_ACTION, SELECTING_CATEGORY, ORDERING_ITEM, SELECTING_ZONE,
 ENTERING_ADDRESS, ENTERING_PHONE, SELECTING_TIME, ENTERING_COMMENT) = range(8)

# Helper Functions
def get_user_lang(update: Update) -> str:
    """Get user's language preference"""
    return db.get_user_language(update.effective_user.id)

def get_main_keyboard(lang: str):
    """Generate main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'catalog'), callback_data='catalog')],
        [InlineKeyboardButton(get_text(lang, 'order'), callback_data='order')],
        [InlineKeyboardButton(get_text(lang, 'my_orders'), callback_data='my_orders')],
        [InlineKeyboardButton(get_text(lang, 'info'), callback_data='info')],
        [InlineKeyboardButton(get_text(lang, 'language'), callback_data='language')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_category_keyboard(lang: str):
    """Generate category selection keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'black_tea'), callback_data='cat_black')],
        [InlineKeyboardButton(get_text(lang, 'green_tea'), callback_data='cat_green')],
        [InlineKeyboardButton(get_text(lang, 'mix_tea'), callback_data='cat_mix')],
        [InlineKeyboardButton(get_text(lang, 'back'), callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_language_keyboard():
    """Generate language selection keyboard"""
    keyboard = [
        [InlineKeyboardButton('🇷🇺 Русский', callback_data='lang_ru')],
        [InlineKeyboardButton('🇬🇧 English', callback_data='lang_en')],
        [InlineKeyboardButton('🇹🇭 ไทย', callback_data='lang_th')],
    ]
    return InlineKeyboardMarkup(keyboard)

def format_product_name(product, lang):
    """Get product name in user's language"""
    if lang == 'ru':
        return product[1]
    elif lang == 'en':
        return product[2]
    else:
        return product[3]

def format_product_description(product, lang):
    """Get product description in user's language"""
    if lang == 'ru':
        return product[5]
    elif lang == 'en':
        return product[6]
    else:
        return product[7]

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    # Add user to database
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    
    lang = get_user_lang(update)
    
    await update.message.reply_text(
        get_text(lang, 'welcome'),
        reply_markup=get_main_keyboard(lang)
    )

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    
    await query.edit_message_text(
        get_text(lang, 'welcome'),
        reply_markup=get_main_keyboard(lang)
    )

# Catalog Handlers
async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show catalog categories"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    
    await query.edit_message_text(
        get_text(lang, 'select_category'),
        reply_markup=get_category_keyboard(lang)
    )

async def show_category_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show products in selected category"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    category = query.data.split('_')[1]  # cat_black -> black
    
    products = db.get_products_by_category(category)
    
    if not products:
        await query.edit_message_text(
            get_text(lang, 'no_products'),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text(lang, 'back'), callback_data='catalog')
            ]])
        )
        return
    
    # Show products list
    for product in products:
        name = format_product_name(product, lang)
        description = format_product_description(product, lang)
        price = product[4]
        
        text = get_text(lang, 'product_info', name=name, price=price, description=description)
        
        keyboard = [
            [InlineKeyboardButton(get_text(lang, 'order_this'), 
                                callback_data=f'order_product_{product[0]}')]
        ]
        
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    # Back button
    await query.message.reply_text(
        '—',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(get_text(lang, 'back'), callback_data='catalog')
        ]])
    )

# Order Handlers
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start order process"""
    query = update.callback_query
    if query:
        await query.answer()
    
    lang = get_user_lang(update)
    
    # Initialize order data
    context.user_data['order'] = {}
    
    keyboard = [[InlineKeyboardButton(get_text(lang, 'select_from_catalog'), callback_data='catalog')]]
    
    if query:
        await query.edit_message_text(
            get_text(lang, 'order_start'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            get_text(lang, 'order_start'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    return ORDERING_ITEM

async def order_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add product to order"""
    query = update.callback_query
    await query.answer()
    
    product_id = int(query.data.split('_')[2])
    product = db.get_product(product_id)
    
    lang = get_user_lang(update)
    name = format_product_name(product, lang)
    
    # Save to order
    if 'order' not in context.user_data:
        context.user_data['order'] = {}
    
    context.user_data['order']['items'] = [{'name': name, 'price': product[4]}]
    context.user_data['order']['items_cost'] = product[4]
    
    await query.message.reply_text(get_text(lang, 'order_added', item=name))
    
    # Ask for delivery zone
    return await ask_delivery_zone(update, context)

async def order_item_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text input for order item"""
    item_text = update.message.text
    lang = get_user_lang(update)
    
    # Save item (we'll parse price later or set default)
    if 'order' not in context.user_data:
        context.user_data['order'] = {}
    
    context.user_data['order']['items'] = [{'name': item_text, 'price': 300}]
    context.user_data['order']['items_cost'] = 300
    
    await update.message.reply_text(get_text(lang, 'order_added', item=item_text))
    
    return await ask_delivery_zone(update, context)

async def ask_delivery_zone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for delivery zone"""
    lang = get_user_lang(update)
    
    keyboard = []
    for zone_id, zone_data in DELIVERY_ZONES.items():
        zone_name = zone_data[f'name_{lang}']
        price = zone_data['price']
        keyboard.append([InlineKeyboardButton(
            f"{zone_name} - ฿{price}", 
            callback_data=f'zone_{zone_id}'
        )])
    
    if update.callback_query:
        await update.callback_query.message.reply_text(
            get_text(lang, 'enter_zone'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            get_text(lang, 'enter_zone'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    return SELECTING_ZONE

async def select_zone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle zone selection"""
    query = update.callback_query
    await query.answer()
    
    zone_id = query.data.split('_')[1]
    zone_data = DELIVERY_ZONES[zone_id]
    
    context.user_data['order']['delivery_zone'] = zone_id
    context.user_data['order']['delivery_cost'] = zone_data['price']
    
    lang = get_user_lang(update)
    
    # Confirm delivery cost
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'yes'), callback_data='confirm_zone')],
        [InlineKeyboardButton(get_text(lang, 'no'), callback_data='order')]
    ]
    
    await query.edit_message_text(
        get_text(lang, 'delivery_cost', cost=zone_data['price']),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return SELECTING_ZONE

async def confirm_zone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm zone and ask for address"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    
    keyboard = [[KeyboardButton(get_text(lang, 'send_location'), request_location=True)]]
    
    await query.message.reply_text(
        get_text(lang, 'enter_address'),
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    
    return ENTERING_ADDRESS

async def receive_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive address (text or location)"""
    lang = get_user_lang(update)
    
    if update.message.location:
        lat = update.message.location.latitude
        lon = update.message.location.longitude
        address = f"📍 Геолокация: {lat}, {lon}"
    else:
        address = update.message.text
    
    context.user_data['order']['address'] = address
    
    keyboard = [[KeyboardButton(get_text(lang, 'share_phone'), request_contact=True)]]
    
    await update.message.reply_text(
        get_text(lang, 'enter_phone'),
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    
    return ENTERING_PHONE

async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive phone number"""
    lang = get_user_lang(update)
    
    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        phone = update.message.text
    
    context.user_data['order']['phone'] = phone
    
    # Ask for delivery time
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'today_afternoon'), callback_data='time_today_afternoon')],
        [InlineKeyboardButton(get_text(lang, 'today_evening'), callback_data='time_today_evening')],
        [InlineKeyboardButton(get_text(lang, 'tomorrow_morning'), callback_data='time_tomorrow_morning')],
        [InlineKeyboardButton(get_text(lang, 'tomorrow_afternoon'), callback_data='time_tomorrow_afternoon')],
        [InlineKeyboardButton(get_text(lang, 'tomorrow_evening'), callback_data='time_tomorrow_evening')],
        [InlineKeyboardButton(get_text(lang, 'other_time'), callback_data='time_other')]
    ]
    
    await update.message.reply_text(
        get_text(lang, 'select_time'),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return SELECTING_TIME

async def select_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle time selection"""
    query = update.callback_query
    await query.answer()
    
    time_key = query.data.split('_', 1)[1]
    lang = get_user_lang(update)
    
    if time_key == 'other':
        await query.edit_message_text(get_text(lang, 'enter_other_time'))
        return SELECTING_TIME
    
    context.user_data['order']['delivery_time'] = get_text(lang, f'time_{time_key}')
    
    # Ask for comment
    keyboard = [[InlineKeyboardButton(get_text(lang, 'skip'), callback_data='skip_comment')]]
    
    await query.edit_message_text(
        get_text(lang, 'enter_comment'),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return ENTERING_COMMENT

async def receive_time_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive custom time as text"""
    context.user_data['order']['delivery_time'] = update.message.text
    
    lang = get_user_lang(update)
    keyboard = [[InlineKeyboardButton(get_text(lang, 'skip'), callback_data='skip_comment')]]
    
    await update.message.reply_text(
        get_text(lang, 'enter_comment'),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return ENTERING_COMMENT

async def receive_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive order comment"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        comment = get_text(get_user_lang(update), 'skip')
    else:
        comment = update.message.text
    
    context.user_data['order']['comment'] = comment
    
    return await show_order_confirmation(update, context)

async def show_order_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show order confirmation"""
    lang = get_user_lang(update)
    order = context.user_data['order']
    
    # Format items
    items_text = '\n'.join([f"• {item['name']} - ฿{item['price']}" 
                           for item in order['items']])
    
    # Create temporary order ID
    order_id = '---'
    
    total = order['items_cost'] + order['delivery_cost']
    
    text = get_text(lang, 'order_confirmation',
                   order_id=order_id,
                   items=items_text,
                   address=order['address'],
                   phone=order['phone'],
                   time=order['delivery_time'],
                   comment=order.get('comment', '-'),
                   items_cost=order['items_cost'],
                   delivery_cost=order['delivery_cost'],
                   total=total)
    
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'confirm_order'), callback_data='confirm_order')],
        [InlineKeyboardButton(get_text(lang, 'edit_order'), callback_data='order')]
    ]
    
    if update.callback_query:
        await update.callback_query.message.reply_text(
            text, 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    return ENTERING_COMMENT

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm and save order"""
    query = update.callback_query
    await query.answer()
    
    order_data = context.user_data['order']
    user_id = update.effective_user.id
    lang = get_user_lang(update)
    
    # Save order to database
    order_id = db.create_order(
        user_id=user_id,
        items=order_data['items'],
        address=order_data['address'],
        phone=order_data['phone'],
        delivery_time=order_data['delivery_time'],
        comment=order_data.get('comment', ''),
        delivery_zone=order_data['delivery_zone'],
        delivery_cost=order_data['delivery_cost'],
        items_cost=order_data['items_cost']
    )
    
    # Notify user
    await query.edit_message_text(
        get_text(lang, 'order_success', order_id=order_id),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(get_text(lang, 'main_menu'), callback_data='main_menu')
        ]])
    )
    
    # Notify admin
    items_text = '\n'.join([f"• {item['name']} - ฿{item['price']}" 
                           for item in order_data['items']])
    
    user = update.effective_user
    user_info = f"@{user.username}" if user.username else f"{user.first_name}"
    
    total = order_data['items_cost'] + order_data['delivery_cost']
    
    admin_text = get_text('ru', 'new_order_admin',
                         order_id=order_id,
                         user=user_info,
                         phone=order_data['phone'],
                         items=items_text,
                         address=order_data['address'],
                         time=order_data['delivery_time'],
                         comment=order_data.get('comment', '-'),
                         total=total)
    
    keyboard = [
        [InlineKeyboardButton('✅ Подтвердить', callback_data=f'admin_confirm_{order_id}')],
        [InlineKeyboardButton('❌ Отменить', callback_data=f'admin_cancel_{order_id}')]
    ]
    
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # Clear order data
    context.user_data.pop('order', None)
    
    return ConversationHandler.END

# My Orders Handlers
async def show_my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's orders"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    lang = get_user_lang(update)
    
    orders = db.get_user_orders(user_id)
    
    if not orders:
        await query.edit_message_text(
            get_text(lang, 'my_orders_empty'),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text(lang, 'back'), callback_data='main_menu')
            ]])
        )
        return
    
    await query.edit_message_text(get_text(lang, 'my_orders_list'))
    
    for order in orders:
        order_id = order[0]
        items = json.loads(order[1])
        status = order[2]
        total = order[3]
        date = order[4]
        
        items_text = ', '.join([item['name'] for item in items])
        status_info = ORDER_STATUS[status]
        status_text = f"{status_info['emoji']} {status_info[lang]}"
        
        text = get_text(lang, 'order_item',
                       order_id=order_id,
                       status=status_text,
                       date=date,
                       items=items_text,
                       total=total)
        
        keyboard = [[InlineKeyboardButton(
            get_text(lang, 'view_details'), 
            callback_data=f'order_details_{order_id}'
        )]]
        
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    await query.message.reply_text(
        '—',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(get_text(lang, 'back'), callback_data='main_menu')
        ]])
    )

async def show_order_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed order information"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[2])
    order = db.get_order(order_id)
    
    if not order:
        await query.answer(get_text(get_user_lang(update), 'error'), show_alert=True)
        return
    
    lang = get_user_lang(update)
    
    items = json.loads(order[2])
    items_text = '\n'.join([f"• {item['name']} - ฿{item['price']}" for item in items])
    
    status_info = ORDER_STATUS[order[11]]
    
    text = get_text(lang, 'order_details',
                   order_id=order[0],
                   status_emoji=status_info['emoji'],
                   status=status_info[lang],
                   date=order[12],
                   items=items_text,
                   address=order[3],
                   phone=order[4],
                   time=order[5],
                   comment=order[6] or '-',
                   items_cost=order[9],
                   delivery_cost=order[8],
                   total=order[10])
    
    keyboard = [[InlineKeyboardButton(get_text(lang, 'back'), callback_data='my_orders')]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Shop Info Handler
async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show shop information"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    
    address = SHOP_ADDRESS_RU if lang == 'ru' else (SHOP_ADDRESS_EN if lang == 'en' else SHOP_ADDRESS_TH)
    hours = WORKING_HOURS_RU if lang == 'ru' else (WORKING_HOURS_EN if lang == 'en' else WORKING_HOURS_TH)
    
    text = get_text(lang, 'shop_info',
                   address=address,
                   hours=hours,
                   phone=SHOP_PHONE)
    
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'show_map'), callback_data='show_map')],
        [InlineKeyboardButton(get_text(lang, 'back'), callback_data='main_menu')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_map(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send shop location on map"""
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_location(latitude=SHOP_LAT, longitude=SHOP_LON)
    
    lang = get_user_lang(update)
    await query.message.reply_text(
        '—',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(get_text(lang, 'back'), callback_data='info')
        ]])
    )

# Language Handler
async def show_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show language selection"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        get_text('ru', 'select_language'),
        reply_markup=get_language_keyboard()
    )

async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change user's language"""
    query = update.callback_query
    await query.answer()
    
    new_lang = query.data.split('_')[1]
    db.set_user_language(update.effective_user.id, new_lang)
    
    await query.edit_message_text(
        get_text(new_lang, 'language_changed'),
        reply_markup=get_main_keyboard(new_lang)
    )

# Admin Handlers
async def admin_confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin confirms order"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[2])
    db.update_order_status(order_id, 'confirmed')
    
    await query.edit_message_text(
        f"✅ Заказ #{order_id} подтвержден",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton('📦 В обработку', callback_data=f'admin_prepare_{order_id}')
        ]])
    )

async def admin_cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin cancels order"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[2])
    db.cancel_order(order_id)
    
    await query.edit_message_text(f"❌ Заказ #{order_id} отменен")

# Cancel handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    lang = get_user_lang(update)
    await update.message.reply_text(
        get_text(lang, 'order_cancelled'),
        reply_markup=get_main_keyboard(lang)
    )
    return ConversationHandler.END

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Order conversation handler
    order_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_order, pattern='^order$'),
            CallbackQueryHandler(order_product, pattern='^order_product_')
        ],
        states={
            ORDERING_ITEM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, order_item_text),
                CallbackQueryHandler(show_catalog, pattern='^catalog$')
            ],
            SELECTING_ZONE: [
                CallbackQueryHandler(select_zone, pattern='^zone_'),
                CallbackQueryHandler(confirm_zone, pattern='^confirm_zone$')
            ],
            ENTERING_ADDRESS: [
                MessageHandler(filters.TEXT | filters.LOCATION, receive_address)
            ],
            ENTERING_PHONE: [
                MessageHandler(filters.TEXT | filters.CONTACT, receive_phone)
            ],
            SELECTING_TIME: [
                CallbackQueryHandler(select_time, pattern='^time_'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_time_text)
            ],
            ENTERING_COMMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_comment),
                CallbackQueryHandler(receive_comment, pattern='^skip_comment$'),
                CallbackQueryHandler(confirm_order, pattern='^confirm_order$')
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(order_conv)
    application.add_handler(CallbackQueryHandler(main_menu, pattern='^main_menu$'))
    application.add_handler(CallbackQueryHandler(show_catalog, pattern='^catalog$'))
    application.add_handler(CallbackQueryHandler(show_category_products, pattern='^cat_'))
    application.add_handler(CallbackQueryHandler(show_my_orders, pattern='^my_orders$'))
    application.add_handler(CallbackQueryHandler(show_order_details, pattern='^order_details_'))
    application.add_handler(CallbackQueryHandler(show_info, pattern='^info$'))
    application.add_handler(CallbackQueryHandler(show_map, pattern='^show_map$'))
    application.add_handler(CallbackQueryHandler(show_language_selection, pattern='^language$'))
    application.add_handler(CallbackQueryHandler(change_language, pattern='^lang_'))
    application.add_handler(CallbackQueryHandler(admin_confirm_order, pattern='^admin_confirm_'))
    application.add_handler(CallbackQueryHandler(admin_cancel_order, pattern='^admin_cancel_'))
    
    # Start bot
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()