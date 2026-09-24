# -*- coding: utf-8 -*-
import os
import time
import random
import asyncio
import logging
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

from pyrogram import Client, filters, enums
from pyrogram.types import Message

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID", "123456")) # Apni API ID dalein
API_HASH = os.environ.get("API_HASH", "your_api_hash") # Apna API Hash dalein
OWNER_ID = int(os.environ.get("OWNER_ID", "8821066459"))

AUTHORIZED_ADMINS = set([8821066459, OWNER_ID])
GBANNED_USERS = set()
CHAT_TASKS = {}
CLIENT_INSTANCES = []

GLOBAL_CHAT_REACT_MODE = {}
REACTION_EMOJI = "🤣"

# --- DATA ARRAYS ---
TARGET_15_LINES = [
    "Clap करो रंडीबाले ne joke mara h 😂👋🏻😂👋🏻😂👋🏻😂👋🏻😂👋🏻😂👋🏻",
    "चलेगी toh teri लंगड़ी maa 😁🔥😂👋🏻😂😂🔥🔥",
    "तेरी maa rundy 😜🙀⚡तेरी maa rundy 😜🙀⚡",
    "Oye message mat kar warna ᴛᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅ dunga🤣🤣",
    "अच्छा teri maa के बूब्स पे green veins h इसलिए tu itna खिलसता h 😂👏🏻",
    "𝐄ɴᴛʀʏ 𝐋ᴇʟɪ 𝐓ᴏ 𝐀sᴍᴀɴ 𝐊ɪ 𝐔ᴄʜᴀɪᴏ 𝐏ᴇ 𝐓ᴇʀɪ 𝐌ᴀ 𝐂ʜᴜᴅᴇɢɪ / 🌘🕊️",
    "Teri Maa Ko Football ⚽ bnake uske 𝗕𝗛😈𝗦𝗗𝗘 pe laat 🦶🏻 marunga 🤩🔥",
    "Tri maa ke bosde pr jcb se khudai krwa duga rndyke😂😂🤟💥💥🤟",
    "Le धमाकेदार mukka kha रन्डी ke चाइल्ड 👊🏻👊🏻👊🏻🤣🤣",
    "चाल चल teri chudai डॉन hogyi !! Ab teri लंगड़ी maa दौड़ेगी 😂👋🏻",
    "subha ho ya sham chudte rhena hai tera kaam😂🔥😂🔥😂🔥",
    "randy pane me to teri ma aval darje ki hakdaar he😁👍😁👍😁👍😁👍",
    "𝘿𝙃𝘼𝙏 ʳⁿᵈⁱ𝙠ᵉʸ 🤦🏿‍♂️💢𝘿𝙃𝘼𝙏 ʳⁿᵈⁱ𝙠ᵉʸ 🤦🏿‍♂️💢",
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
    r"""तेरी बहन का भोसड़ा 😂🤸🏻‍♂️😂🤸🏻‍♂️ 𝘾𝙃𝙐𝙋 𝙍𝙉𝘿𝙄𝙆𝙀"""
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

async def hard_stop_all(chat_id: int):
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

# --- SINGLE PAGE MENU TEXT ---
def get_single_page_menu():
    return (
        "⚔️ **KRISHSLAYIN USERBOT SYSTEM CORE** ⚡\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚔️ **COMBAT & WARFARE**\n"
        "• `+gcnc [spd] [name]` — Coordinated title loop\n"
        "• `+vgcnc [spd] [T1 | T2]` — Title rotator\n"
        "• `+stopgcnc` — Halt title loop\n"
        "• `+target [user]` — Mention loop\n"
        "• `+vtarget [user]` — Advanced 15-reply target trap\n"
        "• `+stoptarget` — Disarm targeting\n"
        "• `+spam [text]` — Speed spam\n"
        "• `+stopspam` — Emergency stop spam\n"
        "• `+flood [user]` / `+vflood [user] [text]` — Mention floods\n"
        "• `+stopflood` — Stop flood\n"
        "• `+gcpfp` / `+stopgcpfp` — Group PFP loop\n"
        "• `+voiceflood` / `+stopvoiceflood` — Voice loop\n\n"

        "⛓️ **TRAPS & CONTROL**\n"
        "• `+ht` / `+mute` [user] — Shadow-mute target\n"
        "• `+unmute` [user] | `+mutelist` — Manage mutes\n"
        "• `+stripmedia` [user] / `+stopstripmedia` — Media auto-delete\n"
        "• `+pfpstripper on/off` — Delete PFP changes\n"
        "• `+autoreply` / `+vautoreply` — Reply traps\n"
        "• `+stopautoreply` — Disarm reply trap\n"
        "• `+reptts` [user] / `+stopreptts` — Voice trap\n"
        "• `+clean [count]` — Purge messages\n"
        "• `+togglereactall` / `+togglereact` — Auto reactions\n"
        "• `+stopall` — **EMERGENCY KILL SWITCH**\n\n"

        "🛠️ **TOOLS & UTILS**\n"
        "• `+scan` | `+ping` | `+getid` | `+status` — Telemetry\n"
        "• `+omg` — Save view-once media to PM\n"
        "• `+tts` / `+ttshi` / `+ttsen` / `+ttsjap` [text] — Voice Note TTS\n"
        "• `+roasthi` / `+roasteng` [user] — Roasts\n\n"

        "👑 **OWNER CONTROLS**\n"
        "• `+cluster` — Node telemetry\n"
        "• `+broadcast [text]` — Network broadcast\n"
        "• `+slayinpowergifted` / `+slayinpowertaken` — Manage admins\n"
        "• `+gban` / `+ungban` — Global ban\n"
        "• `+leave` / `+leavekrishslayin` — Leave chat\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

# --- MAIN COMMAND ROUTER ---
@Client.on_message(filters.command([
    "start", "menu", "panel", "gcnc", "vgcnc", "stopgcnc",
    "target", "vtarget", "stoptarget", "spam", "stopspam",
    "flood", "vflood", "stopflood", "gcpfp", "stopgcpfp",
    "voiceflood", "stopvoiceflood", "ht", "mute", "unmute", "mutelist",
    "stripmedia", "stopstripmedia", "pfpstripper", "autoreply",
    "vautoreply", "stopautoreply", "reptts", "stopreptts",
    "clean", "togglereactall", "togglereact", "stopall",
    "scan", "ping", "getid", "status", "omg", "tts", 
    "ttshi", "ttsen", "ttsjap", "ttsgerman", 
    "roasthi", "roasteng", "cluster", "broadcast",
    "slayinpowergifted", "slayinpowertaken", "slayinfor",
    "gban", "ungban", "leave", "leavekrishslayin"
], prefixes="+"))
async def main_command_handler(client: Client, message: Message):
    user_id = message.from_user.id if message.from_user else 0
    if not is_admin(user_id): return

    cmd = message.command[0].lower()
    chat_id = message.chat.id
    chat_data = get_chat_data(chat_id)

    try:
        await message.delete()
    except Exception:
        pass

    # --- MENU & PANEL ---
    if cmd in ["start", "menu", "panel"]:
        await client.send_message(chat_id, get_single_page_menu(), parse_mode=enums.ParseMode.MARKDOWN)

    # --- COMBAT COMMANDS ---
    elif cmd == "gcnc":
        args = message.command[1:]
        speed = float(args[0]) if args and args[0].replace('.', '', 1).isdigit() else 0.3
        name = " ".join(args[1:]) if len(args) > 1 else "KRISHSLAYIN"

        if "gcnc" in chat_data["tasks"]: chat_data["tasks"]["gcnc"].cancel()

        async def multi_gcnc_loop():
            titles = [f"⚡ {name} ⚡", f"🔥 {name} 🔥", f"👑 {name} 👑"]
            title_idx = 0
            bot_idx = 0
            while True:
                curr_cli = CLIENT_INSTANCES[bot_idx % len(CLIENT_INSTANCES)]
                try: await curr_cli.set_chat_title(chat_id, titles[title_idx % len(titles)])
                except Exception: pass
                title_idx += 1
                bot_idx += 1
                await asyncio.sleep(speed if speed > 0 else 0.05)

        chat_data["tasks"]["gcnc"] = asyncio.create_task(multi_gcnc_loop())
        await client.send_message(chat_id, f"⚔️ GCNC Active across {len(CLIENT_INSTANCES)} Userbots! Speed: {speed}s")

    elif cmd == "vgcnc":
        raw_text = message.text.replace("+vgcnc", "").strip()
        parts = raw_text.split(" ", 1)
        speed = 0.3
        titles_raw = raw_text

        if len(parts) > 0 and parts[0].replace('.', '', 1).isdigit():
            speed = float(parts[0])
            titles_raw = parts[1] if len(parts) > 1 else ""

        titles = [t.strip() for t in titles_raw.split("|") if t.strip()]
        if not titles:
            return await client.send_message(chat_id, "Usage: +vgcnc [speed] Title 1 | Title 2")

        if "gcnc" in chat_data["tasks"]: chat_data["tasks"]["gcnc"].cancel()

        async def multi_vgcnc_loop():
            title_idx, bot_idx = 0, 0
            while True:
                curr_cli = CLIENT_INSTANCES[bot_idx % len(CLIENT_INSTANCES)]
                try: await curr_cli.set_chat_title(chat_id, titles[title_idx % len(titles)])
                except Exception: pass
                title_idx += 1
                bot_idx += 1
                await asyncio.sleep(speed if speed > 0 else 0.05)

        chat_data["tasks"]["gcnc"] = asyncio.create_task(multi_vgcnc_loop())

    elif cmd == "stopgcnc":
        if "gcnc" in chat_data["tasks"]:
            chat_data["tasks"]["gcnc"].cancel()
            del chat_data["tasks"]["gcnc"]
            await client.send_message(chat_id, "🛑 Title loop stopped.")

    elif cmd == "spam":
        text = " ".join(message.command[1:])
        if not text: return await client.send_message(chat_id, "Usage: +spam <text>")
        if "spam" in chat_data["tasks"]: chat_data["tasks"]["spam"].cancel()

        async def spam_loop():
            bot_idx = 0
            while True:
                curr_cli = CLIENT_INSTANCES[bot_idx % len(CLIENT_INSTANCES)]
                try: await curr_cli.send_message(chat_id, text)
                except Exception: pass
                bot_idx += 1
                await asyncio.sleep(0.12)

        chat_data["tasks"]["spam"] = asyncio.create_task(spam_loop())

    elif cmd in ["stopspam", "stopall"]:
        await hard_stop_all(chat_id)
        await client.send_message(chat_id, "🚨 EMERGENCY STOP: All tasks & traps terminated!")

    elif cmd == "target":
        args = message.command[1:]
        target_user = args[0] if args else "@target"
        if "target" in chat_data["tasks"]: chat_data["tasks"]["target"].cancel()

        async def target_loop():
            bot_idx = 0
            while True:
                curr_cli = CLIENT_INSTANCES[bot_idx % len(CLIENT_INSTANCES)]
                line = random.choice(TARGET_LINES)
                try: await curr_cli.send_message(chat_id, f"{target_user}\n{line}")
                except Exception: pass
                bot_idx += 1
                await asyncio.sleep(0.2)

        chat_data["tasks"]["target"] = asyncio.create_task(target_loop())

    elif cmd == "vtarget":
        reply = message.reply_to_message
        target_key = None
        if reply and reply.from_user:
            target_key = str(reply.from_user.id)
        elif len(message.command) > 1:
            target_key = message.command[1].replace("@", "").lower()

        if not target_key:
            return await client.send_message(chat_id, "⚠️ Specify target (Reply or username/ID)")

        chat_data["vtarget_trap"][target_key] = True
        await client.send_message(chat_id, f"🎯 15-Swipe Reply Trap activated on {target_key}!")

    elif cmd == "stoptarget":
        if "target" in chat_data["tasks"]:
            chat_data["tasks"]["target"].cancel()
            del chat_data["tasks"]["target"]
        chat_data["vtarget_trap"].clear()
        await client.send_message(chat_id, "🛑 Targeting loops disarmed.")

    elif cmd == "flood":
        target = message.command[1] if len(message.command) > 1 else "@target"
        if "flood" in chat_data["tasks"]: chat_data["tasks"]["flood"].cancel()

        async def flood_loop():
            bot_idx = 0
            while True:
                for line in FLOOD_LINES:
                    curr_cli = CLIENT_INSTANCES[bot_idx % len(CLIENT_INSTANCES)]
                    try: await curr_cli.send_message(chat_id, f"{target}\n{line}")
                    except Exception: pass
                    bot_idx += 1
                    await asyncio.sleep(0.15)

        chat_data["tasks"]["flood"] = asyncio.create_task(flood_loop())

    elif cmd == "vflood":
        if len(message.command) < 3: return await client.send_message(chat_id, "Usage: +vflood <user> <text>")
        user, text = message.command[1], " ".join(message.command[2:])
        if "flood" in chat_data["tasks"]: chat_data["tasks"]["flood"].cancel()

        async def vflood_loop():
            bot_idx = 0
            while True:
                curr_cli = CLIENT_INSTANCES[bot_idx % len(CLIENT_INSTANCES)]
                try: await curr_cli.send_message(chat_id, f"🌊 {user} {text}")
                except Exception: pass
                bot_idx += 1
                await asyncio.sleep(0.15)

        chat_data["tasks"]["flood"] = asyncio.create_task(vflood_loop())

    elif cmd == "stopflood":
        if "flood" in chat_data["tasks"]:
            chat_data["tasks"]["flood"].cancel()
            del chat_data["tasks"]["flood"]
            await client.send_message(chat_id, "🛑 Flood stopped.")

    elif cmd in ["ht", "mute"]:
        reply = message.reply_to_message
        target_id = reply.from_user.id if reply and reply.from_user else (int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else None)
        if not target_id: return await client.send_message(chat_id, "Reply to target or pass ID.")
        chat_data["muted"].add(target_id)
        await client.send_message(chat_id, f"🔇 Target {target_id} shadow-muted.")

    elif cmd == "unmute":
        reply = message.reply_to_message
        target_id = reply.from_user.id if reply and reply.from_user else (int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else None)
        if not target_id: return await client.send_message(chat_id, "Reply to target or pass ID.")
        chat_data["muted"].discard(target_id)
        await client.send_message(chat_id, f"🔊 Target {target_id} unmuted.")

    elif cmd == "mutelist":
        muted = chat_data["muted"]
        text = "🔇 MUTED TARGETS:\n" + "\n".join([f"• {uid}" for uid in muted]) if muted else "No muted users."
        await client.send_message(chat_id, text)

    elif cmd == "stripmedia":
        reply = message.reply_to_message
        target_id = reply.from_user.id if reply and reply.from_user else (int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else None)
        if target_id: chat_data["stripmedia"].add(target_id)
        await client.send_message(chat_id, f"✂️ Media stripper active on {target_id}.")

    elif cmd == "stopstripmedia":
        chat_data["stripmedia"].clear()
        await client.send_message(chat_id, "✂️ Media stripper disarmed.")

    elif cmd == "pfpstripper":
        state = message.command[1].lower() == "on" if len(message.command) > 1 else False
        chat_data["pfpstripper"] = state
        await client.send_message(chat_id, f"🖼️ PFP Stripper: {state}")

    elif cmd == "autoreply":
        reply = message.reply_to_message
        target_key = reply.from_user.id if reply and reply.from_user else (message.command[1].replace("@", "").lower() if len(message.command) > 1 else None)
        if target_key: chat_data["autoreply"][target_key] = "RANDOM_LINES"
        await client.send_message(chat_id, f"🤖 Auto-reply active on {target_key}.")

    elif cmd == "vautoreply":
        if len(message.command) < 3: return await client.send_message(chat_id, "Usage: +vautoreply <user/id> <msg>")
        target_key = message.command[1].replace("@", "").lower()
        msg_text = " ".join(message.command[2:])
        chat_data["autoreply"][target_key] = msg_text
        await client.send_message(chat_id, f"🤖 Custom auto-reply active on {target_key}.")

    elif cmd == "stopautoreply":
        chat_data["autoreply"].clear()
        await client.send_message(chat_id, "🛑 Auto-reply trap disarmed.")

    elif cmd == "reptts":
        reply = message.reply_to_message
        target_id = reply.from_user.id if reply and reply.from_user else (int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else None)
        if target_id: chat_data["reptts"].add(target_id)
        await client.send_message(chat_id, f"🗣️ Voice trap active on {target_id}.")

    elif cmd == "stopreptts":
        chat_data["reptts"].clear()
        await client.send_message(chat_id, "🛑 Voice trap disarmed.")

    elif cmd == "clean":
        count = int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else 100
        msg_id = message.id
        deleted = 0
        for i in range(count):
            try:
                await client.delete_messages(chat_id, msg_id - i)
                deleted += 1
            except Exception: pass
            if i % 30 == 0: await asyncio.sleep(0.3)
        res = await client.send_message(chat_id, f"✅ Purged {deleted} messages.")
        await asyncio.sleep(3)
        await res.delete()

    elif cmd == "togglereactall":
        curr = GLOBAL_CHAT_REACT_MODE.get(chat_id)
        GLOBAL_CHAT_REACT_MODE[chat_id] = None if curr == "all" else "all"
        await client.send_message(chat_id, f"Auto-Reaction ALL: {GLOBAL_CHAT_REACT_MODE[chat_id] is not None}")

    elif cmd == "togglereact":
        curr = GLOBAL_CHAT_REACT_MODE.get(chat_id)
        GLOBAL_CHAT_REACT_MODE[chat_id] = None if curr == "admin" else "admin"
        await client.send_message(chat_id, f"Auto-Reaction ADMIN: {GLOBAL_CHAT_REACT_MODE[chat_id] is not None}")

    elif cmd == "ping":
        start = time.time()
        m = await client.send_message(chat_id, "📡 Pinging cluster...")
        latency = round((time.time() - start) * 1000, 2)
        await m.edit_text(f"📶 LATENCY: {latency}ms 🟢")

    elif cmd == "scan":
        members = await client.get_chat_members_count(chat_id)
        await client.send_message(chat_id, f"📊 MATRIX SCAN:\n• ID: {chat_id}\n• Members: {members}")

    elif cmd == "getid":
        target = message.reply_to_message.from_user if message.reply_to_message else message.from_user
        await client.send_message(chat_id, f"🆔 User ID: {target.id}\n💬 Chat ID: {chat_id}")

    elif cmd == "status":
        await client.send_message(chat_id, f"⚙️ CLUSTER STATE: Active ({len(CLIENT_INSTANCES)} Userbots)")

    elif cmd == "omg":
        reply = message.reply_to_message
        if reply and (reply.photo or reply.video or reply.document or reply.voice):
            file_path = await reply.download()
            await client.send_document("me", file_path, caption=f"Extract from {chat_id}")
            os.remove(file_path)
            await client.send_message(chat_id, "✅ Saved media to Saved Messages!")

    elif cmd in ["tts", "ttshi", "ttsen", "ttsjap", "ttsgerman"]:
        lang_map = {"tts": "hi", "ttshi": "hi", "ttsen": "en", "ttsjap": "ja", "ttsgerman": "de"}
        text = " ".join(message.command[1:])
        if text and gTTS:
            tts = gTTS(text=text, lang=lang_map[cmd])
            fname = f"tts_{chat_id}.mp3"
            tts.save(fname)
            await client.send_audio(chat_id, fname)
            os.remove(fname)

    elif cmd in ["roasthi", "roasteng"]:
        target = f"@{message.reply_to_message.from_user.username}" if message.reply_to_message and message.reply_to_message.from_user else (" ".join(message.command[1:]) if len(message.command) > 1 else "")
        roast = random.choice(ROASTS_HI if cmd == "roasthi" else ROASTS_ENG)
        await client.send_message(chat_id, f"🔥 {target} {roast}")

    elif cmd == "cluster":
        if user_id == OWNER_ID:
            await client.send_message(chat_id, f"🌐 CLUSTER STATUS: {len(CLIENT_INSTANCES)} Active Userbot Instances.")

    elif cmd == "broadcast":
        if user_id == OWNER_ID:
            text = " ".join(message.command[1:])
            await client.send_message(chat_id, f"📢 BROADCAST: {text}")

    elif cmd == "slayinpowergifted":
        if user_id == OWNER_ID and len(message.command) > 1:
            AUTHORIZED_ADMINS.add(int(message.command[1]))
            await client.send_message(chat_id, f"👑 Admin added: {message.command[1]}")

    elif cmd == "slayinpowertaken":
        if user_id == OWNER_ID and len(message.command) > 1:
            AUTHORIZED_ADMINS.discard(int(message.command[1]))
            await client.send_message(chat_id, f"🗑️ Admin removed: {message.command[1]}")

    elif cmd == "gban":
        if user_id == OWNER_ID:
            target_id = message.reply_to_message.from_user.id if message.reply_to_message else int(message.command[1])
            GBANNED_USERS.add(target_id)
            await client.send_message(chat_id, f"🚫 Target {target_id} GBANNED.")

    elif cmd == "ungban":
        if user_id == OWNER_ID:
            target_id = message.reply_to_message.from_user.id if message.reply_to_message else int(message.command[1])
            GBANNED_USERS.discard(target_id)
            await client.send_message(chat_id, f"✅ Target {target_id} UNGBANNED.")

    elif cmd == "leave":
        await client.leave_chat(chat_id)

    elif cmd == "leavekrishslayin":
        if user_id == OWNER_ID:
            for cli in CLIENT_INSTANCES:
                try: await cli.leave_chat(chat_id)
                except Exception: pass

# --- GLOBAL MESSAGE LISTENER (Traps & Mute Execution) ---
@Client.on_message(~filters.me & ~filters.bot, group=1)
async def global_listener(client: Client, message: Message):
    if not message.from_user: return
    user_id = message.from_user.id
    username = message.from_user.username.lower() if message.from_user.username else ""
    chat_id = message.chat.id
    chat_data = get_chat_data(chat_id)

    # 1. GBAN & Shadow Mute
    if user_id in GBANNED_USERS or user_id in chat_data["muted"]:
        try: return await message.delete()
        except Exception: pass

    # 2. Media Stripper
    if user_id in chat_data["stripmedia"] and (message.photo or message.video or message.document):
        try: return await message.delete()
        except Exception: pass

    # 3. VTARGET 15-SWIPE TRAP
    if str(user_id) in chat_data["vtarget_trap"] or username in chat_data["vtarget_trap"]:
        async def fire_15_replies():
            for _ in range(15):
                line = random.choice(TARGET_15_LINES)
                try:
                    await message.reply_text(line)
                    await asyncio.sleep(0.3)
                except Exception: pass
        asyncio.create_task(fire_15_replies())

    # 4. Auto-reply Trap
    if user_id in chat_data["autoreply"] or username in chat_data["autoreply"]:
        key = user_id if user_id in chat_data["autoreply"] else username
        val = chat_data["autoreply"][key]
        rep = random.choice(AUTOREPLY_LINES) if val == "RANDOM_LINES" else val
        try: await message.reply_text(rep)
        except Exception: pass

    # 5. Voice Trap (TTS)
    if user_id in chat_data["reptts"] and message.text and gTTS:
        try:
            tts = gTTS(text=message.text, lang="hi")
            fname = f"rt_{chat_id}.mp3"
            tts.save(fname)
            await client.send_voice(chat_id, fname)
            os.remove(fname)
        except Exception: pass

    # 6. Auto Reactions
    react_mode = GLOBAL_CHAT_REACT_MODE.get(chat_id)
    if react_mode:
        if react_mode == "all" or (react_mode == "admin" and is_admin(user_id)):
            try: await client.send_reaction(chat_id, message.id, REACTION_EMOJI)
            except Exception: pass

# --- CLUSTER MULTI-ACCOUNT STARTER ---
async def start_all_clones():
    sessions = []
    
    # Environment variables se sabhi sessions retrieve karein
    for key, val in os.environ.items():
        if ("STRING_SESSION" in key or "SESSION" in key) and val.strip():
            sessions.append(val.strip())

    if not sessions:
        print("❌ Error: Minimum ek STRING_SESSION environment variable hona zaroori hai!")
        return

    print(f"🚀 Initializing {len(sessions)} Userbot Clones...")

    for idx, session in enumerate(sessions, start=1):
        app = Client(
            name=f"Userbot_{idx}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session,
            in_memory=True
        )
        await app.start()
        me = await app.get_me()
        CLIENT_INSTANCES.append(app)
        print(f"✅ Userbot #{idx} (@{me.username or me.first_name}) Connected successfully.")

    print("⚡ All Userbot instances active and synchronized.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_all_clones())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 All Userbots stopped.")
