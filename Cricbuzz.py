# CricGuruBot.py
import asyncio
import time
import httpx
from pyrogram import Client, filters

# Initialize Telegram Bot
app = Client("cric_guru", bot_token="YOUR_BOT_TOKEN", api_id=123456, api_hash="your_api_hash")

# RapidAPI headers
headers = {
    "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
    "X-RapidAPI-Host": "cricket-live-line1.p.rapidapi.com"
}

# Command to start live feed
@app.on_message(filters.command("live") & filters.user(YOUR_USER_ID))  # restrict to owner
async def live_match(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/live match_id`")
    
    match_id = message.command[1]
    chat_id = message.chat.id
    last_ball = ""

    await message.reply(f"Starting 🔴 *LIVE Cricket Feed* for match `{match_id}`...")

    while True:
        try:
            # Fetch live score
            async with httpx.AsyncClient() as clientx:
                res = await clientx.get(f"https://cricket-live-line1.p.rapidapi.com/match-detail?match_id={match_id}", headers=headers)
                data = res.json()
            
            score = data.get("score", "Not available")
            overs = data.get("overs", "??")
            striker = data.get("striker", {}).get("name", "Unknown")
            non_striker = data.get("non_striker", {}).get("name", "Unknown")
            batsman_scores = f"{striker} :- {data['striker']['runs']}({data['striker']['balls']})\n" \
                             f"{non_striker} :- {data['non_striker']['runs']}({data['non_striker']['balls']})"

            # Fetch commentary
            res = await clientx.get(f"https://cricket-live-line1.p.rapidapi.com/commentary?match_id={match_id}", headers=headers)
            commentary_data = res.json().get("commentary", [])
            if commentary_data:
                latest_ball = commentary_data[0].get("text", "")
                ball_num = commentary_data[0].get("ball", "")

                if latest_ball != last_ball:
                    formatted = f"""
{ball_num} 🎾 {score}

{striker.upper()} ON STRIKE ✔️

🅾️ {overs} OVER 🅾️

📟 SCORECARD 📟
{batsman_scores}
                    """.strip()

                    await app.send_message(chat_id, formatted)
                    last_ball = latest_ball

        except Exception as e:
            await app.send_message(chat_id, f"⚠️ Error fetching live data:\n`{e}`")
        
        await asyncio.sleep(10)  # every 10 seconds

# Run the bot
app.run()
