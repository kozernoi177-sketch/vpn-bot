import telebot
import os
from telebot import types

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 7006835550  # Твой Telegram ID

bot = telebot.TeleBot(TOKEN)

# Хранилище пользователей (пока в памяти)
users = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💳 Купить")
    btn2 = types.KeyboardButton("🛠 Техподдержка")
    btn3 = types.KeyboardButton("📄 О сервисе")
    markup.add(btn1, btn2, btn3)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username

    if user_id not in users:
        users[user_id] = {
            "username": username,
            "status": "new"
        }

    bot.send_message(
        message.chat.id,
        "🚀 Добро пожаловать в VPN Bot\n\n"
        "🔒 Быстрое и стабильное подключение\n"
        "💎 Тариф: 299₽ / месяц",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: True)
def handler(message):

    user_id = message.from_user.id
    username = message.from_user.username

    if message.text == "💳 Купить":

        users[user_id]["status"] = "pending"

        bot.send_message(
            message.chat.id,
            "💳 Оплатите 299₽ на карту XXXX\n\n"
            "После оплаты отправьте чек."
        )

        bot.send_message(
            ADMIN_ID,
            f"💰 Новый запрос на покупку\n"
            f"Username: @{username}\n"
            f"ID: {user_id}\n"
            f"Статус: pending"
        )

    elif message.text == "🛠 Техподдержка":
        bot.send_message(
            message.chat.id,
            "📩 Поддержка: @vpotoke013"
        )

    elif message.text == "📄 О сервисе":
        bot.send_message(
            message.chat.id,
            "⚡ Высокая скорость\n"
            "🌍 Серверы в Европе\n"
            "🔐 Без логов"
        )

    else:
        bot.send_message(
            message.chat.id,
            "Выберите кнопку ниже 👇",
            reply_markup=main_menu()
        )

# Команда для админа: подтвердить оплату
@bot.message_handler(commands=['approve'])
def approve(message):

    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split()[1])
        if user_id in users:
            users[user_id]["status"] = "active"

            bot.send_message(
                user_id,
                "✅ Оплата подтверждена!\n\n"
                "Ваш VPN скоро будет выдан."
            )

            bot.send_message(
                ADMIN_ID,
                f"Пользователь {user_id} активирован."
            )
    except:
        bot.send_message(ADMIN_ID, "Используй: /approve USER_ID")

bot.polling()
