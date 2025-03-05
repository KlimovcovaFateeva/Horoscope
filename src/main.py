import random
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from functools import partial


# Твой токен от BotFather
TOKEN = "7688416796:AAF7wM1cF-BPilUXuTtg2anZEGdx5v99ZEQ"

async def start(update: Update, context: CallbackContext):
    #Приветствие бота
    await update.message.reply_text(
        "Привет! Отправь мне свой знак зодиака и число дня месяца(например: Овен 5), и я дам тебе совет на день."
    )

async def get_horoscope(update: Update, context: CallbackContext, horoscopes):
    #Обработка входящих сообщений
    text = update.message.text.split()
    if len(text) < 2:
        await update.message.reply_text("Пожалуйста, введите знак зодиака и число дня месяца(например: Лев 12).")
        return

    sign = text[0].capitalize()
    day = text[1].capitalize()
    if sign not in horoscopes:
        await update.message.reply_text("Такого знака зодиака нет! Попробуйте снова.")
        return
    if day not in horoscopes[sign]:
        await update.message.reply_text("Введите число от 1 до 31! Попробуйте снова.")
        return

    advice = random.choice(horoscopes[sign][day])
    await update.message.reply_text(f"Твой совет на день: {advice}")

def main():
    #Загрузка подготовленных советов
    with open('../datasets/horoscopes.json', 'r', encoding='utf-8') as file:
      horoscopes = json.load(file)

    #Запуск бота
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, partial(get_horoscope, horoscopes=horoscopes)))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()