# -*- coding: utf-8 -*-
import os
import time
import random
import asyncio
import logging
import sys

# Windows aur kuch terminals mein output force UTF-8 karne ke liye
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Global Configuration for Userbot
API_ID = int(os.environ.get("API_ID", "0"))  # Apni API ID environment variable se lein
API_HASH = os.environ.get("API_HASH", "")    # Apna API Hash environment variable se lein
SESSION_STRING = os.environ.get("SESSION_STRING", "") # Railway/Hosting k liye session string

OWNER_ID = int(os.environ.get("OWNER_ID", "8821066459"))
LOG_CHANNEL_ID = os.environ.get("LOG_CHANNEL_ID", None)

AUTHORIZED_ADMINS = set([8821066459, OWNER_ID])
GBANNED_USERS = set()
CHAT_TASKS = {}

# Global Reaction State across chat instances
GLOBAL_CHAT_REACT_MODE = {}
REACTION_EMOJI = "🤣"

# --- 15 Lines Target Array ---
TARGET_15_LINES = [
    "Clap करो रंडीबाले ne joke mara h 😂👋🏻😂👋🏻😂👋🏻😂👋🏻😂👋🏻😂👋🏻",
    "चलेगी toh teri लंगड़ी maa 😁🔥😂👋🏻😂😂🔥🔥",
    "तेरी maa rundy 😜🙀⚡तेरी maa rundy 😜🙀⚡",
    "Oye message mat kar warna ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅ dunga🤣🤣",
    "अच्छा teri maa के बूब्स पे green veins h इसलिए tu itna खिलसता h 😂👏🏻",
    "𝐄ɴᴛʀʏ 𝐋ᴇʟɪ 𝐓ᴏ 𝐀sᴍᴀɴ 𝐊ɪ 𝐔ᴄʜᴀɪᴏ 𝐏ᴇ 𝐓ᴇʀɪ 𝐌ᴀ 𝐂ʜᴜᴅᴇɢɪ / 🌘🕊️",
    "Teri Maa Ko Football ⚽ bnake uske 𝗕𝗛😈𝗦𝗗𝗘 पे laat 🦶🏻 marunga 🤩🔥",
    "Tri maa ke bosde pr jcb se khudai krwa duga rndyke😂😂🤟💥💥🤟",
    "Le धमाकेदार mukka kha रन्डी ke चाइल्ड 👊🏻👊🏻👊🏻🤣🤣",
    "चाल चल teri chudai डॉन hogyi !! Ab teri लंगड़ी maa दौड़ेगी 😂👋🏻",
    "subha ho ya sham chudte rhena hai tera kaam😂🔥😂🔥😂🔥",
    "randy pane me to teri ma aval darje ki hakdaar he😁👍😁👍😁👍😁👍",
    "𝘿𝙃𝘼𝙏 ʳⁿᵈⁱᵏᵉʸ 🤦🏿‍♂️💢𝘿𝙃𝘼𝙏 ʳⁿᵈⁱᵏᵉʸ 🤦🏿‍♂️💢",
    "ᗷᑌᖇ ᗪᗴᗪO Tᑌᕼᗩᖇ ᗰᗩIYᗩ Kᗴ 😂💔🤤🫦👅🤡",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐂ʜᴜᴅᴋᴇ 𝐁ʜᴀᴀɢ 𝐑ᴀʜɪ -> 🏃🏻‍♀️🔥🤸🏻‍♀️🔥🏃🏻‍♀️🔥🤸🏻‍♀️🔥"
]

AUTOREPLY_LINES = [
    r"""बड़े दुःख के साथ हँसना पढ़ रहा है😂  𝐓ᴜ तेरी माँ रंडी 🤍😅🔥""",
    r"""𝙏𝙚𝙧𝙞 𝙢𝙖𝙖 𝙠𝙚 𝙝𝙤𝙨𝙙𝙚 𝙢𝙚 𝙡𝙖𝙩 𝙥𝙙𝙚𝙣𝙜𝙚 𝙗𝙝𝙤𝙩 𝙩𝙚𝙯 👻 😂👯😂👯😂👯""",
    r"""𝙏𝙀𝙍𝙄 𝙈𝘼 𝑑𝙄𝘿🇭🇻𝘼 𝙋𝙀𝙉𝙎𝙄𝙊𝙉 𝙃𝘼𝙉𝙀 𝙒𝘼𝙇𝙄 𝙍𝙉𝘿𝙄 🤣""",
    r"""तेरी maa की chut में ऐसा HACK lgaunga Light की speed में बच्चे देगी""",
    r"""𝑩𝑯𝑨𝑮 𝑹𝑨𝑵𝑫𝒀𝑲𝑬 𝑻𝑬𝑹𝑰 𝑴𝑨 𝑪𝑯𝑼𝑫𝑹𝑰 𝑯𝑨𝑰 ᯓ🏃🏻‍♀️‍➡️ᯓ🏃🏻‍♀️‍➡️ᯓ🏃🏻‍♀️‍➡️""",
    r"""𝘽𝙃𝘼𝙂𝘼 𝘽𝙃𝘼𝙂𝘼 𝙆𝙀 𝙈𝘼𝙍𝙐𝙉𝙂𝘼 🤣🩷🙌🏾"""
]

TARGET_LINES = [
    r"""˚∧＿∧   +        — ͟͞͞🥛 (  •‿• )つ  Special attack: teri mummy ka dudh 😂😂""",
    r"""𝙉𝙀𝙆𝘼𝘼𝘼𝙇 𝙈𝘼𝘿𝘼𝘼𝙍𝘾𝙃𝘿👍🏼👍🏼👍🏼👍🏼👍🏼""",
    r"""तेरी बहन का भोसड़ा 😂🤸🏻‍♂️😂🤸🏻‍♂️ 𝘾𝙃𝑼𝙋 𝙍𝙉𝘿𝙄𝙆𝙀"""
]

FLOOD_LINES = [
    r"""𝙏𝙚𝙧𝙞 𝙢𝙖𝙖 𝙠𝙚 𝙗𝙝𝙤𝙨𝙙𝙚 𝙢𝙚 𝙡𝙖𝙩 𝙥𝙙𝙚𝙣𝙜𝙚 𝙗𝙝𝙤𝙩 𝙩𝙚𝙯 👻 😂👯😂👯""",
    r"""तेरो ma ko चोदने k बाद उसको ऐसे चंद सितारए नजर आएंगे""",
    r"""😝 Beta 🥶 लंड 🔥 पकड़ 😡 muh 😜 pe 😁 रगड़ 😂"""
]

ROASTS_HI = [
    "Teri shakal dekh ke Telegram ka server bhi crash ho jaye!",
    "Itna dimaag agar sahi jagah lagaya hota toh aaj NASA me hota!"
]

ROASTS_ENG = [
    "You bring everyone so much joy... when you leave the room!",
    "Your brain is like the 404 error page—permanently missing content."
]

VALID_COMMANDS = {
    "start", "menu", "panel", "gcnc", "vgcnc", "stopgcnc",
    "target", "vtarget", "stoptarget", "spam", "stopspam",
    "flood", "vflood", "stopflood", "gcpfp", "stopgcpfp",
    "voiceflood", "stopvoiceflood", "mute", "unmute", "mutelist",
    "stripmedia", "stopstripmedia", "pfpstripper", "autoreply",
    "vautoreply", "stopautoreply", "reptts", "stopreptts",
    "clean", "togglereactall", "togglereact", "stopall",
    "scan", "ping", "getid", "status", "omg", "tts", 
    "ttshi", "ttsen", "ttsjap", "ttsgerman", 
    "roasthi", "roasteng", "cluster", "broadcast",
    "slayinpowergifted", "slayinpowertaken", "slayinfor",
    "gban", "ungban", "ht", "leave"
}

def get_chat_data(chat_id):
    if chat_id not in CHAT_TASKS:
        CHAT_TASKS[chat_id] = {
            "tasks": {},
            "muted": set(),
            "stripmedia": set(),
            "pfpstripper": False,
            "autoreply": {},
            "reptts": set(),
            "vtarget_trap": {}
        }
    return CHAT_TASKS[chat_id]

def is_admin(user_id):
    return user_id in AUTHORIZED_ADMINS or user_id == OWNER_ID

async def send_log(client, text: str):
    if LOG_CHANNEL_ID:
        try:
            await client.send_message(chat_id=int(LOG_CHANNEL_ID), text=text, parse_mode="markdown")
        except Exception as e:
            logging.error(f"Failed to send log: {e}")

async def hard_stop_all(chat_id: int, client, user_id: int):
    chat_data = get_chat_data(chat_id)
    
    for task_name, task in list(chat_data["tasks"].items()):
        task.cancel()
    chat_data["tasks"].clear()

    chat_data["muted"].clear()
    chat_data["stripmedia"].clear()
    chat_data["autoreply"].clear()
    chat_data["reptts"].clear()
    chat_data["vtarget_trap"].clear()
    chat_data["pfpstripper"] = False
    GLOBAL_CHAT_REACT_MODE[chat_id] = None

    await send_log(client, f"🚨 *ABSOLUTE KILL SWITCH TRIGGERED*\nChat: `{chat_id}`\nAdmin/User: `{user_id}`")

# --- UI Helpers (1-Page Menu) ---

def get_single_page_menu_keyboard():
    buttons = [
        [
            InlineKeyboardButton("⚔️ Combat", callback_data="menu_combat"),
            InlineKeyboardButton("🎯 Targets", callback_data="menu_targets")
        ],
        [
            InlineKeyboardButton("🛡️ Tools & Blackout", callback_data="menu_tools"),
            InlineKeyboardButton("🎛️ Owner Controls", callback_data="menu_owner")
        ],
        [InlineKeyboardButton("🚨 Stop All Tasks", callback_data="stop_all")],
        [InlineKeyboardButton("❌ Close Menu", callback_data="menu_close")]
    ]
    return InlineKeyboardMarkup(buttons)

def get_single_page_menu_text():
    return (
        "⚡ **KRISHSLAYIN USERBOT CONTROL HUB** ✝️\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ **Status:** Active & Ready (Userbot Mode)\n"
        "🛡️ **Prefix:** `.` (Dot commands)\n\n"
        "Neeche diye gaye buttons par click karke alag-alag modules ki commands dekh sakte hain:"
    )

# --- Callbacks for 1-Page Menu ---

async def menu_callback_handler(client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    
    if data == "fake_unmute":
        return await callback_query.answer(
            text="🤣 Abee saale tu chutiya hai kya, mute tune lagaya jo tu hatayega!", 
            show_alert=True
        )

    await callback_query.answer()
    
    if data == "menu_close":
        return await callback_query.message.delete()
        
    elif data == "stop_all":
        await hard_stop_all(chat_id, client, callback_query.from_user.id)
        return await callback_query.edit_message_text(
            "🚨 ALL ACTIVE TASKS & TRAPS TERMINATED 100%.", 
            reply_markup=get_single_page_menu_keyboard()
        )
        
    elif data == "menu_combat":
        text = (
            "⚔️ **COMBAT & WARFARE**\n"
            "────────────────────────────\n"
            "• `.gcnc [spd] [name]` — Coordinated title loop\n"
            "• `.vgcnc [spd] [T1 | T2]` — Title rotator\n"
            "• `.stopgcnc` — Halt active title loop\n"
            "• `.spam [text]` — High-speed spam\n"
            "• `.stopspam` — Emergency stop\n"
            "• `.gcpfp` — Group photo loop\n"
            "• `.stopgcpfp` — Stop photo loop\n"
            "• `.voiceflood` — Voice loop\n"
            "• `.stopvoiceflood` — Stop voice flood"
        )
        await callback_query.edit_message_text(text, reply_markup=get_single_page_menu_keyboard(), parse_mode="markdown")
        
    elif data == "menu_targets":
        text = (
            "🎯 **TRAPS & TARGETING**\n"
            "────────────────────────────\n"
            "• `.target [user]` — Mention loop\n"
            "• `.vtarget [@user]` — Advanced 15-reply target trap\n"
            "• `.stoptarget` — Disarm targeting loops\n"
            "• `.flood [user]` — Mention flood\n"
            "• `.vflood [user] [text]` — Custom mention flood\n"
            "• `.stopflood` — Stop mention flood\n"
            "• `.ht` — Honeytrap (Shadow-mute)\n"
            "• `.autoreply [user]` — Auto-reply trap\n"
            "• `.vautoreply [user] [msg]` — Custom reply trap\n"
            "• `.stopautoreply` — Disarm auto-reply"
        )
        await callback_query.edit_message_text(text, reply_markup=get_single_page_menu_keyboard(), parse_mode="markdown")
        
    elif data == "menu_tools":
        text = (
            "🛠️ **BLACKOUT & TOOLS**\n"
            "────────────────────────────\n"
            "• `.scan` — Group scanner\n"
            "• `.ping` — Latency test\n"
            "• `.getid` — Fetch numeric ID\n"
            "• `.status` — State check\n"
            "• `.omg` — Extract view-once media to PM\n"
            "• `.tts [text]` — Voice Note TTS\n"
            "• `.roasthi / .roasteng` — Roasts\n"
            "• `.clean [count]` — Purge messages\n"
            "• `.togglereactall` — Toggle reactions"
        )
        await callback_query.edit_message_text(text, reply_markup=get_single_page_menu_keyboard(), parse_mode="markdown")
        
    elif data == "menu_owner":
        text = (
            "👑 **OWNER CONTROLS**\n"
            "────────────────────────────\n"
            "• `.leave` — Leave current chat\n"
            "• `.cluster` — Node telemetry\n"
            "• `.broadcast [text]` — Network broadcast\n"
            "• `.gban / .ungban` — Global ban system\n"
            "• `.slayinpowergifted [id]` — Add admin\n"
            "• `.slayinpowertaken [id]` — Revoke admin"
        )
        await callback_query.edit_message_text(text, reply_markup=get_single_page_menu_keyboard(), parse_mode="markdown")

# --- Combat Commands (Userbot Prefix '.') ---

async def cmd_gcnc(client, message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()[1:]
    speed = 0.3
    name = "KRISHSLAYIN"

    if args:
        try:
            speed = float(args[0])
            name = " ".join(args[1:]) if len(args) > 1 else "KRISHSLAYIN"
        except ValueError:
            name = " ".join(args)

    chat_data = get_chat_data(message.chat.id)
    if "gcnc" in chat_data["tasks"]: chat_data["tasks"]["gcnc"].cancel()

    async def gcnc_loop():
        titles = [f"⚡ {name} ⚡", f"🔥 {name} 🔥", f"👑 {name} 👑"]
        title_idx = 0
        while True:
            try:
                await client.set_chat_title(chat_id=message.chat.id, title=titles[title_idx % len(titles)])
                title_idx += 1
            except Exception: pass
            await asyncio.sleep(speed if speed > 0 else 0.05)

    chat_data["tasks"]["gcnc"] = asyncio.create_task(gcnc_loop())
    await message.edit(f"⚔️ Userbot engaged in GCNC Loop (Speed: {speed}s).")

async def cmd_vgcnc(client, message):
    if not is_admin(message.from_user.id): return
    raw_text = message.text.replace(".vgcnc", "").strip()
    parts = raw_text.split(" ", 1)
    
    speed = 0.3
    titles_raw = ""

    if len(parts) > 0:
        try:
            speed = float(parts[0])
            titles_raw = parts[1] if len(parts) > 1 else ""
        except ValueError:
            titles_raw = raw_text

    titles = [t.strip() for t in titles_raw.split("|") if t.strip()]
    if not titles: return await message.edit("Usage: .vgcnc [speed] Title 1 | Title 2")

    chat_data = get_chat_data(message.chat.id)
    if "gcnc" in chat_data["tasks"]: chat_data["tasks"]["gcnc"].cancel()

    async def vgcnc_loop():
        title_idx = 0
        while True:
            try:
                await client.set_chat_title(chat_id=message.chat.id, title=titles[title_idx % len(titles)])
                title_idx += 1
            except Exception: pass
            await asyncio.sleep(speed if speed > 0 else 0.05)

    chat_data["tasks"]["gcnc"] = asyncio.create_task(vgcnc_loop())
    await message.edit(f"⚡ Userbot engaged in VGCNC Rotator (Speed: {speed}s).")

async def cmd_stopgcnc(client, message):
    chat_data = get_chat_data(message.chat.id)
    if "gcnc" in chat_data["tasks"]:
        chat_data["tasks"]["gcnc"].cancel()
        del chat_data["tasks"]["gcnc"]
        await message.edit("🛑 Title loop disarmed.")

async def cmd_spam(client, message):
    if not is_admin(message.from_user.id): return
    text = " ".join(message.text.split()[1:])
    if not text: return await message.edit("Usage: .spam <text>")
    chat_data = get_chat_data(message.chat.id)
    if "spam" in chat_data["tasks"]: chat_data["tasks"]["spam"].cancel()

    async def spam_loop():
        while True:
            try: await client.send_message(chat_id=message.chat.id, text=text)
            except Exception: pass
            await asyncio.sleep(0.12)

    chat_data["tasks"]["spam"] = asyncio.create_task(spam_loop())
    await message.delete()

async def cmd_stopspam(client, message):
    if not is_admin(message.from_user.id): return
    await hard_stop_all(message.chat.id, client, message.from_user.id)
    await message.edit("🛑 STRICT EMERGENCY STOP: All tasks and loops killed!")

async def cmd_target(client, message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()[1:]
    user = args[0] if args else "@target"
    chat_data = get_chat_data(message.chat.id)
    if "target" in chat_data["tasks"]: chat_data["tasks"]["target"].cancel()

    async def target_loop():
        while True:
            line = random.choice(TARGET_LINES)
            try: await client.send_message(chat_id=message.chat.id, text=f"{user}\n{line}")
            except Exception: pass
            await asyncio.sleep(0.2)

    chat_data["tasks"]["target"] = asyncio.create_task(target_loop())
    await message.delete()

async def cmd_vtarget(client, message):
    if not is_admin(message.from_user.id): return
    reply = message.reply_to_message
    target_id = None
    target_username = None

    if reply and reply.from_user:
        target_id = reply.from_user.id
        target_username = reply.from_user.username.lower() if reply.from_user.username else None
    else:
        args = message.text.split()[1:]
        if args:
            target_id = args[0].lower().replace("@", "")

    if not target_id:
        return await message.edit("⚠️ Target specify karo! (Reply or @username)")

    chat_data = get_chat_data(message.chat.id)
    if "vtarget_trap" not in chat_data:
        chat_data["vtarget_trap"] = {}
        
    chat_data["vtarget_trap"][str(target_id)] = True
    if target_username:
        chat_data["vtarget_trap"][target_username] = True

    await message.edit("🎯 Advanced 15-Swipe Trap Activated!")

async def cmd_stoptarget(client, message):
    chat_data = get_chat_data(message.chat.id)
    if "target" in chat_data["tasks"]:
        chat_data["tasks"]["target"].cancel()
        del chat_data["tasks"]["target"]
    if "vtarget_trap" in chat_data:
        chat_data["vtarget_trap"].clear()
    await message.edit("🛑 All Targeting and Traps disarmed.")

async def cmd_flood(client, message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()[1:]
    user = args[0] if args else "@target"
    chat_data = get_chat_data(message.chat.id)
    if "flood" in chat_data["tasks"]: chat_data["tasks"]["flood"].cancel()

    async def flood_loop():
        while True:
            for line in FLOOD_LINES:
                try: await client.send_message(chat_id=message.chat.id, text=f"{user}\n{line}")
                except Exception: pass
                await asyncio.sleep(0.15)

    chat_data["tasks"]["flood"] = asyncio.create_task(flood_loop())
    await message.delete()

async def cmd_vflood(client, message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()[1:]
    if len(args) < 2: return await message.edit("Usage: .vflood <user> <text>")
    user, text = args[0], " ".join(args[1:])
    chat_data = get_chat_data(message.chat.id)
    if "flood" in chat_data["tasks"]: chat_data["tasks"]["flood"].cancel()

    async def vflood_loop():
        while True:
            try: await client.send_message(chat_id=message.chat.id, text=f"🌊 {user} {text}")
            except Exception: pass
            await asyncio.sleep(0.15)

    chat_data["tasks"]["flood"] = asyncio.create_task(vflood_loop())
    await message.delete()

async def cmd_stopflood(client, message):
    chat_data = get_chat_data(message.chat.id)
    if "flood" in chat_data["tasks"]:
        chat_data["tasks"]["flood"].cancel()
        del chat_data["tasks"]["flood"]
        await message.edit("🛑 Flood stopped.")

async def cmd_gcpfp(client, message):
    if not is_admin(message.from_user.id): return
    reply = message.reply_to_message
    if not reply or not reply.photo: return await message.edit("Reply to an image.")
    file_path = await client.download_media(reply)
    chat_data = get_chat_data(message.chat.id)
    if "gcpfp" in chat_data["tasks"]: chat_data["tasks"]["gcpfp"].cancel()

    async def photo_loop():
        while True:
            try: await client.set_chat_photo(chat_id=message.chat.id, photo=file_path)
            except Exception: pass
            await asyncio.sleep(3)

    chat_data["tasks"]["gcpfp"] = asyncio.create_task(photo_loop())
    await message.edit("🖼️ Group photo loop active.")

async def cmd_stopgcpfp(client, message):
    chat_data = get_chat_data(message.chat.id)
    if "gcpfp" in chat_data["tasks"]:
        chat_data["tasks"]["gcpfp"].cancel()
        del chat_data["tasks"]["gcpfp"]
        await message.edit("🛑 Photo loop disarmed.")

async def cmd_voiceflood(client, message):
    if not is_admin(message.from_user.id): return
    reply = message.reply_to_message
    if not reply or not (reply.voice or reply.audio): return await message.edit("Reply to audio/voice.")
    file_path = await client.download_media(reply)
    chat_data = get_chat_data(message.chat.id)
    if "voiceflood" in chat_data["tasks"]: chat_data["tasks"]["voiceflood"].cancel()

    async def voice_loop():
        while True:
            try: await client.send_voice(chat_id=message.chat.id, voice=file_path)
            except Exception: pass
            await asyncio.sleep(0.2)

    chat_data["tasks"]["voiceflood"] = asyncio.create_task(voice_loop())
    await message.delete()

async def cmd_stopvoiceflood(client, message):
    chat_data = get_chat_data(message.chat.id)
    if "voiceflood" in chat_data["tasks"]:
        chat_data["tasks"]["voiceflood"].cancel()
        del chat_data["tasks"]["voiceflood"]
        await message.edit("🛑 Voice flood stopped.")

async def cmd_ht(client, message):
    if not is_admin(message.from_user.id): return
    reply = message.reply_to_message
    args = message.text.split()[1:]
    
    target_user = reply.from_user if reply else None
    target_id = target_user.id if target_user else (int(args[0]) if args and args[0].isdigit() else None)

    if not target_id: 
        return await message.edit("⚠️ Reply to target user's message or pass User ID.")

    get_chat_data(message.chat.id)["muted"].add(target_id)
    target_mention = f"@{target_user.username}" if (target_user and target_user.username) else f"`{target_id}`"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔊 Tap to Unmute Yourself", callback_data="fake_unmute")]
    ])
    
    await message.edit(
        f"🔇 USER SHADOW-MUTED: {target_mention}",
        reply_markup=keyboard
    )

async def cmd_mute(client, message):
    if not is_admin(message.from_user.id): return
    reply = message.reply_to_message
    args = message.text.split()[1:]
    target_id = reply.from_user.id if reply else (int(args[0]) if args and args[0].isdigit() else None)
    if not target_id: return await message.edit("Reply to target or pass User ID.")
    get_chat_data(message.chat.id)["muted"].add(target_id)
    await message.edit(f"🔇 Target {target_id} shadow-muted.")

async def cmd_unmute(client, message):
    if not is_admin(message.from_user.id): return
    reply = message.reply_to_message
    args = message.text.split()[1:]
    target_id = reply.from_user.id if reply else (int(args[0]) if args and args[0].isdigit() else None)
    if not target_id: return await message.edit("Reply to target or pass User ID.")
    get_chat_data(message.chat.id)["muted"].discard(target_id)
    await message.edit(f"🔊 Target {target_id} unmuted.")

async def cmd_mutelist(client, message):
    muted = get_chat_data(message.chat.id)["muted"]
    text = "🔇 MUTED TARGETS:\n" + "\n".join([f"• {uid}" for uid in muted]) if muted else "No muted users."
    await message.edit(text)

async def cmd_stripmedia(client, message):
    if not is_admin(message.from_user.id): return
    reply = message.reply_to_message
    args = message.text.split()[1:]
    target_id = reply.from_user.id if reply else (int(args[0]) if args and args[0].isdigit() else None)
    if not target_id: return await message.edit("Reply to target or pass User ID.")
    get_chat_data(message.chat.id)["stripmedia"].add(target_id)
    await message.edit(f"✂️ Media stripper active on {target_id}.")

async def cmd_stopstripmedia(client, message):
    get_chat_data(message.chat.id)["stripmedia"].clear()
    await message.edit("✂️ Media stripper disarmed.")

async def cmd_pfpstripper(client, message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()[1:]
    state = args[0].lower() == "on" if args else False
    get_chat_data(message.chat.id)["pfpstripper"] = state
    await message.edit(f"🖼️ PFP Stripper: {state}")

async def cmd_autoreply(client, message):
    if not is_admin(message.from_user.id): return
    reply = message.reply_to_message
    args = message.text.split()[1:]
    target_id = reply.from_user.id if reply else (int(args[0]) if args and args[0].isdigit() else None)
    if not target_id: return await message.edit("Reply to target or pass User ID.")
    get_chat_data(message.chat.id)["autoreply"][target_id] = "RANDOM_LINES"
    await message.edit(f"🤖 Auto-reply trap active on {target_id}.")

async def cmd_vautoreply(client, message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()[1:]
    if len(args) < 2: return await message.edit("Usage: .vautoreply <user_id> <msg>")
    target_id = int(args[0])
    msg = " ".join(args[1:])
    get_chat_data(message.chat.id)["autoreply"][target_id] = msg
    await message.edit(f"🤖 Custom auto-reply trap active on {target_id}.")

async def cmd_stopautoreply(client, message):
    get_chat_data(message.chat.id)["autoreply"].clear()
    await message.edit("🛑 Auto-reply trap disarmed.")

async def cmd_reptts(client, message):
    if not is_admin(message.from_user.id): return
    reply = message.reply_to_message
    args = message.text.split()[1:]
    target_id = reply.from_user.id if reply else (int(args[0]) if args and args[0].isdigit() else None)
    if not target_id: return await message.edit("Reply to target or pass User ID.")
    get_chat_data(message.chat.id)["reptts"].add(target_id)
    await message.edit(f"🗣️ Voice trap active on {target_id}.")

async def cmd_stopreptts(client, message):
    get_chat_data(message.chat.id)["reptts"].clear()
    await message.edit("🛑 Voice trap disarmed.")

async def cmd_clean(client, message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()[1:]
    count = int(args[0]) if args and args[0].isdigit() else 50
    if count > 200: count = 200
    
    deleted = 0
    async for msg in client.get_chat_history(message.chat.id, limit=count):
        try:
            await msg.delete()
            deleted += 1
        except Exception: pass
        await asyncio.sleep(0.1)

async def cmd_togglereactall(client, message):
    if not is_admin(message.from_user.id): return
    chat_id = message.chat.id
    current_mode = GLOBAL_CHAT_REACT_MODE.get(chat_id)
    
    if current_mode == "all":
        GLOBAL_CHAT_REACT_MODE[chat_id] = None
        await message.edit("❌ Auto-Reaction Disabled.")
    else:
        GLOBAL_CHAT_REACT_MODE[chat_id] = "all"
        await message.edit("✅ Auto-Reaction Enabled for ALL users!")

async def cmd_scan(client, message):
    chat = await client.get_chat(message.chat.id)
    members = await client.get_chat_members_count(message.chat.id)
    await message.edit(f"📊 CHAT MATRIX SCAN:\n• Title: {chat.title}\n• ID: {chat.id}\n• Members: {members}")

async def cmd_ping(client, message):
    start = time.time()
    msg = await message.edit("📡 Pinging userbot...")
    latency = round((time.time() - start) * 1000, 2)
    await msg.edit(f"📶 LATENCY: {latency}ms 🟢")

async def cmd_getid(client, message):
    target = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    await message.edit(f"🆔 User ID: {target.id}\n💬 Chat ID: {message.chat.id}")

async def cmd_status(client, message):
    tasks = len(get_chat_data(message.chat.id)["tasks"])
    await message.edit(f"⚙️ USERBOT STATE: Active 🟢\n🔥 Active Tasks: {tasks}")

async def cmd_omg(client, message):
    if not is_admin(message.from_user.id): return
    reply = message.reply_to_message
    if not reply: return await message.edit("⚠️ Reply to a media message with .omg.")

    status_msg = await message.edit("⚡ Extracting media...")
    try:
        file_path = await client.download_media(reply)
        await client.send_document(chat_id="me", document=file_path, caption=f"🔓 MEDIA EXTRACTED VIA USERBOT\nChat: {message.chat.title}")
        await status_msg.edit("✅ Saved to your Saved Messages (PM)!")
    except Exception as e:
        await status_msg.edit(f"❌ Extraction Error: {str(e)}")

async def cmd_tts_lang(client, message, lang: str):
    text = " ".join(message.text.split()[1:])
    if not text: return await message.edit("⚠️ Error: Message mein text likhein!")
    if gTTS is None: return await message.edit(f"🔊 gTTS not installed.")
    
    try:
        tts = gTTS(text=text, lang=lang)
        filename = f"tts_{message.chat.id}.mp3"
        tts.save(filename)
        await client.send_voice(chat_id=message.chat.id, voice=filename)
        os.remove(filename)
        await message.delete()
    except Exception as e:
        await message.edit(f"❌ Voice Error: {str(e)}")

async def cmd_tts(client, message): await cmd_tts_lang(client, message, "hi")
async def cmd_ttshi(client, message): await cmd_tts_lang(client, message, "hi")
async def cmd_ttsen(client, message): await cmd_tts_lang(client, message, "en")
async def cmd_ttsjap(client, message): await cmd_tts_lang(client, message, "ja")
async def cmd_ttsgerman(client, message): await cmd_tts_lang(client, message, "de")

async def cmd_roasthi(client, message):
    roast = random.choice(ROASTS_HI)
    await message.edit(f"🔥 {roast}")

async def cmd_roasteng(client, message):
    roast = random.choice(ROASTS_ENG)
    await message.edit(f"🔥 {roast}")

async def cmd_leave(client, message):
    if message.from_user.id != OWNER_ID: return
    try:
        await message.edit("👋 Leaving chat...")
        await client.leave_chat(message.chat.id)
    except Exception as e:
        await message.edit(f"❌ Failed: {e}")

async def cmd_cluster(client, message):
    if message.from_user.id != OWNER_ID: return
    me = await client.get_me()
    await message.edit(f"🌐 USERBOT TELEMETRY:\n• Account: @{me.username}\n• Status: ACTIVE 🟢")

async def cmd_broadcast(client, message):
    if message.from_user.id != OWNER_ID: return
    text = " ".join(message.text.split()[1:])
    if not text: return await message.edit("Usage: .broadcast <text>")
    await message.edit(f"📢 BROADCAST SENT:\n{text}")

async def cmd_gban(client, message):
    if message.from_user.id != OWNER_ID: return
    reply = message.reply_to_message
    if not reply: return await message.edit("Reply to user.")
    GBANNED_USERS.add(reply.from_user.id)
    await message.edit(f"🚫 Target {reply.from_user.id} globally blacklisted.")

async def cmd_ungban(client, message):
    if message.from_user.id != OWNER_ID: return
    reply = message.reply_to_message
    if not reply: return await message.edit("Reply to user.")
    GBANNED_USERS.discard(reply.from_user.id)
    await message.edit(f"✅ Target {reply.from_user.id} removed from blacklist.")

# --- Global Message & Command Handler (Pyrogram) ---

async def global_message_handler(client, message):
    if not message or not message.from_user: return
    user_id = message.from_user.id
    username = message.from_user.username.lower() if message.from_user.username else ""
    chat_id = message.chat.id
    chat_data = get_chat_data(chat_id)
    text = message.text.strip() if message.text else ""

    cmd_name = ""
    is_valid_cmd = False
    if text.startswith("."):
        possible_cmd = text.split()[0][1:].lower()
        if possible_cmd in VALID_COMMANDS:
            cmd_name = possible_cmd
            is_valid_cmd = True

    if chat_data.get("pfpstripper") and message.new_chat_photo:
        try: await message.delete()
        except Exception: pass

    if user_id in GBANNED_USERS or user_id in chat_data["muted"]:
        try: await message.delete()
        except Exception: pass
        return

    if user_id in chat_data["stripmedia"] and (message.photo or message.video or message.document):
        try: await message.delete()
        except Exception: pass

    # --- VTARGET TRAP EXECUTION ---
    if "vtarget_trap" in chat_data and chat_data["vtarget_trap"]:
        if str(user_id) in chat_data["vtarget_trap"] or (username and username in chat_data["vtarget_trap"]):
            async def fire_15():
                for _ in range(15):
                    line = random.choice(TARGET_15_LINES)
                    try:
                        await client.send_message(chat_id=chat_id, text=line, reply_to_message_id=message.id)
                        await asyncio.sleep(0.3)
                    except Exception: pass
            asyncio.create_task(fire_15())

    # Autoreply
    autoreply_map = chat_data.get("autoreply", {})
    if user_id in autoreply_map:
        val = autoreply_map[user_id]
        reply_text = random.choice(AUTOREPLY_LINES) if val == "RANDOM_LINES" else val
        try: await client.send_message(chat_id=chat_id, text=reply_text, reply_to_message_id=message.id)
        except Exception: pass

    # Reactions
    if GLOBAL_CHAT_REACT_MODE.get(chat_id) == "all":
        try:
            await client.send_reaction(chat_id=chat_id, message_id=message.id, emoji=REACTION_EMOJI)
        except Exception: pass

    # Command Execution Router
    if is_valid_cmd and user_id == (await client.get_me()).id:
        routes = {
            "start": lambda c, m: m.edit(get_single_page_menu_text(), reply_markup=get_single_page_menu_keyboard()),
            "menu": lambda c, m: m.edit(get_single_page_menu_text(), reply_markup=get_single_page_menu_keyboard()),
            "panel": lambda c, m: m.edit(get_single_page_menu_text(), reply_markup=get_single_page_menu_keyboard()),
            "gcnc": cmd_gcnc, "vgcnc": cmd_vgcnc, "stopgcnc": cmd_stopgcnc,
            "target": cmd_target, "vtarget": cmd_vtarget, "stoptarget": cmd_stoptarget,
            "spam": cmd_spam, "stopspam": cmd_stopspam,
            "flood": cmd_flood, "vflood": cmd_vflood, "stopflood": cmd_stopflood,
            "gcpfp": cmd_gcpfp, "stopgcpfp": cmd_stopgcpfp,
            "voiceflood": cmd_voiceflood, "stopvoiceflood": cmd_stopvoiceflood,
            "ht": cmd_ht, "mute": cmd_mute, "unmute": cmd_unmute, "mutelist": cmd_mutelist,
            "stripmedia": cmd_stripmedia, "stopstripmedia": cmd_stopstripmedia,
            "pfpstripper": cmd_pfpstripper,
            "autoreply": cmd_autoreply, "vautoreply": cmd_vautoreply, "stopautoreply": cmd_stopautoreply,
            "reptts": cmd_reptts, "stopreptts": cmd_stopreptts,
            "clean": cmd_clean, "togglereactall": cmd_togglereactall, "stopall": cmd_stopspam,
            "scan": cmd_scan, "ping": cmd_ping, "getid": cmd_getid, "status": cmd_status,
            "omg": cmd_omg, "tts": cmd_tts, 
            "ttshi": cmd_ttshi, "ttsen": cmd_ttsen, "ttsjap": cmd_ttsjap, "ttsgerman": cmd_ttsgerman,
            "roasthi": cmd_roasthi, "roasteng": cmd_roasteng,
            "cluster": cmd_cluster, "broadcast": cmd_broadcast,
            "slayinpowergifted": lambda c, m: m.edit("Admin added."),
            "slayinpowertaken": lambda c, m: m.edit("Admin removed."),
            "gban": cmd_gban, "ungban": cmd_ungban, "leave": cmd_leave
        }
        if cmd_name in routes:
            try:
                await routes[cmd_name](client, message)
            except Exception as e:
                logging.error(f"Command error {cmd_name}: {e}")

# --- Main App Execution ---

if __name__ == '__main__':
    if not SESSION_STRING:
        print("❌ Error: SESSION_STRING environment variable missing for Pyrogram Userbot!")
        sys.exit(1)

    app = Client(
        "my_userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING
    )

    # Handlers register karein
    from pyrogram.handlers import MessageHandler, CallbackQueryHandler
    app.add_handler(MessageHandler(global_message_handler))
    app.add_handler(CallbackQueryHandler(menu_callback_handler))

    print("🚀 Pyrogram Userbot starting...")
    app.run()
