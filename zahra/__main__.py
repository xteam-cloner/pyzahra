import asyncio
from kurigram import Client, idle
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

async def start_ubot(data):
    try:
        zahra = Client(
            name=f"zahra_{data['user_id']}",
            api_id=data["api_id"],
            api_hash=data["api_hash"],
            session_string=data["session"],
            plugins=dict(root="plugins"),
            in_memory=True
        )
        await zahra.start()
        
        call = PyTgCalls(zahra)
        await call.start()
        zahra.call = call
        
        print(f"✅ Aktif: {data['user_id']}")
        return zahra
    except Exception as e:
        print(f"❌ Gagal {data['user_id']}: {e}")
        return None

async def runner():
    await app.start()
    async for acc in collection.find({}):
        await start_ubot(acc)
    print("🚀 ZAHRA CORE ONLINE")
    await idle()

if __name__ == "__main__":
    asyncio.run(runner())
    
