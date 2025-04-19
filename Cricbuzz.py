import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://www.cricbuzz.com"

async def get_ipl_upcoming_matches():
    url = f"{BASE_URL}/cricket-series/7607/indian-premier-league-2025/matches"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")
    matches = []

    match_cards = soup.select(".cb-col.cb-col-100.cb-ltst-wgt-hdr .cb-col.cb-col-100.cb-mtch-blk")

    for card in match_cards:
        try:
            title = card.select_one(".text-bold").text.strip()
            link = BASE_URL + card.find("a")["href"]
            time = card.select_one(".schedule-date").text.strip()
            teams = card.select_one(".cb-ovr-flo.cb-hmscg-tm-nm").text.strip()
            venue = card.select_one(".cb-ovr-flo.cb-text-complete").text.strip()
            matches.append({
                "title": title,
                "time": time,
                "teams": teams,
                "venue": venue,
                "link": link
            })
        except Exception:
            continue

    return matches
