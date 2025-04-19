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

        # Extract the match data (Title, Link, etc.) from the main page
        matches = await page.query_selector_all('a.w-full.bg-cbWhite')  # Target the anchors with the match titles

        match_details = []
        for match in matches:
            title = await match.inner_text()  # Extract the match title
            link = await match.get_attribute('href')  # Get the link to match details

            # Store basic match information before navigating away
            title_parts = title.split('•')

            # Create a placeholder dictionary with the basic match details
            match_info = {
                'title': title_parts[0].strip(),
                'link': link
            }

            # Now go to the match details page to scrape extra information like date, time, and stadium
            await page.goto("https://m.cricbuzz.com" + link)
            await page.wait_for_load_state('load')  # Wait for the new page to load

            # Extract date, time, and stadium details
            match_date = await page.query_selector_eval('div.dates', 'el => el.innerText') or "N/A"
            match_time = await page.query_selector_eval('div.time', 'el => el.innerText') or "N/A"
            stadium = await page.query_selector_eval('div.stadium', 'el => el.innerText') or "N/A"

            # Add the additional details to the match dictionary
            match_info.update({
                'date': match_date.strip(),
                'time': match_time.strip(),
                'stadium': stadium.strip()
            })

            # Append the match details to the list
            match_details.append(match_info)

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
