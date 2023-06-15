import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os, func

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token="5413986641:AAF0af8LQw_d4YTTvm1HJoZNKY6L1FOouKM")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    cid = message.from_user.id
    if os.path.isdir(f"./users/{cid}") == False:
        os.mkdir(f"./users/{cid}")
    
    await message.answer_photo("https://www.boredpanda.com/blog/wp-content/uploads/2018/04/I-make-everything-alive-again-5ad5baced289b__880.jpg",
    "Hello, I colorize old black and white photos with a set of colors\n\nTry it by sending a photo")



@dp.message_handler(content_types=['photo'])
async def echo_message(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    color = types.InlineKeyboardButton("💡 Colorized", callback_data="color")
    grey = types.InlineKeyboardButton("🔲 Greyscale", callback_data="grey")
    markup.add(color, grey)

    await message.answer_photo(message.photo[-1].file_id, caption="🔸 @iCoderNet", reply_markup=markup)
    

@dp.callback_query_handler()
async def echo_message(query: types.CallbackQuery):
    cid = query.message.from_user.id

    await query.message.photo[-1].download(f"./users/{cid}/input.jpg")
    await query.message.delete()
    if query.data == "color":
        if func.colorized(f"./users/{cid}/input.jpg", f"./users/{cid}/output.jpg")['status'] == 'ok':
            await query.message.answer_photo(open(f"./users/{cid}/output.jpg", 'rb'), caption="🔸 @iCoderNet")
        else:
            await query.message.answer("Error: Try again")

    elif query.data == "grey":
        if func.picGray(f"./users/{cid}/input.jpg", f"./users/{cid}/output.jpg")['status'] == 'ok':
            await query.message.answer_photo(open(f"./users/{cid}/output.jpg", 'rb'), caption="🔸 @iCoderNet")
        else:
            await query.message.answer("Error: Try again")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)