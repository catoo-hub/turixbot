import telebot
from settings import API_TOKEN
from database.db import init_db
from handlers import register as register_handlers

def main():
    # ==Инцилизация базы данных==
    init_db()

    # ==Инцилизация бота & подключение==
    bot = telebot.TeleBot(API_TOKEN)

    # ==Регистрация хэндлеров==
    register_handlers(bot)

    # ==Хэндлер для неизвестных команд==
    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        bot.reply_to(message, f"❓ Неизвестная команда: {message.text}\nНапиши /help")

    # ==Запуск бота==
    print("✅ Бот запущен!")
    bot.infinity_polling()



if __name__ == "__main__":
    main()