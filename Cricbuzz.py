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

            # Split the title to get teams
            title_parts = title.split('•')

            # Extract date, time, and stadium from the match's page
            match_date = "N/A"
            match_time = "N/A"
            stadium = "N/A"

            # Go to the match details page to scrape extra information like date, time, and stadium
            await page.goto("https://m.cricbuzz.com" + link)
            await page.wait_for_load_state('load')

            # Extract date, time, and stadium details using 'evaluate'
            match_date = await page.query_selector('div.dates')
            if match_date:
                match_date = await match_date.evaluate('el => el.innerText')

            match_time = await page.query_selector('div.time')
            if match_time:
                match_time = await match_time.evaluate('el => el.innerText')

            stadium = await page.query_selector('div.stadium')
            if stadium:
                stadium = await stadium.evaluate('el => el.innerText')

            # Create match dictionary with all details
            match_details.append({
                'title': title_parts[0].strip(),
                'date': match_date.strip() if match_date else "N/A",
                'time': match_time.strip() if match_time else "N/A",
                'stadium': stadium.strip() if stadium else "N/A",
                'link': link
            })
        
        await browser.close()

        if match_details:
            return match_details
        else:
            return "No upcoming matches found!"

# Run the function and print results
async def main():
    result = await get_upcoming_ipl_matches()

    # Print the result in the requested format
    if isinstance(result, list):
        for match in result:
            print(f"**{match['title']}**:")
            print(f"- **Date**: {match['date']}")
            print(f"- **Time**: {match['time']}")
            print(f"- **Stadium**: {match['stadium']}")
            print(f"- **Link**: [Match Link](https://m.cricbuzz.com{match['link']})")
            print("\n---\n")
    else:
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
