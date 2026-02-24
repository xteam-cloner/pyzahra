import asyncio
from kurigram import Client, filters, errors
from kurigram.types import InlineKeyboardMarkup, InlineKeyboardButton
from kuricore.config import Config
from kuricore.database import collection

user_temp = {}

async def finalize_login(client, uid):
    data = user_temp[uid]
    session_str = await data["cli"].export_session_string()
    
    payload = {
        "user_id": uid,
        "api_id": Config.API_ID,
        "api_hash": Config.API_HASH,
        "session": session_str
    }
    
    await collection.update_one({"user_id": uid}, {"$set": payload}, upsert=True)
    await client.send_message(uid, "✅ **Login Berhasil!**\nSesi Anda telah disimpan.")
    
    await data["cli"].disconnect()
    if uid in user_temp:
        del user_temp[uid]

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    if not client.me.is_bot: return 
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Tambah Akun", callback_data="add_ubot")],
        [InlineKeyboardButton("🗑 Hapus Akun", callback_data="del_ubot")]
    ])
    
    await message.reply(
        f"👋 Halo **{message.from_user.first_name}**\n\nBot Manager aktif.",
        reply_markup=buttons
    )

@Client.on_callback_query(filters.regex("add_ubot"))
async def add_ubot_cb(client, cb):
    if not client.me.is_bot: return
    
    uid = cb.from_user.id
    user_temp[uid] = {"step": "phone"}
    
    await cb.message.edit(
        "📱 **Input Nomor Telepon**\n\nFormat: `+62812345678`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Batal", callback_data="cancel")]])
    )

@Client.on_message(filters.text & filters.private)
async def login_flow_handler(client, message):
    if not client.me.is_bot: return
    
    uid = message.chat.id
    if uid not in user_temp: return
    
    step = user_temp[uid]["step"]
    input_text = message.text.strip()

    try:
        if step == "phone":
            temp_cli = Client(
                f"temp_{uid}", 
                api_id=Config.API_ID, 
                api_hash=Config.API_HASH, 
                in_memory=True
            )
            await temp_cli.connect()
            
            sent_code = await temp_cli.send_code(input_text.replace(" ", ""))
            
            user_temp[uid].update({
                "cli": temp_cli,
                "phone": input_text,
                "hash": sent_code.phone_code_hash,
                "step": "otp"
            })
            
            await message.reply("📩 **Kode OTP Terkirim**")

        elif step == "otp":
            otp_code = input_text.replace(" ", "")
            data = user_temp[uid]
            
            try:
                await data["cli"].sign_in(data["phone"], data["hash"], otp_code)
                await finalize_login(client, uid)
            except errors.SessionPasswordNeeded:
                user_temp[uid]["step"] = "2fa"
                await message.reply("🔐 **2-Step Verification**")
            except errors.PhoneCodeInvalid:
                await message.reply("❌ Kode OTP salah.")

        elif step == "2fa":
            data = user_temp[uid]
            try:
                await data["cli"].check_password(input_text)
                await finalize_login(client, uid)
            except errors.PasswordHashInvalid:
                await message.reply("❌ Password salah.")

    except Exception as e:
        await message.reply(f"⚠️ **Error:** `{str(e)}`")
        if uid in user_temp:
            del user_temp[uid]

@Client.on_callback_query(filters.regex("cancel"))
async def cancel_cb(client, cb):
    uid = cb.from_user.id
    if uid in user_temp:
        if "cli" in user_temp[uid]:
            await user_temp[uid]["cli"].disconnect()
        del user_temp[uid]
    await cb.message.edit("❌ Dibatalkan.")
  
