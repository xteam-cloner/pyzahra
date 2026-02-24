import asyncio
import os
from pyrogram import Client, idle
from pytgcalls import PyTgCalls
from .config import Config
from .database import collection

def get_plugins():
    plugin_list = []
    if os.path.exists("plugins"):
        for file in os.listdir("plugins"):
            if file.endswith(".py") and not file.startswith("__"):
                plugin_list.append(file[:-3])
    return plugin_list

app = Client(
    "zahra", 
    api_id=Config.API_ID, 
    api_hash=Config.API_HASH, 
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

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
        
        print(f"OK: {data['user_id']}")
        return zahra_ub
    except Exception as e:
        print(f"ERR: {data['user_id']} | {e}")
        return None

async def runner():
    plugins = get_plugins()
    for p in plugins:
        print(f"LOAD: {p}")
    
    await app.start()
    async for acc in collection.find({}):
        await start_ubot(acc)
        
    print(f"ONLINE | PLUGINS: {len(plugins)}")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(runner())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
    
