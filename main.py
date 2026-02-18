import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Masukkan Token Anda di sini
TOKEN = "8392450438:AAF8GuDJjAkW7c9ePLLkHXFDKshP4RfndSI"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    # Membuat keyboard secara manual tanpa Builder
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="▶️ Putar Musik", 
                    callback_data="play",
                    background_color=0x00CC66  # Hijau (API 9.4)
                ),
                InlineKeyboardButton(
                    text="⏹ Hentikan", 
                    callback_data="stop",
                    background_color=0xFF3333  # Merah (API 9.4)
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ ADD ME TO YOUR GROUP ✨", 
                    url=f"https://t.me/{(await Bot.get_me()).username}?startgroup=true"
                )
            ]
        ]
    )

    await message.answer(
        f"Halo {html.bold(message.from_user.full_name)}!\nSilakan pilih menu musik di bawah:",
        reply_markup=keyboard
    )
    
    

# Handler agar tombol "Putar Musik" berfungsi saat ditekan di grup
@dp.message(F.text == "Putar Musik")
async def music_guide(message: types.Message):
    await message.reply("Ketik `/play [judul lagu]` untuk memutar musik di Voice Chat!")
    
    

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        # Mengirim kembali pesan yang sama
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Wah, aku tidak mengerti tipe pesan itu!")

async def main() -> None:
    # Inisialisasi Bot
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # Jalankan polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
  
