from IstkharMusic import app
import asyncio
import random
from pyrogram import filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant

spam_chats = []

EMOJI = [
    "🦋🦋🦋🦋🦋", "🧚🌸🧋🍬🫖", "🥀🌷🌹🌺💐",
    "🌸🌿💮🌱🌵", "❤️💚💙💜🖤", "💓💕💞💗💖"
]

TAGMES = [
    "𝐇𝐞𝐲 𝐁𝐚𝐛𝐲 𝐊𝐚𝐡𝐚 𝐇𝐨🤗",
    "𝐎𝐲𝐞 𝐎𝐧𝐥𝐢𝐧𝐞 𝐀𝐚𝐨😊",
    "𝐁𝐚𝐭 𝐊𝐚𝐫𝐨 𝐍𝐚🙂",
    "𝐌𝐢𝐬𝐬 𝐘𝐨𝐮🥺",
    "𝐇𝐞𝐥𝐥𝐨 𝐉𝐢😛"
]

def is_admin(member):
    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    )

@app.on_message(filters.command(
    ["tagall", "tag", "etag", "atag", "stag", "utag"]
))
async def mentionall(client, message):
    chat_id = message.chat.id

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("❌ This command only works in groups.")

    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if not is_admin(member):
            return await message.reply("❌ Only admins can use this command.")
    except UserNotParticipant:
        return await message.reply("❌ You are not a member of this group.")

    if chat_id in spam_chats:
        return await message.reply("⚠️ Tagging already running.\nUse /tagoff")

    spam_chats.append(chat_id)

    mode = "text"
    text = None

    if message.reply_to_message:
        mode = "reply"
        text = message.reply_to_message

    try:
        async for user in client.get_chat_members(chat_id):
            if chat_id not in spam_chats:
                break

            if user.user.is_bot:
                continue

            mention = f"[{user.user.first_name}](tg://user?id={user.user.id})"

            if mode == "reply":
                await text.reply(mention)
            else:
                msg = f"{mention} {random.choice(TAGMES)}"
                await client.send_message(chat_id, msg)

            await asyncio.sleep(3)

    finally:
        if chat_id in spam_chats:
            spam_chats.remove(chat_id)

@app.on_message(filters.command(["tagoff", "tagstop"]))
async def cancel_tag(client, message):
    chat_id = message.chat.id

    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if not is_admin(member):
            return await message.reply("❌ Only admins can stop tagging.")
    except UserNotParticipant:
        return await message.reply("❌ You are not a member.")

    if chat_id not in spam_chats:
        return await message.reply("ℹ️ No tag process running.")

    spam_chats.remove(chat_id)
    await message.reply("🛑 **Tagging Stopped Successfully**")
