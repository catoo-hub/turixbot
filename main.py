import telebot
import settings

print("Hello!")

def main():
    API_TOKEN = '8219277974:AAH5OPuCRsS_zTrXWSBaZrf50h4ZFn_kO30'

    print("Hello from main()")
    bot = telebot.TeleBot(API_TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Привет, напиши /help для получения информации по боту\n")

    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.reply_to(message, "Вот доступные команды:\n/start: Запустить бота,\n/help: Отправка команд бота\n")

    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        bot.reply_to(message, message.text)

    bot.infinity_polling()



if __name__=="__main__":
    settings.intilizateDb()
    
    main()
