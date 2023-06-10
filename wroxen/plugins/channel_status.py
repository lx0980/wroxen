# (c) @TheLx0980

from wroxen.database.authorized_chat import get_authorized_channels, add_authorized_channel, delete_authorized_channel, \
   delete_all_authorized_chats, get_authorized_chat
from wroxen.database.caption_db import get_forward_settings, get_replace_data
from pyrogram import Client, filters
from wroxen.vars import ADMIN_IDS

AUTHORIZED_CHANL = get_authorized_channels()

@Client.on_message(filters.command("Channel_status") & filters.channel)
async def channel_status_command(bot, message):
    channel_id = str(message.chat.id)
    forward_settings = get_forward_settings(channel_id)
    if forward_settings:
        from_chat = forward_settings["from_chat"]
        to_chat = forward_settings["to_chat"]
        old_username, new_username, caption = get_replace_data(channel_id)
        await bot.send_message(message.chat.id, f"New Username: {new_username} 🖐️")
        channel_status_text = f"""
From Channel: {from_chat}
To chat: {to_chat}
        
Caption: {caption}
        
Replace TEXT:
{old_username} To {new_username}

Channel name: {message.chat.title}"""

        await bot.send_message(message.chat.id, channel_status_text)
    else:
        await bot.send_message(message.chat.id, f"Forward settings not found for Channel ID {channel_id}")


        

@Client.on_message(filters.command("add_authorised_chat"))
async def add_authorised_chat_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("You are not an authorized user to execute this command.")
        return

    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/add_authorised_chat {channel_id}`.")
        return

    channel_id = command_parts[1]

    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id

    if channel_id in AUTHORIZED_CHANL:
        await message.reply("Channel ID is already authorized.")
        return

    try:
        add_authorized_channel(channel_id)
        await message.reply(f"Channel ID {channel_id} added to authorized list.")
    except Exception as e:
        await message.reply("An error occurred while adding the channel ID to the authorized list.")

@Client.on_message(filters.command("delete_authorised_chat"))
async def delete_authorised_chat_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("You are not an authorized user to execute this command.")
        return

    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/delete_authorised_chat {channel_id}`.")
        return

    channel_id = command_parts[1]

    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id

    try:
        delete_authorized_channel(channel_id)
        await message.reply(f"Channel ID {channel_id} removed from authorized list.")
    except Exception as e:
        await message.reply("An error occurred while removing the channel ID from the authorized list.")

@Client.on_message(filters.command("delete_all_authorised_chats"))
async def delete_all_authorised_chats_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("You are not an authorized user to execute this command.")
        return

    try:
        deleted_count = delete_all_authorized_chats()
        await message.reply(f"{deleted_count} authorized chats have been deleted.")
    except Exception as e:
        await message.reply("An error occurred while deleting the authorized chats.")
        
        
        
@Client.on_message(filters.command("check_authorised"))
async def check_authorised_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("You are not an authorized user to execute this command.")
        return

    try:
        authorised_chats = get_authorized_chat()
        if not authorised_chats:
            await message.reply("No authorized chats found.")
        else:
            reply_message = "Authorized Chats:\n"
            for chat_id in authorised_chats:
                reply_message += f"- {chat_id}\n"
            await message.reply(reply_message)
    except Exception as e:
        await message.reply("An error occurred while checking the authorized chats.")

        
        
