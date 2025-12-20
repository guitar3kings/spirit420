import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, MessageHandler, 
                         CallbackQueryHandler, ContextTypes, filters, ConversationHandler)

from config import *
from texts import get_text
from database import db

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states for admin
(ADMIN_ADD_NAME, ADMIN_ADD_CATEGORY, ADMIN_ADD_TYPE, ADMIN_ADD_THC,
 ADMIN_ADD_PRICE, ADMIN_ADD_DESC, ADMIN_ADD_SPECIAL) = range(7)

# Helper Functions
def get_user_lang(update: Update) -> str:
    """Get user's language preference"""
    return db.get_user_language(update.effective_user.id)

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in [ADMIN_ID, OWNER_ID]

def get_main_keyboard(lang: str):
    """Generate main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'catalog'), callback_data='catalog')],
        [InlineKeyboardButton(get_text(lang, 'info'), callback_data='info')],
        [InlineKeyboardButton(get_text(lang, 'legal'), callback_data='legal')],
        [InlineKeyboardButton(get_text(lang, 'contacts'), callback_data='contacts')],
        [InlineKeyboardButton(get_text(lang, 'language'), callback_data='language')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_category_keyboard(lang: str):
    """Generate category selection keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'sorts'), callback_data='cat_sorts')],
        [InlineKeyboardButton(get_text(lang, 'joints'), callback_data='cat_joints')],
        [InlineKeyboardButton(get_text(lang, 'back'), callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_sorts_type_keyboard(lang: str):
    """Generate sorts type selection keyboard"""
    keyboard = [
        [InlineKeyboardButton('☀️ Sativa', callback_data='type_sativa')],
        [InlineKeyboardButton('🌙 Indica', callback_data='type_indica')],
        [InlineKeyboardButton('🌓 Hybrid', callback_data='type_hybrid')],
        [InlineKeyboardButton(get_text(lang, 'back'), callback_data='catalog')]
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

def format_product_card(product, lang):
    """Format product information"""
    product_id, name, product_type, thc, price, description, special = product
    
    type_info = PRODUCT_TYPES.get(product_type, {})
    type_emoji = type_info.get('emoji', '🌿')
    type_name = type_info.get(lang, product_type)
    
    special_text = f"🎁 {special}" if special else ""
    desc_text = description if description else ""
    
    return get_text(lang, 'product_card',
                   name=name,
                   type_emoji=type_emoji,
                   type=type_name,
                   thc=thc,
                   price=price,
                   special=special_text,
                   description=desc_text)

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    # Add user to database
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    
    # Check if user has selected language
    lang = get_user_lang(update)
    
    # If no language selected yet, show language selection first
    if not db.has_selected_language(user.id):
        await update.message.reply_text(
            '🌿 Welcome to spirit420!\n🌐 Please select your language:\n\nПожалуйста, выберите язык:\nกรุณาเลือกภาษา:',
            reply_markup=get_language_keyboard()
        )
        return
    
    # Check if user accepted disclaimer
    if not db.has_accepted_disclaimer(user.id):
        return await show_disclaimer(update, context)
    
    await update.message.reply_text(
        get_text(lang, 'welcome'),
        reply_markup=get_main_keyboard(lang)
    )

async def show_disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show age disclaimer"""
    lang = get_user_lang(update)
    
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'accept_disclaimer'), callback_data='accept_disclaimer')],
        [InlineKeyboardButton(get_text(lang, 'decline_disclaimer'), callback_data='decline_disclaimer')]
    ]
    
    if update.message:
        await update.message.reply_text(
            get_text(lang, 'disclaimer'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.callback_query.edit_message_text(
            get_text(lang, 'disclaimer'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def accept_disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User accepted disclaimer"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    db.accept_disclaimer(user_id)
    
    lang = get_user_lang(update)
    
    await query.edit_message_text(
        get_text(lang, 'welcome'),
        reply_markup=get_main_keyboard(lang)
    )

async def decline_disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User declined disclaimer"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    await query.edit_message_text(get_text(lang, 'disclaimer_declined'))

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
    
    user_id = update.effective_user.id
    lang = get_user_lang(update)
    
    # Log catalog view
    db.log_action(user_id, 'catalog_view')
    
    await query.edit_message_text(
        get_text(lang, 'catalog_disclaimer') + '\n\n' + get_text(lang, 'select_category'),
        reply_markup=get_category_keyboard(lang)
    )

async def show_category_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show products in selected category or type selection for sorts"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    category = query.data.split('_')[1]  # cat_sorts -> sorts
    
    # If sorts, show type selection
    if category == 'sorts':
        await query.edit_message_text(
            get_text(lang, 'select_sort_type'),
            reply_markup=get_sorts_type_keyboard(lang)
        )
        return
    
    # For joints, show all products
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
    category_name = CATEGORIES[category][lang]
    await query.edit_message_text(f"{category_name}\n\n{get_text(lang, 'catalog_disclaimer')}")
    
    for product in products:
        text = format_product_card(product, lang)
        await query.message.reply_text(text)
    
    # Back button
    await query.message.reply_text(
        '—',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(get_text(lang, 'back'), callback_data='catalog')
        ]])
    )

async def show_sorts_by_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show sorts filtered by type"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    sort_type = query.data.split('_')[1]  # type_sativa -> sativa
    
    products = db.get_products_by_type('sorts', sort_type)
    
    if not products:
        await query.edit_message_text(
            get_text(lang, 'no_products'),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text(lang, 'back'), callback_data='cat_sorts')
            ]])
        )
        return
    
    # Show products list
    type_info = PRODUCT_TYPES.get(sort_type, {})
    type_emoji = type_info.get('emoji', '🌿')
    type_name = type_info.get(lang, sort_type)
    
    await query.edit_message_text(f"{type_emoji} {type_name}\n\n{get_text(lang, 'catalog_disclaimer')}")
    
    for product in products:
        text = format_product_card(product, lang)
        await query.message.reply_text(text)
    
    # Back button
    await query.message.reply_text(
        '—',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(get_text(lang, 'back'), callback_data='cat_sorts')
        ]])
    )

# Shop Info Handler
async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show shop information"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    
    if lang == 'ru':
        address = SHOP_ADDRESS_RU
        hours = WORKING_HOURS_RU
        description = SHOP_DESCRIPTION_RU
    elif lang == 'en':
        address = SHOP_ADDRESS_EN
        hours = WORKING_HOURS_EN
        description = SHOP_DESCRIPTION_EN
    else:
        address = SHOP_ADDRESS_TH
        hours = WORKING_HOURS_TH
        description = SHOP_DESCRIPTION_TH
    
    text = get_text(lang, 'shop_info',
                   address=address,
                   hours=hours,
                   description=description)
    
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

# Legal Info Handler
async def show_legal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show legal information"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    
    keyboard = [[InlineKeyboardButton(get_text(lang, 'back'), callback_data='main_menu')]]
    
    await query.edit_message_text(
        get_text(lang, 'legal_info'),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Contacts Handler
async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show contact information"""
    query = update.callback_query
    await query.answer()
    
    lang = get_user_lang(update)
    
    text = get_text(lang, 'contacts_info')
    
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'contact_whatsapp'), url=f'https://wa.me/{WHATSAPP.replace("+", "").replace(" ", "")}')],
        [InlineKeyboardButton(get_text(lang, 'contact_line'), url=f'https://line.me/R/ti/p/{LINE_ID.replace("@", "%40")}')],
        [InlineKeyboardButton(get_text(lang, 'back'), callback_data='main_menu')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Language Handler
async def show_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show language selection"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        get_text('en', 'select_language'),
        reply_markup=get_language_keyboard()
    )

async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change user's language"""
    query = update.callback_query
    await query.answer()
    
    new_lang = query.data.split('_')[1]
    user_id = update.effective_user.id
    db.set_user_language(user_id, new_lang)
    
    # If user hasn't accepted disclaimer yet, show it after language selection
    if not db.has_accepted_disclaimer(user_id):
        return await show_disclaimer(update, context)
    
    await query.edit_message_text(
        get_text(new_lang, 'language_changed'),
        reply_markup=get_main_keyboard(new_lang)
    )

# Admin Panel
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin panel"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text(get_text(get_user_lang(update), 'access_denied'))
        return
    
    lang = get_user_lang(update)
    
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'add_product'), callback_data='admin_add')],
        [InlineKeyboardButton(get_text(lang, 'edit_product'), callback_data='admin_edit')],
        [InlineKeyboardButton(get_text(lang, 'delete_product'), callback_data='admin_delete')],
        [InlineKeyboardButton(get_text(lang, 'toggle_product'), callback_data='admin_toggle')],
        [InlineKeyboardButton(get_text(lang, 'view_stats'), callback_data='admin_stats')],
        [InlineKeyboardButton(get_text(lang, 'back'), callback_data='main_menu')]
    ]
    
    if update.message:
        await update.message.reply_text(
            get_text(lang, 'admin_menu'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.callback_query.edit_message_text(
            get_text(lang, 'admin_menu'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show statistics"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.answer(get_text(get_user_lang(update), 'access_denied'), show_alert=True)
        return
    
    lang = get_user_lang(update)
    stats = db.get_stats()
    
    text = get_text(lang, 'stats',
                   users=stats['users'],
                   products=stats['products'],
                   views=stats['views'])
    
    keyboard = [[InlineKeyboardButton(get_text(lang, 'back'), callback_data='admin')]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle product visibility"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        return
    
    lang = get_user_lang(update)
    
    products = db.get_all_products(include_hidden=True)
    
    keyboard = []
    for p in products:
        status = '✅' if p[8] else '❌'
        keyboard.append([InlineKeyboardButton(
            f"{status} {p[1]} ({p[2]})",
            callback_data=f'toggle_{p[0]}'
        )])
    
    keyboard.append([InlineKeyboardButton(get_text(lang, 'back'), callback_data='admin')])
    
    await query.edit_message_text(
        get_text(lang, 'select_product_to_toggle'),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def toggle_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle specific product"""
    query = update.callback_query
    await query.answer()
    
    product_id = int(query.data.split('_')[1])
    new_status = db.toggle_product_visibility(product_id)
    
    lang = get_user_lang(update)
    status_text = get_text(lang, 'product_visible' if new_status else 'product_hidden')
    
    await query.answer(status_text, show_alert=True)
    await admin_toggle(update, context)

async def admin_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete product"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        return
    
    lang = get_user_lang(update)
    
    products = db.get_all_products(include_hidden=True)
    
    keyboard = []
    for p in products:
        keyboard.append([InlineKeyboardButton(
            f"{p[1]} ({p[2]}, ฿{p[5]})",
            callback_data=f'delete_{p[0]}'
        )])
    
    keyboard.append([InlineKeyboardButton(get_text(lang, 'back'), callback_data='admin')])
    
    await query.edit_message_text(
        get_text(lang, 'select_product_to_delete'),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def delete_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete specific product"""
    query = update.callback_query
    await query.answer()
    
    product_id = int(query.data.split('_')[1])
    db.delete_product(product_id)
    
    lang = get_user_lang(update)
    await query.answer(get_text(lang, 'product_deleted'), show_alert=True)
    
    await admin_panel(update, context)

# Add Product Conversation
async def admin_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start adding product"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        return
    
    lang = get_user_lang(update)
    await query.edit_message_text(get_text(lang, 'enter_product_name'))
    
    return ADMIN_ADD_NAME

async def admin_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive product name"""
    context.user_data['new_product'] = {'name': update.message.text}
    
    lang = get_user_lang(update)
    
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'sorts'), callback_data='addcat_sorts')],
        [InlineKeyboardButton(get_text(lang, 'joints'), callback_data='addcat_joints')]
    ]
    
    await update.message.reply_text(
        get_text(lang, 'select_product_category'),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return ADMIN_ADD_CATEGORY

async def admin_add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive category"""
    query = update.callback_query
    await query.answer()
    
    category = query.data.split('_')[1]
    context.user_data['new_product']['category'] = category
    
    lang = get_user_lang(update)
    
    keyboard = [
        [InlineKeyboardButton('☀️ Sativa', callback_data='addtype_sativa')],
        [InlineKeyboardButton('🌙 Indica', callback_data='addtype_indica')],
        [InlineKeyboardButton('🌓 Hybrid', callback_data='addtype_hybrid')]
    ]
    
    await query.edit_message_text(
        get_text(lang, 'select_product_type'),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return ADMIN_ADD_TYPE

async def admin_add_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive type"""
    query = update.callback_query
    await query.answer()
    
    product_type = query.data.split('_')[1]
    context.user_data['new_product']['type'] = product_type
    
    lang = get_user_lang(update)
    await query.edit_message_text(get_text(lang, 'enter_thc_content'))
    
    return ADMIN_ADD_THC

async def admin_add_thc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive THC content"""
    try:
        thc = int(update.message.text)
        context.user_data['new_product']['thc'] = thc
        
        lang = get_user_lang(update)
        await update.message.reply_text(get_text(lang, 'enter_price'))
        
        return ADMIN_ADD_PRICE
    except:
        lang = get_user_lang(update)
        await update.message.reply_text(get_text(lang, 'invalid_number'))
        return ADMIN_ADD_THC

async def admin_add_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive price"""
    try:
        price = int(update.message.text)
        context.user_data['new_product']['price'] = price
        
        lang = get_user_lang(update)
        await update.message.reply_text(get_text(lang, 'enter_description'))
        
        return ADMIN_ADD_DESC
    except:
        lang = get_user_lang(update)
        await update.message.reply_text(get_text(lang, 'invalid_number'))
        return ADMIN_ADD_PRICE

async def admin_add_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive description"""
    desc = update.message.text if update.message.text != '/skip' else ''
    context.user_data['new_product']['description'] = desc
    
    lang = get_user_lang(update)
    await update.message.reply_text(get_text(lang, 'enter_special_offer'))
    
    return ADMIN_ADD_SPECIAL

async def admin_add_special(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive special offer and save product"""
    special = update.message.text if update.message.text != '/skip' else ''
    product = context.user_data['new_product']
    
    db.add_product(
        name=product['name'],
        category=product['category'],
        product_type=product['type'],
        thc_content=product['thc'],
        price=product['price'],
        description=product.get('description', ''),
        special_offer=special
    )
    
    lang = get_user_lang(update)
    await update.message.reply_text(get_text(lang, 'product_added'))
    
    # Clear data
    context.user_data.pop('new_product', None)
    
    # Show admin menu
    keyboard = [[InlineKeyboardButton(get_text(lang, 'admin_panel'), callback_data='admin')]]
    await update.message.reply_text('—', reply_markup=InlineKeyboardMarkup(keyboard))
    
    return ConversationHandler.END

async def cancel_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel admin operation"""
    context.user_data.pop('new_product', None)
    await admin_panel(update, context)
    return ConversationHandler.END

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add product conversation handler
    add_product_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_add_start, pattern='^admin_add$')],
        states={
            ADMIN_ADD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_add_name)],
            ADMIN_ADD_CATEGORY: [CallbackQueryHandler(admin_add_category, pattern='^addcat_')],
            ADMIN_ADD_TYPE: [CallbackQueryHandler(admin_add_type, pattern='^addtype_')],
            ADMIN_ADD_THC: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_add_thc)],
            ADMIN_ADD_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_add_price)],
            ADMIN_ADD_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_add_desc)],
            ADMIN_ADD_SPECIAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_add_special)]
        },
        fallbacks=[CommandHandler('cancel', cancel_admin)]
    )
    
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('admin', admin_panel))
    application.add_handler(add_product_conv)
    
    application.add_handler(CallbackQueryHandler(accept_disclaimer, pattern='^accept_disclaimer$'))
    application.add_handler(CallbackQueryHandler(decline_disclaimer, pattern='^decline_disclaimer$'))
    application.add_handler(CallbackQueryHandler(main_menu, pattern='^main_menu$'))
    application.add_handler(CallbackQueryHandler(show_catalog, pattern='^catalog$'))
    application.add_handler(CallbackQueryHandler(show_category_products, pattern='^cat_'))
    application.add_handler(CallbackQueryHandler(show_sorts_by_type, pattern='^type_'))
    application.add_handler(CallbackQueryHandler(show_info, pattern='^info$'))
    application.add_handler(CallbackQueryHandler(show_map, pattern='^show_map$'))
    application.add_handler(CallbackQueryHandler(show_legal, pattern='^legal$'))
    application.add_handler(CallbackQueryHandler(show_contacts, pattern='^contacts$'))
    application.add_handler(CallbackQueryHandler(show_language_selection, pattern='^language$'))
    application.add_handler(CallbackQueryHandler(change_language, pattern='^lang_'))
    
    # Admin handlers
    application.add_handler(CallbackQueryHandler(admin_panel, pattern='^admin$'))
    application.add_handler(CallbackQueryHandler(admin_stats, pattern='^admin_stats$'))
    application.add_handler(CallbackQueryHandler(admin_toggle, pattern='^admin_toggle$'))
    application.add_handler(CallbackQueryHandler(toggle_product, pattern='^toggle_\d+$'))
    application.add_handler(CallbackQueryHandler(admin_delete, pattern='^admin_delete$'))
    application.add_handler(CallbackQueryHandler(delete_product, pattern='^delete_\d+$'))
    
    # Start bot
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()