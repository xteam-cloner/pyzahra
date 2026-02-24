import asyncio
from pyrogram import Client, idle
from pytgcalls import PyTgCalls
from .config import Config
from .database import collection

app = Client(
    "zahra", 
    api_id=Config.API_ID, 
    api_hash=Config.API_HASH, 
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

async def send_log(text):
    try:
        await app.send_message(Config.LOG_ID, text)
    except Exception as e:
        print(f"Gagal kirim log: {e}")

async def start_ubot(data):
    try:
        zahra_ub = Client(
            name=f"zahra_{data['user_id']}",
            api_id=data["api_id"],
            api_hash=data["api_hash"],
            session_string=data["session"],
            plugins=dict(root="plugins"),
            in_memory=True
        )
        await zahra_ub.start()
        
        call = PyTgCalls(zahra_ub)
        await call.start()
        zahra_ub.call = call
        
        await send_log(f"✅ **Userbot Aktif**\nID: `{data['user_id']}`")
        return zahra_ub
    except Exception as e:
        await send_log(f"❌ **Gagal Login**\nID: `{data['user_id']}`\nError: `{e}`")
        return None

async def runner():
    try:
        await app.start()
        async for acc in collection.find({}):
            await start_ubot(acc)
        
        await send_log("🚀 **Zahra Core Online**\nSemua sistem telah dimuat.")
        print("🚀 ZAHRA CORE IS RUNNING")
        await idle()
    except Exception as e:
        print(f"❌ Error saat menjalankan core: {e}")
    finally:
        # Menutup semua koneksi saat bot mati
        await app.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(runner())
    except KeyboardInterrupt:
        print("\nSistem dimatikan oleh pengguna.")
    finally:
        loop.close()
