import asyncio
from playwright.async_api import async_playwright

async def get_upcoming_ipl_matches():
    url = "https://m.cricbuzz.com/cricket-series/9237/indian-premier-league-2025/matches"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Launch headless browser
        page = await browser.new_page()
        await page.goto(url)
        
        # Ensure the page is fully loaded
        await page.wait_for_load_state('load')
        
        # Scrape the upcoming matches
        try:
            match_elements = await page.query_selector_all('a.cb-mtch-lst-link')
            if not match_elements:
                print("No matches found")
                return "No upcoming IPL matches found!"
            
            matches = []
            for match in match_elements:
                title = await match.query_selector('div.cb-col-60')
                time = await match.query_selector('div.cb-col-33.cb-col')

                title_text = await title.inner_text() if title else "Match"
                time_text = await time.inner_text() if time else "Time"

                link = await match.get_attribute('href')
                matches.append({
                    "title": title_text.strip(),
                    "time": time_text.strip(),
                    "link": f"https://m.cricbuzz.com{link}"
                })
            
            await browser.close()

            return matches

        except Exception as e:
            print(f"Error: {e}")
            await browser.close()
            return "An error occurred while fetching the matches."

# Run the function and print results
async def main():
    matches = await get_upcoming_ipl_matches()
    if isinstance(matches, list):
        for match in matches:
            print(f"Title: {match['title']}")
            print(f"Time: {match['time']}")
            print(f"Link: {match['link']}")
            print("="*40)
    else:
        print(matches)

# Start the async function
if __name__ == "__main__":
    asyncio.run(main())
