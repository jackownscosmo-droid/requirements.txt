import os
import time
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import Message
from gtts import gTTS

# --- 1. RENDER WEB SERVER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "KrishSlayin Userbot Status: ONLINE"

def run_flask():
    # Render default port 10000 or PORT env variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- 2. BOT CONFIGURATION & ENV CHECK ---
API_ID_RAW = os.environ.get("API_ID", "")
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

if not API_ID_RAW or not API_HASH or not SESSION_STRING:
    print("❌ ERROR: Environment Variables (API_ID, API_HASH, SESSION_STRING) missing hain!")

API_ID = int(API_ID_RAW) if API_ID_RAW.isdigit() else 0

bot = Client(
    "krish_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

PREFIX = "+"
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

@bot.on_message(filters.incoming & ~filters.me, group=1)
async def auto_delete_muted(client, message: Message):
    if message.from_user and message.from_user.id in MUTED_USERS:
        try:
            await message.delete()
        except Exception:
            pass

# --- 4. START PROCESS ---
if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    print("🚀 Web server started on port...")
    try:
        bot.run()
    except Exception as e:
        print(f"❌ CRASH REASON: {e}")
