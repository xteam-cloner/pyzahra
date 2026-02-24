from pyrogram import filters, Client

@Client.on_message(filters.command("ping", ".") & filters.me)
async def ping_ubot(client, message):
    await message.edit("PONG! Userbot Aktif 🔥")
  
