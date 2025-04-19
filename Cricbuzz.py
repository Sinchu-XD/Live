import asyncio
from playwright.async_api import async_playwright

async def get_upcoming_ipl_matches():
    url = "https://m.cricbuzz.com/cricket-series/9237/indian-premier-league-2025/matches"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Launch headless browser
        page = await browser.new_page()
        await page.goto(url)
        
        # Wait for the page to fully load
        await page.wait_for_load_state('load')

        # Print the page content for debugging
        page_content = await page.content()
        print(page_content)  # Output the page content to see if matches are loaded

        # You may want to stop here and manually inspect what elements contain match info

        await browser.close()
        return "Page printed. Inspect the content manually for further debugging."

# Run the function and print results
async def main():
    result = await get_upcoming_ipl_matches()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
