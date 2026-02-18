import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
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
    # Menggunakan ReplyKeyboardBuilder untuk fleksibilitas
    builder = ReplyKeyboardBuilder()
    
    # Menambahkan tombol dengan gaya warna (style) dan custom emoji
    builder.row(
        types.KeyboardButton(
            text="Putar Musik", 
            style="primary",  # Warna Biru
            icon_custom_emoji_id="5432109876543210" # Ganti dengan ID emoji aslimu
        ),
        types.KeyboardButton(
            text="Hentikan", 
            style="danger"    # Warna Merah
        )
    )
    
    builder.row(
        types.KeyboardButton(
            text="Bantuan & FAQ", 
            style="success"   # Warna Hijau
        )
    )

    await message.answer(
        f"Halo {message.from_user.first_name}!\nSilakan pilih menu berwarna di bawah:",
        reply_markup=builder.as_markup(resize_keyboard=True)
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
  
