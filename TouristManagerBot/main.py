import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import database
import api_services
import urllib.parse
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BOT_TOKEN = "8050268291:AAGYI6GN-YJ0xbzWiE3nWHRcly0jvJ2gvGg"
bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}  # Формат: {telegram_id: {'state': 'awaiting_email_register', 'email': '...'}}
# Возможные состояния: awaiting_email_register, awaiting_password_register, awaiting_email_login, awaiting_password_login

def get_maps_url(name, city, coords=None):
    if coords:
        return f"https://www.google.com/maps?q={coords}"
    query = urllib.parse.quote(f"{name} {city}")
    return f"https://www.google.com/maps?q={query}"

def create_auth_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Регистрация", callback_data="register"),
        InlineKeyboardButton("Вход", callback_data="login")
    )
    return markup

def create_city_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    cities = sorted(api_services.CITY_COUNTRY.keys())
    for i in range(0, len(cities), 2):
        row = []
        row.append(InlineKeyboardButton(cities[i], callback_data=f"city_{cities[i]}"))
        if i + 1 < len(cities):
            row.append(InlineKeyboardButton(cities[i + 1], callback_data=f"city_{cities[i + 1]}"))
        markup.add(*row)
    return markup

def create_menu(city):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🌤️ Погода", callback_data=f"weather_{city}"),
        InlineKeyboardButton("💸 Валюта", callback_data=f"currency_{city}"),
        InlineKeyboardButton("🏛️ Достопримечательности", callback_data=f"sights_{city}"),
        InlineKeyboardButton("🏨 Отель", callback_data=f"hotel_{city}"),
        InlineKeyboardButton("📋 Всё сразу", callback_data=f"all_{city}"),
        InlineKeyboardButton("🔙 Выбрать другой город", callback_data="back_to_cities")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    telegram_id = message.from_user.id
    logging.info(f"Команда /start от пользователя {telegram_id}")
    bot.send_message(message.chat.id, "Добро пожаловать! Пожалуйста, зарегистрируйтесь или войдите:", reply_markup=create_auth_menu())
    user_states[telegram_id] = {'state': None, 'email': None}

@bot.message_handler(content_types=['text'])
def process_text(message):
    telegram_id = message.from_user.id
    state_data = user_states.get(telegram_id, {'state': None, 'email': None})
    state = state_data.get('state')
    logging.info(f"Обработка текста от {telegram_id}, текущее состояние: {state}")

    if state == 'awaiting_email_register':
        email = message.text.strip()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email):
            bot.send_message(message.chat.id, "Пожалуйста, введите корректный email (@gmail.com):")
            return
        user_states[telegram_id] = {'state': 'awaiting_password_register', 'email': email}
        bot.send_message(message.chat.id, "Введите пароль (минимум 6 символов):")
    elif state == 'awaiting_password_register':
        password = message.text.strip()
        if len(password) < 6:
            bot.send_message(message.chat.id, "Пароль должен содержать минимум 6 символов. Попробуйте снова:")
            return
        email = state_data['email']
        if database.register_user(telegram_id, email, password):
            user_states[telegram_id] = {'state': None, 'email': None}
            bot.send_message(message.chat.id, "Регистрация успешна! Выберите город:", reply_markup=create_city_menu())
            logging.info(f"Пользователь {telegram_id} зарегистрирован с email {email}")
        else:
            bot.send_message(message.chat.id, "Ошибка: Этот Telegram ID или email уже зарегистрирован. Пожалуйста, войдите.")
            user_states[telegram_id] = {'state': None, 'email': None}
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=create_auth_menu())
    elif state == 'awaiting_email_login':
        email = message.text.strip()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email):
            bot.send_message(message.chat.id, "Пожалуйста, введите корректный email (@gmail.com):")
            return
        user_states[telegram_id] = {'state': 'awaiting_password_login', 'email': email}
        bot.send_message(message.chat.id, "Введите пароль:")
    elif state == 'awaiting_password_login':
        password = message.text.strip()
        email = state_data['email']
        if database.authenticate_user(telegram_id, email, password):
            user_states[telegram_id] = {'state': None, 'email': None}
            bot.send_message(message.chat.id, "Вход успешен! Выберите город:", reply_markup=create_city_menu())
            logging.info(f"Пользователь {telegram_id} вошел с email {email}")
        else:
            bot.send_message(message.chat.id, "Неверный email или пароль. Попробуйте снова.")
            user_states[telegram_id] = {'state': None, 'email': None}
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=create_auth_menu())
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте команду /start для начала работы.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        telegram_id = call.from_user.id
        data = call.data
        logging.info(f"Callback от {telegram_id}: {data}")

        if data == "register":
            user_states[telegram_id] = {'state': 'awaiting_email_register', 'email': None}
            bot.send_message(call.message.chat.id, "Введите ваш email (@gmail.com):")
            bot.answer_callback_query(call.id)
        elif data == "login":
            user_states[telegram_id] = {'state': 'awaiting_email_login', 'email': None}
            bot.send_message(call.message.chat.id, "Введите ваш email (@gmail.com):")
            bot.answer_callback_query(call.id)
        else:
            if not database.is_user_registered(telegram_id):
                bot.send_message(call.message.chat.id, "Пожалуйста, зарегистрируйтесь или войдите:", reply_markup=create_auth_menu())
                bot.answer_callback_query(call.id)
                return

            if data.startswith("city_"):
                city = data.split("_")[1]
                if city in api_services.CITY_COUNTRY:
                    bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=f"Вы выбрали {city}. Что хотите узнать?",
                        reply_markup=create_menu(city)
                    )
                else:
                    bot.answer_callback_query(call.id, "Город не найден.")
            elif data == "back_to_cities":
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Выберите город:",
                    reply_markup=create_city_menu()
                )
            else:
                action, city = data.split("_")
                country_code = api_services.CITY_COUNTRY.get(city, "Unknown")
                sights = database.get_sights(city)
                logging.info(f"Действие: {action}, Город: {city}")

                if action == "weather":
                    weather = api_services.get_weather(city)
                    response = f"**Погода в {city} на день:**\n{weather}"
                    bot.send_message(call.message.chat.id, response, parse_mode="Markdown", reply_markup=create_menu(city))
                elif action == "currency":
                    currency = api_services.get_currency(country_code) if country_code != "Unknown" else "Неизвестная валюта"
                    response = f"**Валюта страны:** {currency} (по курсу к USD)"
                    bot.send_message(call.message.chat.id, response, parse_mode="Markdown", reply_markup=create_menu(city))
                elif action == "sights":
                    if sights:
                        sight1, sight2, _, sight1_coords, sight2_coords, _, sight1_photo, sight2_photo = sights
                        caption1 = f"**{sight1}** ([на карте]({get_maps_url(sight1, city, sight1_coords)}))"
                        if sight1_photo:
                            bot.send_photo(call.message.chat.id, sight1_photo, caption=caption1, parse_mode="Markdown")
                        else:
                            bot.send_message(call.message.chat.id, caption1, parse_mode="Markdown")
                        caption2 = f"**{sight2}** ([на карте]({get_maps_url(sight2, city, sight2_coords)}))"
                        if sight2_photo:
                            bot.send_photo(call.message.chat.id, sight2_photo, caption=caption2, parse_mode="Markdown")
                        else:
                            bot.send_message(call.message.chat.id, caption2, parse_mode="Markdown")
                        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=create_menu(city))
                    else:
                        response = "Достопримечательности для этого города не найдены."
                        bot.send_message(call.message.chat.id, response, parse_mode="Markdown", reply_markup=create_menu(city))
                elif action == "hotel":
                    if sights:
                        _, _, hotel, _, _, hotel_coords, _, _ = sights
                        response = f"**Рекомендуемый отель в {city}:**\n{hotel} ([на карте]({get_maps_url(hotel, city, hotel_coords)}))"
                        bot.send_message(call.message.chat.id, response, parse_mode="Markdown", reply_markup=create_menu(city))
                elif action == "all":
                    weather = api_services.get_weather(city)
                    currency = api_services.get_currency(country_code) if country_code != "Unknown" else "Неизвестная валюта"
                    if sights:
                        sight1, sight2, hotel, sight1_coords, sight2_coords, hotel_coords, sight1_photo, sight2_photo = sights
                        response = (
                            f"**Погода в {city} на неделю:**\n{weather}\n\n"
                            f"**Валюта страны:** {currency} (по курсу к USD)\n\n"
                        )
                        bot.send_message(call.message.chat.id, response, parse_mode="Markdown")
                        caption1 = f"**{sight1}** ([на карте]({get_maps_url(sight1, city, sight1_coords)}))"
                        if sight1_photo:
                            bot.send_photo(call.message.chat.id, sight1_photo, caption=caption1, parse_mode="Markdown")
                        else:
                            bot.send_message(call.message.chat.id, caption1, parse_mode="Markdown")
                        caption2 = f"**{sight2}** ([на карте]({get_maps_url(sight2, city, sight2_coords)}))"
                        if sight2_photo:
                            bot.send_photo(call.message.chat.id, sight2_photo, caption=caption2, parse_mode="Markdown")
                        else:
                            bot.send_message(call.message.chat.id, caption2, parse_mode="Markdown")
                        response = f"**Рекомендуемый отель:**\n{hotel} ([на карте]({get_maps_url(hotel, city, hotel_coords)}))"
                        bot.send_message(call.message.chat.id, response, parse_mode="Markdown", reply_markup=create_menu(city))
                    else:
                        response = (
                            f"**Погода в {city} на неделю:**\n{weather}\n\n"
                            f"**Валюта страны:** {currency} (по курсу к USD)\n\n"
                            "Достопримечательности и отель для этого города не найдены."
                        )
                        bot.send_message(call.message.chat.id, response, parse_mode="Markdown", reply_markup=create_menu(city))

            bot.answer_callback_query(call.id)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Произошла ошибка. Попробуйте снова.")
        logging.error(f"Ошибка в callback_query для {telegram_id}: {e}")

if __name__ == '__main__':
    logging.info("Запуск бота...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
