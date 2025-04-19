from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Config import API_ID, API_HASH, BOT_TOKEN
from Cricbuzz import get_ipl_upcoming_matches

bot = Client("IPLMatchBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_match_data = {}

@bot.on_message(filters.command("start"))
async def start(client, message):
    matches = await get_ipl_upcoming_matches()
    if not matches:
        return await message.reply("❌ No upcoming IPL matches found!")

    user_match_data[message.from_user.id] = matches
    buttons = [
        [InlineKeyboardButton(text=f"{m['title'][:50]}", callback_data=f"match_{i}")]
        for i, m in enumerate(matches[:10])  # Show max 10 buttons
    ]

    await message.reply(
        "🏏 *Upcoming IPL Matches:*",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="markdown"
    )

@bot.on_callback_query()
async def match_info(client, query):
    matches = user_match_data.get(query.from_user.id)
    if not matches:
        return await query.answer("No match data found. Use /start again.")

    match_index = int(query.data.split("_")[1])
    if match_index >= len(matches):
        return await query.answer("Invalid match selected.")

    match = matches[match_index]
    msg = (
        f"🏏 *{match['title']}*\n"
        f"🕒 *Time:* {match['time']}\n"
        f"📍 *Venue:* {match['venue']}\n"
        f"👥 *Teams:* {match['teams']}\n"
        f"🔗 [View on Cricbuzz]({match['link']})"
    )
    await query.message.edit(msg, parse_mode="markdown", disable_web_page_preview=True)

bot.run()
