import asyncio
from kurigram import Client, filters, idle
from pytgcalls import PyTgCalls
from .config import Config
from .database import collection

app = Client("zahra", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

async def start_ubot(data):
    zahra = Client(
        name=f"zahra{data['user_id']}",
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
    return zahra

async def runner():
    await app.start()
    async for acc in collection.find({}):
        await start_ubot(acc)
    print("🚀 CORE ONLINE")
    await idle()  
