import asyncio
from Cricbuzz import get_upcoming_ipl_matches, get_live_score

async def test_ipl_bot():
    print("✅ Testing upcoming IPL matches...\n")
    matches = await get_upcoming_ipl_matches()

    if not matches:
        print("❌ No upcoming IPL matches found!")
        return

    for i, match in enumerate(matches[:5], 1):
        print(f"{i}. {match['title']} - {match['time']}")
        print(f"   Venue: {match['venue']}")
        print(f"   Teams: {match['teams']}")
        print(f"   Link: {match['link']}\n")

    # Optional: Test live score for the first match (only if live)
    print("\n✅ Testing live score for first match (if live)...\n")
    score = await get_live_score(matches[0]["link"])
    if score:
        print(f"Title: {score['title']}")
        print(f"Score: {score['score']}")
        print(f"Status: {score['status']}")
        print(f"Recent Ball: {score['recent']}")
    else:
        print("⚠️ Score not available (match may not be live).")

# Run the test
asyncio.run(test_ipl_bot())
