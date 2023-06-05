# (c) @TheLx0980

from wroxen.database import channels_collection, get_caption

def get_channel_info(user_id):
    channel_doc = channels_collection.find_one({"user_id": user_id})
    if channel_doc:
        channel_id = channel_doc["channel_id"]
        caption = get_caption(user_id, channel_id)
        return channel_id, caption
    return None, None
