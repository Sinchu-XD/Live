import httpx
from bs4 import BeautifulSoup

MOBILE_SERIES_URL = "https://m.cricbuzz.com/cricket-series/9237/indian-premier-league-2025/matches"

async def get_upcoming_ipl_matches():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(MOBILE_SERIES_URL, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")
    matches = []

    match_blocks = soup.find_all("div", class_="cb-col cb-col-100 cb-ltst-wgt-hdr")

    for block in match_blocks:
        all_matches = block.find_all("a", href=True)
        for a in all_matches:
            title = a.text.strip()
            href = a["href"]
            if not title or "vs" not in title:
                continue
            link = f"https://m.cricbuzz.com{href}"
            parent_div = a.find_parent("div")
            time_tag = parent_div.find_next_sibling("div")
            time = time_tag.text.strip() if time_tag else "Time not found"

            matches.append({
                "title": title,
                "time": time,
                "link": link
            })

    return matches



async def get_live_score(link: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient() as client:
        res = await client.get(link, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    try:
        title = soup.select_one(".cb-nav-hdr.cb-font-18.line-ht24").text.strip()
        score = soup.select_one(".cb-font-20.text-bold").text.strip()
        status = soup.select_one(".cb-text-inprogress, .cb-text-live").text.strip()

        # Get recent balls
        commentary = soup.select(".cb-col.cb-col-100.cb-com-ln")
        recent_ball = commentary[0].text.strip() if commentary else "Commentary not available."

        return {
            "title": title,
            "score": score,
            "status": status,
            "recent": recent_ball
        }
    except:
        return None
