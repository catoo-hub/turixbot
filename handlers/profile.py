from database.models import get_user, get_bookings, update_user_email
from utils.keyboard import main_menu

def register(bot):
    # == Профиль пользователя ==
    @bot.callback_query_handler(func=lambda call: call.data == "btn_profile")
    def handle_profile(call):
        import telebot
        user_id = call.from_user.id
        user = get_user(user_id)
        bookings = get_bookings(user_id)
        
        text = f"""
👤 <b>Мой профиль</b>

👥 Имя: {user['username'] or 'Не указано'}
📧 Email: {user['email'] or '❌ Не заполнен'}
💰 Баланс: {user['balance']}₽
📅 Регистрация: {user['registered_at'][:10]}

🎫 <b>Забронированные туры: {len(bookings)}</b>
        """
        
        if bookings:
            text += "\n"
            for b in bookings:
                text += f"✅ {b['name']} - {b['price']}₽\n"
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("✏️ Добавить Email", callback_data="profile_add_email"))
        markup.add(telebot.types.InlineKeyboardButton("↩️ Меню", callback_data="main_menu"))
        
        bot.edit_message_text(text,
                             user_id,
                             call.message.message_id,
                             parse_mode="HTML",
                             reply_markup=markup)
        bot.answer_callback_query(call.id)
    
    # == Добавление/обновление email ==
    @bot.callback_query_handler(func=lambda call: call.data == "profile_add_email")
    def handle_add_email(call):
        user_id = call.from_user.id
        msg = bot.send_message(user_id, "📧 Введите ваш email:")
        bot.register_next_step_handler(msg, process_email, user_id)
        bot.answer_callback_query(call.id)

    def process_email(message, user_id):
        email = message.text.strip()
        
        # Простая проверка email
        if "@" not in email or "." not in email:
            msg = bot.send_message(user_id, "❌ Некорректный email. Попробуйте снова:")
            bot.register_next_step_handler(msg, process_email, user_id)
            return
        
        # Сохраняем email
        update_user_email(user_id, email)
        bot.send_message(user_id, f"✅ Email успешно добавлен: {email}", reply_markup=main_menu())
