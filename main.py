import telebot
import os
from telebot import types # Импортируем типы, чтобы создавать кнопки

# --- БАЗА ДАННЫХ НАШИХ ПРОМОКОДОВ ---
# Мы храним все промокоды в одном месте. Так их легко менять, не трогая логику.
PROMO_CODES = {
    # Ключ 'market' - для Яндекс Маркета
    'market': {
        'name': '🛍️ Яндекс Маркет',
        # У Маркета есть подкатегории, поэтому создаем вложенный словарь
        'subcategories': {
            'market_first': {
                'name': 'На первый заказ',
                'code': '1ZAKAZ-AF',
                'conditions': 'Скидка 1000 ₽ на заказ от 3000 ₽ (на первый заказ).'
            },
            'market_repeat': {
                'name': 'На повторный заказ',
                'code': '1ZAKAZ-AF', # Пока везде один и тот же код, как ты и просил
                'conditions': 'Скидка 1000 ₽ на заказ от 3000 ₽ (на первый заказ).'
            },
            'market_tech': {
                'name': 'На технику и электронику',
                'code': '1ZAKAZ-AF',
                'conditions': 'Скидка 1000 ₽ на заказ от 3000 ₽ (на первый заказ).'
            },
            'market_home': {
                'name': 'На мебель и товары для дома',
                'code': '1ZAKAZ-AF',
                'conditions': 'Скидка 1000 ₽ на заказ от 3000 ₽ (на первый заказ).'
            }
        }
    },
    # Ключ 'food' - для Яндекс Еды
    'food': {
        'name': '🍔 Яндекс Еда',
        'code': 'F3LUT6SN',
        'conditions': 'Скидка 400 ₽ на заказ от 1000 ₽ или первая доставка бесплатно.'
    },
    # Ключ 'travel' - для Яндекс Путешествий
    'travel': {
        'name': '✈️ Яндекс Путешествия',
        'code': 'DI-PERVIYZAKAZ',
        'conditions': 'Скидка 12%, но не более 1000 ₽ для новых и постоянных клиентов.'
    },
    # Ключ 'business' - для Яндекс Бизнеса
    'business': {
        'name': '💼 Яндекс Бизнес',
        'code': 'PERK-B24D-4DBA-BCBA',
        'conditions': '5000 ₽ на запуск первой рекламной кампании при пополнении от 15 000 ₽ без НДС.'
    },
    # Ключ 'vkusvill' - для ВкусВилла
    'vkusvill': {
        'name': '🥦 ВкусВилл',
        'code': 'VS4B13',
        'conditions': 'Скидка 200 ₽ на первый заказ от 1000 ₽.'
    }
}


TOKEN = os.getenv('7987490515:AAGdjTBjYz8mlN3n4rtY665YIrXcBJCcYGE')
bot = telebot.TeleBot(TOKEN)

# --- ОБРАБОТЧИК КОМАНДЫ /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру (набор кнопок)
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Пробегаемся по нашей "базе данных" и создаем по кнопке на каждую категорию
    for key, value in PROMO_CODES.items():
        # 'text' - то, что написано на кнопке. 'callback_data' - уникальный идентификатор, который прилетит нам, когда на нее нажмут.
        button = types.InlineKeyboardButton(text=value['name'], callback_data=f"category_{key}")
        markup.add(button)

    # Приветственный текст от кота
    welcome_text = "Мяу! Я Промокот, твой личный гид в мире экономии! 😽\n\nГотов сэкономить твои денежки? Выбирай категорию, и я мигом найду для тебя лучший промокод!"
    
    # Отправляем сообщение с текстом и прикрепленными кнопками
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


# --- ГЛАВНЫЙ ОБРАБОТЧИК НАЖАТИЙ НА КНОПКИ ---
# Этот декоратор ловит все нажатия на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: True)
# --- ГЛАВНЫЙ ОБРАБОТЧИК НАЖАТИЙ НА КНОПКИ ---
# Этот декоратор ловит все нажатия на инлайн-кнопки
@callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # call.data - это тот самый 'callback_data', который мы задали кнопкам
    
    # --- ЛОГИКА ДЛЯ ГЛАВНОГО МЕНЮ ---
    if call.data.startswith("category_"):
        category_key = call.data.split('_', 1)[1]
        category = PROMO_CODES[category_key]

        if 'subcategories' in category:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for sub_key, sub_value in category['subcategories'].items():
                # Вот здесь мы создаем callback для подкатегорий, например "subcategory_market_first"
                button = types.InlineKeyboardButton(text=sub_value['name'], callback_data=f"subcategory_{sub_key}")
                markup.add(button)
            markup.add(types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Отлично! Уточняем для категории «{category['name']}»:", reply_markup=markup)
        
        else:
            promo_text = f"Держи промокод для «{category['name']}»!\n\n🎟️ **Промокод:** `{category['code']}`\n\n**Условия:** {category['conditions']}\n\nМяу! Удачных покупок!"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=promo_text, reply_markup=markup, parse_mode='Markdown')

    # --- ЛОГИКА ДЛЯ ПОДКАТЕГОРИЙ (Яндекс Маркет) ---
    # !!!!!!!!!! ВОТ ЭТОТ БЛОК МЫ ПОЛНОСТЬЮ МЕНЯЕМ !!!!!!!!!!
    elif call.data.startswith("subcategory_"):
        # Извлекаем ключ подкатегории, например 'market_first' из 'subcategory_market_first'
        subcategory_key = call.data.split('_', 1)[1]
        
        # Теперь нам нужно найти родительскую категорию и сам промокод
        parent_category_key = None
        subcategory_data = None

        for cat_key, cat_value in PROMO_CODES.items():
            if 'subcategories' in cat_value and subcategory_key in cat_value['subcategories']:
                parent_category_key = cat_key
                subcategory_data = cat_value['subcategories'][subcategory_key]
                break
        
        # Если мы нашли данные (а мы должны были найти)
        if subcategory_data:
            promo_text = f"Держи промокод для «{subcategory_data['name']}»!\n\n🎟️ **Промокод:** `{subcategory_data['code']}`\n\n**Условия:** {subcategory_data['conditions']}\n\nМяу! Удачных покупок!"
            markup = types.InlineKeyboardMarkup()
            # Кнопка "Назад" теперь ведет в меню Яндекс Маркета, используя найденный родительский ключ
            markup.add(types.InlineKeyboardButton(text="🔙 Назад к категориям Маркета", callback_data=f"category_{parent_category_key}"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=promo_text, reply_markup=markup, parse_mode='Markdown')

    # --- ЛОГИКА ДЛЯ КНОПКИ "НАЗАД" ---
    elif call.data == "back_to_main":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, value in PROMO_CODES.items():
            button = types.InlineKeyboardButton(text=value['name'], callback_data=f"category_{key}")
            markup.add(button)
        
        welcome_text = "Снова в главном меню! Что будем искать теперь? 😼"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=welcome_text, reply_markup=markup)

    # Отвечаем на запрос, чтобы у пользователя пропали "часики" на кнопке
    bot.answer_callback_query(call.id)


# Запускаем вечный опрос сервера телеграма
bot.polling(none_stop=True)