import os
import time
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import Message
from gtts import gTTS

# --- 1. RENDER WEB SERVER (KEEPALIVE) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "KrishSlayin Userbot Status: ACTIVE"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- 2. BOT CONFIGURATION ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

bot = Client("krish_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
PREFIX = "+"

# Global Storage
MUTED_USERS = set()

# --- 3. COMMAND HANDLERS ---

@bot.on_message(filters.me & filters.command("ping", prefixes=PREFIX))
async def ping_handler(client, message: Message):
    start = time.time()
    reply = await message.edit_text("⚡ Ping Check...")
    end = time.time()
    ms = round((end - start) * 1000, 2)
    await reply.edit_text(f"🏓 **Pong!**\n⚡ Latency: `{ms}ms`")

@bot.on_message(filters.me & filters.command("getid", prefixes=PREFIX))
async def getid_handler(client, message: Message):
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        await message.edit_text(f"👤 **User ID:** `{target_id}`\n💬 **Chat ID:** `{message.chat.id}`")
    else:
        await message.edit_text(f"💬 **Chat ID:** `{message.chat.id}`\n👤 **Your ID:** `{message.from_user.id}`")

@bot.on_message(filters.me & filters.command("status", prefixes=PREFIX))
async def status_handler(client, message: Message):
    await message.edit_text("⚙️ **Cluster Telemetry:**\n• Status: `Online`\n• Host: `Render Cloud`\n• Engine: `Pyrogram MTProto`")

@bot.on_message(filters.me & filters.command("clean", prefixes=PREFIX))
async def clean_handler(client, message: Message):
    args = message.text.split()
    count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 10
    await message.delete()
    async for msg in client.get_chat_history(message.chat.id, limit=count):
        if msg.from_user and msg.from_user.is_self:
            try:
                await msg.delete()
            except Exception:
                pass

@bot.on_message(filters.me & filters.command("tts", prefixes=PREFIX))
async def tts_handler(client, message: Message):
    text = message.text.split(maxsplit=1)
    if len(text) < 2 and not message.reply_to_message:
        return await message.edit_text("❌ Type text or reply to a message!")
    
    target_text = text[1] if len(text) > 1 else message.reply_to_message.text
    await message.edit_text("🎙️ Generating Voice Note...")
    tts = gTTS(text=target_text, lang='hi')
    filename = "tts.ogg"
    tts.save(filename)
    await message.delete()
    await client.send_audio(message.chat.id, filename)
    if os.path.exists(filename):
        os.remove(filename)

@bot.on_message(filters.me & filters.command("mute", prefixes=PREFIX))
async def mute_handler(client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        MUTED_USERS.add(user_id)
        await message.edit_text(f"🤐 Target `{user_id}` shadow-muted.")
    else:
        await message.edit_text("❌ Reply to a user to mute.")

@bot.on_message(filters.me & filters.command("unmute", prefixes=PREFIX))
async def unmute_handler(client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        MUTED_USERS.discard(user_id)
        await message.edit_text(f"🔊 Target `{user_id}` unmuted.")
    else:
        await message.edit_text("❌ Reply to a user to unmute.")

@bot.on_message(filters.me & filters.command("leave", prefixes=PREFIX))
async def leave_handler(client, message: Message):
    await message.edit_text("👋 Leaving Chat...")
    await client.leave_chat(message.chat.id)

# Auto-delete messages from Muted Users (Shadow Mute Logic)
@bot.on_message(filters.incoming & ~filters.me, group=1)
async def auto_delete_muted(client, message: Message):
    if message.from_user and message.from_user.id in MUTED_USERS:
        try:
            await message.delete()
        except Exception:
            pass

# --- 4. START PROCESS ---
if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.run()
