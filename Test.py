import asyncio
from Cricbuzz import get_upcoming_ipl_matches

async def main():
    print("✅ Testing upcoming IPL matches...\n")
    matches = await get_upcoming_ipl_matches()
    if not matches:
        print("❌ No upcoming IPL matches found!")
    else:
        for i, m in enumerate(matches, 1):
            print(f"{i}. {m['title']} - {m['time']}\n   {m['link']}")

asyncio.run(main())
