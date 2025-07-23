import telebot

TOKEN = '7987490515:AAHB8GUZdqnMP43U0V-WY92MYAkJ_9aaFKs'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здарова, заебал")

bot.polling(none_stop=True)
