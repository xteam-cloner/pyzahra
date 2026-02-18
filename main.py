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
    # Menggunakan builder agar tata letak tombol rapi
    builder = ReplyKeyboardBuilder()
    
    # Tombol pertama (Baris 1): Putar Musik (Biru) & Hentikan (Merah)
    builder.row(
        types.KeyboardButton(text="Putar Musik", style="primary"),
        types.KeyboardButton(text="Hentikan", style="danger")
    )
    
    # Tombol kedua (Baris 2): Bantuan (Hijau)
    builder.row(
        types.KeyboardButton(text="Bantuan & FAQ", style="success")
    )
    
    # Pesan respon
    text = f"Halo {html.bold(message.from_user.full_name)}!\n"
    if message.chat.type in ["group", "supergroup"]:
        text += f"Selamat datang di grup {html.bold(message.chat.title)}. Menu musik sudah siap!"
    else:
        text += "Silakan pilih menu berwarna di bawah untuk kontrol musik:"

    # Kirim pesan dengan keyboard yang warnanya dipertahankan
    await message.answer(
        text,
        reply_markup=builder.as_markup(resize_keyboard=True)
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
  
