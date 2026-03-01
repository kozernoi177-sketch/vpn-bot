import telebot
import os
from telebot import types

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💳 Купить")
    btn2 = types.KeyboardButton("🛠 Техподдержка")
    markup.add(btn1, btn2)

    bot.send_message(
        message.chat.id,
        "🚀 Добро пожаловать в VPN Bot\n\n"
        "💎 Тариф:\n"
        "1 месяц — 299₽",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handler(message):
    if message.text == "💳 Купить":
        bot.send_message(
            message.chat.id,
            "💳 Оплатите 299₽ и отправьте чек."
        )
    elif message.text == "🛠 Техподдержка":
        bot.send_message(
            message.chat.id,
            "📩 По всем вопросам пишите: @vpotoke013"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Выберите кнопку ниже 👇"
        )

bot.polling()
