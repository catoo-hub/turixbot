import telebot

def main_menu():
    """Главное меню с коллбэком кнопок"""
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🌏 Туры", callback_data="btn_tours"))
    markup.add(telebot.types.InlineKeyboardButton("⭐ Избранные", callback_data="btn_favorites"))
    markup.add(telebot.types.InlineKeyboardButton("💰 Баланс", callback_data="btn_balance"))
    markup.add(telebot.types.InlineKeyboardButton("📔 Бронирования", callback_data="btn_bookings"))
    markup.add(telebot.types.InlineKeyboardButton("👤 Профиль", callback_data="btn_profile"))
    markup.add(telebot.types.InlineKeyboardButton("❓ Помощь", callback_data="btn_help"))
    return markup

def tours_pagination_keyboard(page, total_pages):
    """Инлайн клавиатура для навигации по турам"""
    markup = telebot.types.InlineKeyboardMarkup()
    
    if page > 1:
        markup.add(telebot.types.InlineKeyboardButton("⬅️ Назад", callback_data=f"tours_page_{page-1}"))
    
    if page < total_pages:
        markup.add(telebot.types.InlineKeyboardButton("➡️ Вперед", callback_data=f"tours_page_{page+1}"))
    
    markup.add(telebot.types.InlineKeyboardButton("↩️ Меню", callback_data="main_menu"))
    return markup

def tour_detail_keyboard(tour_id):
    """Клавиатура для детального просмотра тура"""
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("⭐ Добавить в избранное", callback_data=f"add_fav_{tour_id}"))
    markup.add(telebot.types.InlineKeyboardButton("💳 Забронировать", callback_data=f"book_{tour_id}"))
    markup.add(telebot.types.InlineKeyboardButton("⬅️ Назад к турам", callback_data="tours_page_1"))
    return markup

def balance_keyboard():
    """Клавиатура пополнения баланса"""
    markup = telebot.types.InlineKeyboardMarkup()
    amounts = [1000, 5000, 10000, 50000]
    for amount in amounts:
        markup.add(telebot.types.InlineKeyboardButton(f"{amount}₽", callback_data=f"add_balance_{amount}"))
    markup.add(telebot.types.InlineKeyboardButton("↩️ Меню", callback_data="main_menu"))
    return markup

def topup_tour_keyboard(tour_id):
    """Клавиатура пополнения прогресса тура с прессетами сумм"""
    markup = telebot.types.InlineKeyboardMarkup()
    amounts = [5000, 10000, 20000, 50000]
    for amount in amounts:
        markup.add(telebot.types.InlineKeyboardButton(f"Пополнить {amount}₽", callback_data=f"topup_amount_{tour_id}_{amount}"))
    markup.add(telebot.types.InlineKeyboardButton("🔄 Использовать весь баланс", callback_data=f"topup_all_{tour_id}"))
    markup.add(telebot.types.InlineKeyboardButton("⬅️ Назад", callback_data="btn_favorites"))
    return markup
