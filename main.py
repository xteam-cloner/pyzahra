import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Masukkan Token Anda di sini
TOKEN = "8392450438:AAF8GuDJjAkW7c9ePLLkHXFDKshP4RfndSI"

dp = Dispatcher()

# Handler untuk perintah /start

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # Membuat tombol
    kb = [
        [
            InlineKeyboardButton(text="Cek Profil", callback_data="view_profile"),
            InlineKeyboardButton(text="Bantuan", callback_data="help_info")
        ],
        [InlineKeyboardButton(text="Kunjungi Website", url="https://google.com")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(
        f"Halo, {html.bold(message.from_user.full_name)}!\nApa yang ingin kamu lakukan hari ini?",
        reply_markup=keyboard
    )

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
  
