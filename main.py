import telebot
import os # 

TOKEN = os.getenv('TELEGRAM_TOKEN') 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здарова, заебал (теперь с сервера!)") # Можешь поменять текст, чтобы видеть разницу

bot.polling(none_stop=True)ы
