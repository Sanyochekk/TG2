# from aiogram import Bot, Dispatcher, executor, types
# import aiohttp
# import re
# import json

# token = '6863654909:AAHGcWW2J2YvCl3ZLfWGmKjuybxMDDqBpW4'

# bot = Bot(token=token)
# dp = Dispatcher(bot)

# async def download(url):
#     async with aiohttp.ClientSession() as session:
#         request_url = f'https://api.douyin.wtf/api?url={url}'
#         async with session.get(request_url) as response:
#             if response.status == 200:
#                 data = await response.text()
#                 print(data)  # Выводим содержимое ответа для диагностики
#                 try:
#                     json_data = response.json(content_type=None)
#                     video = json_data['video_data']['nwm_video_url_HQ']
#                     return video
#                 except json.JSONDecodeError as e:
#                     print(f"Ошибка декодирования JSON: {e}")
#                     return None
#             else:
#                 print(f"Ошибка запроса: {response.status}")
#                 return None

# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     await message.reply('Привет! Чтобы скачать видео, просто отправь на него видео.')

# @dp.message_handler()
# async def process(message: types.Message):
#     if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
#         m = await message.reply('Ожидайте..')
#         video = await download(message.text)
#         await bot.delete_message(message.chat.id, m['message_id'])
#         await message.answer_video(video, caption=f'Готово!')

# if __name__ == "__main__":
#     executor.start_polling(dp)

from aiogram import Bot, Dispatcher, executor, types
import aiohttp
import re
import os

token = '6863654909:AAHGcWW2J2YvCl3ZLfWGmKjuybxMDDqBpW4'

bot = Bot(token=token)
dp = Dispatcher(bot)

async def download(url):
    async with aiohttp.ClientSession() as session:
        request_url = f'https://api.douyin.wtf/api?url={url}'
        async with session.get(request_url) as response:
            if response.status == 200:
                data = await response.read()
                return data
            else:
                print(f"Ошибка запроса: {response.status}")
                return None

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет! Чтобы скачать видео, просто отправь на него видео.')

@dp.message_handler()
async def process(message: types.Message):
    if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
        m = await message.reply('Ожидайте..')
        video_data = await download(message.text)
        if video_data:
            video_file_name = 'video.mp4'
            with open(video_file_name, 'wb') as video_file:
                video_file.write(video_data)
            await bot.delete_message(message.chat.id, m.message_id)
            await message.answer_video(types.InputFile(video_file_name), caption='Готово!')
            os.remove(video_file_name)
        else:
            await bot.delete_message(message.chat.id, m.message_id)
            await message.reply('Ошибка при загрузке видео.')

if __name__ == "__main__":
    executor.start_polling(dp)
