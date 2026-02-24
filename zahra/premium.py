from zahra.database import mongodb

user = mongodb.premium

async def get_prem():
    prem = await user.find_one({"prem": "prem"})
    if not prem:
        return []
    return prem.get("list", [])

async def add_prem(user_id):
    try:
        await user.update_one(
            {"prem": "prem"}, 
            {"$addToSet": {"list": user_id}}, 
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Error add_prem: {e}")
        return False

async def remove_prem(user_id):
    try:
        res = await user.update_one(
            {"prem": "prem"}, 
            {"$pull": {"list": user_id}}
        )
        return res.modified_count > 0
    except Exception as e:
        print(f"Error remove_prem: {e}")
        return False
      
