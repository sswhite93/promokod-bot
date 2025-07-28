import telebot
import os
from telebot import types

# --- БАЗА ДАННЫХ ПРОМОКОДОВ (остается без изменений) ---
PROMO_CODES = {    'market': {
        'name': '🛍️ Яндекс Маркет',
        
        'subcategories': {
            'market_first': {'name': 'На первый заказ', 'code': '1ZAKAZ-AF', 'conditions': 'Скидка 1000 ₽ на заказ от 3000 ₽ (на первый заказ).'},
            'market_repeat': {'name': 'На повторный заказ', 'code': '1ZAKAZ-AF', 'conditions': 'Скидка 1000 ₽ на заказ от 3000 ₽ (на первый заказ).'},
            'market_tech': {'name': 'На технику и электронику', 'code': '1ZAKAZ-AF', 'conditions': 'Скидка 1000 ₽ на заказ от 3000 ₽ (на первый заказ).'},
            'market_home': {'name': 'На мебель и товары для дома', 'code': '1ZAKAZ-AF', 'conditions': 'Скидка 1000 ₽ на заказ от 3000 ₽ (на первый заказ).'}
        }
    },
    'food': {'name': '🍔 Яндекс Еда', 'code': 'F3LUT6SN', 'conditions': 'Скидка 400 ₽ на заказ от 1000 ₽ или первая доставка бесплатно.'},
    'travel': {'name': '✈️ Яндекс Путешествия', 'code': 'DI-PERVIYZAKAZ', 'conditions': 'Скидка 12%, но не более 1000 ₽ для новых и постоянных клиентов.'},
    'business': {'name': '💼 Яндекс Бизнес', 'code': 'PERK-B24D-4DBA-BCBA', 'conditions': '5000 ₽ на запуск первой рекламной кампании при пополнении от 15 000 ₽ без НДС.'},
    'vkusvill': {'name': '🥦 ВкусВилл', 'code': 'VS4B13', 'conditions': 'Скидка 200 ₽ на первый заказ от 1000 ₽.'}
}

# Вписываем токен прямо сюда, как мы и договорились
TOKEN = "7987490515:AAGdjTBjYz8mlN3n4rtY665YIrXcBJCcYGE"
bot = telebot.TeleBot(TOKEN)

# --- ФУНКЦИЯ ДЛЯ ГЕНЕРАЦИИ ГЛАВНОГО МЕНЮ ---
# Выносим создание кнопок в отдельную функцию, чтобы не повторять код
def create_main_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, value in PROMO_CODES.items():
        # Новая архитектура: cat:ключ (например, "cat:market")
        button = types.InlineKeyboardButton(text=value['name'], callback_data=f"cat:{key}")
        markup.add(button)
    return markup

# --- ОБРАБОТЧИК КОМАНДЫ /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = create_main_menu_markup()
    welcome_text = "Мяу! Я Промокот, твой личный гид в мире экономии! 😽\n\nГотов сэкономить твои денежки? Выбирай категорию, и я мигом найду для тебя лучший промокод!"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


# --- ГЛАВНЫЙ ОБРАБОТЧИК НАЖАТИЙ НА КНОПКИ ---

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # call.data - это наш идентификатор, например "cat:market" или "sub:market:market_first"
    
    # --- ЛОГИКА ДЛЯ ГЛАВНОГО МЕНЮ (префикс "cat:") ---
    if call.data.startswith("cat:"):
        category_key = call.data.split(':')[1]
        category = PROMO_CODES[category_key]

        if 'subcategories' in category:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for sub_key, sub_value in category['subcategories'].items():
                # Новая архитектура: sub:родитель:потомок (например, "sub:market:market_first")
                button = types.InlineKeyboardButton(text=sub_value['name'], callback_data=f"sub:{category_key}:{sub_key}")
                markup.add(button)
            markup.add(types.InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Отлично! Уточняем для категории «{category['name']}»:", reply_markup=markup)
        
        else:
            promo_text = f"Держи промокод для «{category['name']}»!\n\n🎟️ **Промокод:** `{category['code']}`\n\n**Условия:** {category['conditions']}\n\nМяу! Удачных покупок!"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=promo_text, reply_markup=markup, parse_mode='Markdown')

    # --- ЛОГИКА ДЛЯ ПОДКАТЕГОРИЙ (префикс "sub:") ---
    elif call.data.startswith("sub:"):
        # Разбираем команду "sub:market:market_first" на части
        _, parent_key, sub_key = call.data.split(':')
        
        subcategory = PROMO_CODES[parent_key]['subcategories'][sub_key]
        
        promo_text = f"Держи промокод для «{subcategory['name']}»!\n\n🎟️ **Промокод:** `{subcategory['code']}`\n\n**Условия:** {subcategory['conditions']}\n\nМяу! Удачных покупок!"
        markup = types.InlineKeyboardMarkup()
        # Кнопка "Назад" теперь ведет в меню Яндекс Маркета
        markup.add(types.InlineKeyboardButton(text="🔙 Назад к категориям Маркета", callback_data=f"cat:{parent_key}"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=promo_text, reply_markup=markup, parse_mode='Markdown')

    # --- ЛОГИКА ДЛЯ КНОПКИ "НАЗАД В ГЛАВНОЕ МЕНЮ" ---
    elif call.data == "main_menu":
        markup = create_main_menu_markup()
        welcome_text = "Снова в главном меню! Что будем искать теперь? 😼"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=welcome_text, reply_markup=markup)

    # Отвечаем на запрос, чтобы у пользователя пропали "часики" на кнопке
    bot.answer_callback_query(call.id)


# Запускаем вечный опрос сервера телеграма
bot.polling(none_stop=True)
