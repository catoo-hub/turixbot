def register(bot):
    from utils.keyboard import main_menu
    
    # == Старт ==
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        from database.models import add_user
        add_user(message.from_user.id, message.from_user.username or "")
        bot.send_message(message.from_user.id, 
                        "👋 <b>Добро пожаловать в TurixBot!</b>",
                        parse_mode="HTML",
                        reply_markup=main_menu())
    
    # == Помощь ==
    @bot.message_handler(commands=['help'])
    def handle_help(message):
        bot.send_message(message.from_user.id,
                        "ℹ️ <b>Используй кнопки меню для навигации.</b>",
                        parse_mode="HTML",
                        reply_markup=main_menu())
