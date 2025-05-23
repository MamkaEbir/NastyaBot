import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.client.default import DefaultBotProperties
from pytz import timezone


# 🔐 Токен и ID Насти
BOT_TOKEN = "7551500537:AAHXDafFbKUPf_WSTFP2GrN5LZCfbLuq7yc"
NASTYA_CHAT_ID = 813196147

# Инициализация бота и диспетчера
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="мне грустно 😢"), KeyboardButton(text="мне весело 😊")],
        [KeyboardButton(text="мне одиноко 🏠"), KeyboardButton(text="заебла эта учёба 📚")],
    ],
    resize_keyboard=True
)

# Список пожеланий
morning_wishes = [
    "Доброе утро, Настенька! 🌞 Пусть этот день принесёт тебе улыбки, лёгкость и капельку волшебства!",
    "Просыпайся, Настя! ☀️ Сегодня — идеальный день для маленьких радостей и больших свершений!",
    "Доброе утро, Настя! 💖 Пусть всё сложится именно так, как ты захочешь, а день будет добрым и светлым!",
    "Насть, доброе утро! 🌸 Пусть сегодня тебя ждёт что-то прекрасное и волшебное",
    "Доброе утро, Настя! 🌈 Пусть день будет таким же ярким, как твои глаза, и таким же тёплым, как твоё сердце!",
    "Проснись и улыбнись! 😊 Сегодняшний день создан для счастья — не упусти его!",
    "Настенька, доброе утро! 🌹 Пусть сегодня всё получается легко, а любая грусть растворяется в твоей улыбке!",
    "Утро началось, а значит, где-то рядом уже ждёт что-то хорошее! ✨ Держи хвост пистолетом, красавица!",
    "Доброе утро, Настя! 🐇 Пусть день будет наполнен приятными моментами, а все тревоги обойдут тебя стороной!",
    "Солнце светит специально для тебя! ☀️💛 Пусть этот день подарит тебе вдохновение и сотню поводов для радости!"
]

# Функция для утреннего сообщения — выбирает случайное пожелание
async def send_morning():
    try:
        wish = random.choice(morning_wishes)
        await bot.send_message(NASTYA_CHAT_ID, wish)
    except Exception as e:
        print(f"Ошибка при отправке утреннего сообщения: {e}")

# Дневное сообщение в 16:00
async def send_afternoon():
    try:
        await bot.send_message(NASTYA_CHAT_ID, "Настя, привет, какое у тебя сегодня настроение?🌸")
    except Exception as e:
        print(f"Ошибка при отправке дневного сообщения: {e}")


# Настройка планировщика с московским временем
def setup_scheduler():
    moscow_tz = timezone('Europe/Moscow')
    scheduler = AsyncIOScheduler(timezone=moscow_tz)
    scheduler.add_job(send_morning, trigger='cron', hour=10, minute=0)
    scheduler.add_job(send_afternoon, trigger='cron', hour=16, minute=0)
    scheduler.start()

# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет, Настя! Какое у тебя сегодня настроение?🌸", reply_markup=keyboard)

# Обработка нажатий на кнопки
@dp.message()
async def handle_buttons(message: types.Message):
    text = message.text.lower().strip()

    folders = {
        "мне грустно 😢": "media/sad",
        "мне весело 😊": "media/happy",
        "мне одиноко 🏠": "media/lonely",
        "заебла эта учёба 📚": "media/busy"
    }

    if text in folders:
        folder = folders[text]
        if not os.path.exists(folder):
            await message.answer("Насть, папка с изображениями не найдена 😢, скажи Грише, он скоро всё исправит")
            return

        images = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        if images:
            path = os.path.join(folder, random.choice(images))
            photo = FSInputFile(path)
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
        else:
            await message.answer("Насть, пока нет изображений в этой категории 🥺, скажи Грише, он скоро всё исправит")
    else:
        await message.answer("Насть, какое у тебя настроение сегодня?😊")

# Основной запуск
async def main():
    setup_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
