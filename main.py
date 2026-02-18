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
    builder = InlineKeyboardBuilder()
    
    # Baris 1: Tombol lebar dengan Custom Emoji
    builder.row(
        types.InlineKeyboardButton(
            text="✨ ADD ME TO YOUR GROUP ✨",
            url="https://t.me/xtbot?startgroup=true"
        )
    )
    
    # Baris 2: Tombol Berwarna (Menggunakan Hex Color)
    builder.row(
        types.InlineKeyboardButton(
            text="⚙️ Settings", 
            callback_data="settings",
            background_color=0x3399FF  # Warna Biru (Primary)
        ),
        types.InlineKeyboardButton(
            text="📦 Module", 
            callback_data="module",
            background_color=0x7F7F7F  # Warna Abu-abu
        )
    )
    
    # Baris 3: Tombol Putar & Hentikan dengan warna kontras
    builder.row(
        types.InlineKeyboardButton(
            text="▶️ Putar Musik", 
            callback_data="play_music",
            background_color=0x00CC66  # Warna Hijau (Success)
        ),
        types.InlineKeyboardButton(
            text="⏹ Hentikan", 
            callback_data="stop_music",
            background_color=0xFF3333  # Warna Merah (Danger)
        )
    )

    await message.answer(
        f"Hey {html.bold(message.from_user.full_name)}. Please browse through the options 👇",
        reply_markup=builder.as_markup()
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
  
