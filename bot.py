import telebot
import os
import time
from telebot import types
from datetime import datetime

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 7006835550

bot = telebot.TeleBot(TOKEN)

users = {}
LIMIT = 150  # лимит мест

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🚀 Предзапуск", "💳 Купить")
    markup.row("🌍 Проверить IP", "📡 Статус сети")
    markup.row("📊 Мой статус", "❓ FAQ")
    markup.row("🛠 Техподдержка")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {
            "status": "new",
            "joined": datetime.now().strftime("%d.%m.%Y")
        }

    bot.send_message(
        message.chat.id,
        "🛡 *SaveWafe Private Access*\n\n"
        "🔒 Закрытый VPN-доступ\n"
        "⚡ Европейская инфраструктура\n"
        "🌍 Высокая скорость\n\n"
        f"Осталось мест: {LIMIT - len(users)}",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: True)
def handler(message):
    user_id = message.from_user.id

    if message.text == "🚀 Предзапуск":
        bot.send_message(message.chat.id, "⏳ Проверяем доступ...")
        time.sleep(2)
        bot.send_message(
            message.chat.id,
            f"Вы добавлены в список ожидания.\n"
            f"Ваш номер: {len(users)}\n\n"
            "Мы уведомим вас при запуске."
        )

    elif message.text == "💳 Купить":
        users[user_id]["status"] = "pending"
        bot.send_message(message.chat.id, "⏳ Проверяем доступ...")
        time.sleep(2)
        bot.send_message(
            message.chat.id,
            "💳 Для активации требуется подтверждение.\n"
            "Оплатите 299₽ и отправьте чек."
        )

        bot.send_message(
            ADMIN_ID,
            f"💰 Новый запрос\nID: {user_id}\nСтатус: pending"
        )

    elif message.text == "🌍 Проверить IP":
        bot.send_message(
            message.chat.id,
            "🌍 Ваш IP: скрыт\n"
            "📍 Локация: защищена\n"
            "🔐 Статус: VPN не активирован"
        )

    elif message.text == "📡 Статус сети":
        bot.send_message(
            message.chat.id,
            "📡 *Статус инфраструктуры*\n\n"
            "🇩🇪 Германия — 🟢 Онлайн\n"
            "🇳🇱 Нидерланды — 🟢 Онлайн\n"
            "🇫🇷 Франция — 🟢 Онлайн\n\n"
            "Нагрузка: 34%",
            parse_mode="Markdown"
        )

    elif message.text == "📊 Мой статус":
        status = users.get(user_id, {}).get("status", "new")
        bot.send_message(
            message.chat.id,
            f"📊 Ваш статус: {status}\n"
            f"Дата входа: {users[user_id]['joined']}"
        )

    elif message.text == "❓ FAQ":
        bot.send_message(
            message.chat.id,
            "❓ *Частые вопросы*\n\n"
            "1️⃣ Работает ли на iPhone? — Да\n"
            "2️⃣ Сколько устройств? — До 3\n"
            "3️⃣ Есть ли логи? — Нет\n"
            "4️⃣ Поддержка? — 24/7",
            parse_mode="Markdown"
        )

    elif message.text == "🛠 Техподдержка":
        bot.send_message(
            message.chat.id,
            "📩 Поддержка: @vpotoke013"
        )

    else:
        bot.send_message(
            message.chat.id,
            "Выберите действие 👇",
            reply_markup=main_menu()
        )

@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        uid = int(message.text.split()[1])
        users[uid]["status"] = "active"
        bot.send_message(uid, "✅ Доступ активирован.")
        bot.send_message(ADMIN_ID, f"Пользователь {uid} активирован.")
    except:
        bot.send_message(ADMIN_ID, "Используй: /approve USER_ID")

bot.polling()
