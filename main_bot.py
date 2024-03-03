from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile, CallbackQuery
from aiogram.enums import ParseMode
from io import BytesIO
import logging
import sys
import asyncio
from pytube import YouTube
from config import *
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет, я умею скачивать видео с YouTube! Скинь ссылку.")

@dp.message(lambda message: message.text.startswith(("https://www.youtube.com/", "https://youtu.be/")))
async def handle_youtube_link(message: types.Message):
    if message.text.startswith(("https://www.youtube.com/", "https://youtu.be/")):
        print('ok')
        markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Видео💻", callback_data="Видео💻"),
            InlineKeyboardButton(text="Аудио🔊", callback_data="Аудио🔊")
        ]])
        await message.answer(message.text, reply_markup=markup)

@dp.callback_query()
async def callback_handler(query: CallbackQuery):
    if query.data == "Видео💻":
        await download_youtube_video(query.message, query.message.text)
    if query.data == "Аудио🔊":
        await download_youtube_audio(query.message, query.message.text)

async def download_youtube_video(message: Message, url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
        buffer = BytesIO()
        stream.stream_to_buffer(buffer)
        file = BufferedInputFile(buffer.getvalue(), filename=f"{yt.title}.mp4")
        await message.answer_video(file)
    except Exception as e:
        await message.answer(f"Ошибка при скачивании или отправке видео: {str(e)}")

async def download_youtube_audio(message: Message, url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        buffer = BytesIO()
        stream.stream_to_buffer(buffer)
        file = BufferedInputFile(buffer.getvalue(), filename=f"{yt.title}.mp3")
        await message.answer_audio(file)
    except Exception as e:
        await message.answer(f"Ошибка при скачивании или отправке видео: {str(e)}")

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())