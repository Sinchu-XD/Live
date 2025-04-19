from playwright.async_api import async_playwright
import asyncio

async def get_upcoming_ipl_matches():
    url = "https://m.cricbuzz.com/cricket-series/9237/indian-premier-league-2025/matches"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Launch headless browser
        page = await browser.new_page()
        await page.goto(url)
        
        # Wait for the page to fully load
        await page.wait_for_load_state('load')

        # Extract the match data
        matches = await page.query_selector_all('a.w-full.bg-cbWhite')  # Target the anchors with the match titles

        match_details = []
        for match in matches:
            title = await match.inner_text()  # Extract the match title
            link = await match.get_attribute('href')  # Get the link to match details
            match_details.append({'title': title, 'link': link})
        
        await browser.close()
        
        if match_details:
            return match_details
        else:
            return "No upcoming matches found!"

# Run the function and print results
async def main():
    result = await get_upcoming_ipl_matches()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
