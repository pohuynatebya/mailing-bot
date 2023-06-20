import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '5802664997:AAH4VxEHybKauPOM00JPpDTP1sx6xl8UPXg'  # Замените на свой токен

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для рассылки сообщений с фотографиями.")

@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def process_admin_message(message: types.Message):
    if message.from_user.id == 79616282:  
        caption = message.caption if message.caption else ""
        photo_file_id = message.photo[-1].file_id

        # Разбиваем сообщение на текст и ссылку
        parts = caption.split("|")
        if len(parts) == 2:
            button_text = parts[0].strip()
            button_url = parts[1].strip()

            # Создаем кнопку с текстом и ссылкой
            button = types.InlineKeyboardButton(button_text, url=button_url)
            keyboard = types.InlineKeyboardMarkup().add(button)

            # Получаем список всех подписчиков бота
            subscribers = await bot.get_chat_members(chat_id=message.chat.id)
            for subscriber in subscribers:
                # Отправляем фотографию с подписью и кнопкой каждому подписчику
                await bot.send_photo(
                    subscriber.user.id,
                    photo=photo_file_id,
                    caption=caption,
                    reply_markup=keyboard
                )
        else:
            await message.reply("Некорректный формат сообщения. Пожалуйста, используйте формат: Текст | Ссылка")
    else:
        await message.reply("Вы не являетесь администратором.")


if __name__ == '__main__':
    from aiogram import executor
    print("start")
    executor.start_polling(dp, skip_updates=True)
