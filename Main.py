from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Cricbuzz import get_upcoming_ipl_matches, get_live_score
from Config import API_ID, API_HASH, BOT_TOKEN

bot = Client("LiveIPLBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

match_data = {}

@bot.on_message(filters.command("start"))
async def start(_, message):
    matches = await get_upcoming_ipl_matches()
    if not matches:
        return await message.reply("❌ No upcoming IPL matches found!")

    match_data[message.from_user.id] = matches
    buttons = [
        [InlineKeyboardButton(f"{m['title']}", callback_data=f"match_{i}")]
        for i, m in enumerate(matches[:10])
    ]
    await message.reply("🏏 *Upcoming IPL Matches:*", reply_markup=InlineKeyboardMarkup(buttons), parse_mode="markdown")

@bot.on_callback_query()
async def handle_match_query(_, query):
    user_id = query.from_user.id
    matches = match_data.get(user_id)
    if not matches:
        return await query.answer("Please use /start again.", show_alert=True)

    index = int(query.data.split("_")[1])
    selected = matches[index]

    score = await get_live_score(selected['link'])
    if score:
        msg = (
            f"🏏 *{score['title']}*\n"
            f"📊 *Score:* {score['score']}\n"
            f"🕒 *Status:* {score['status']}\n\n"
            f"🎯 *Recent Ball:* {score['recent']}"
        )
    else:
        msg = (
            f"🏏 *{selected['title']}*\n"
            f"🕒 *Time:* {selected['time']}\n"
            f"📍 *Venue:* {selected['venue']}\n"
            f"👥 *Teams:* {selected['teams']}\n\n"
            f"🔗 [Match Info]({selected['link']})"
        )

    await query.message.edit_text(msg, parse_mode="markdown", disable_web_page_preview=True)

bot.run()
