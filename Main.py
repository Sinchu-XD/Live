from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Config import API_ID, API_HASH, BOT_TOKEN
from Cricbuzz import get_live_matches, get_score_and_commentary

bot = Client("LiveScoreBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_match_links = {}

@bot.on_message(filters.command("start"))
async def start(_, message):
    matches = await get_live_matches()
    if not matches:
        return await message.reply("No live matches found!")

    buttons = [
        [InlineKeyboardButton(text=m["title"], callback_data=f"match_{i}")]
        for i, m in enumerate(matches)
    ]
    await message.reply("Select a match:", reply_markup=InlineKeyboardMarkup(buttons))
    user_match_links[message.from_user.id] = matches

@bot.on_callback_query()
async def match_select(_, query):
    matches = user_match_links.get(query.from_user.id, [])
    match_index = int(query.data.split("_")[1])
    if match_index >= len(matches):
        return await query.answer("Invalid match.")
    link = matches[match_index]["link"]
    user_match_links[query.from_user.id] = link
    await query.message.edit(f"✅ Match Selected:\n{matches[match_index]['title']}")

@bot.on_message(filters.command("score"))
async def live_score(_, message):
    link = user_match_links.get(message.from_user.id)
    if not link:
        return await message.reply("Please select a match using /start")
    score, status, _ = await get_score_and_commentary(link)
    await message.reply(f"🏏 *Score:* `{score}`\n📢 *Status:* `{status}`", parse_mode="markdown")

@bot.on_message(filters.command("commentary"))
async def live_commentary(_, message):
    link = user_match_links.get(message.from_user.id)
    if not link:
        return await message.reply("Please select a match using /start")
    _, _, last_ball = await get_score_and_commentary(link)
    await message.reply(f"🗣️ *Last Ball:* `{last_ball}`", parse_mode="markdown")

bot.run()
