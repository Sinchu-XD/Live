import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://www.cricbuzz.com"

# IPL 2025 Series ID (as of now)
IPL_SERIES_ID = "7607"

async def get_upcoming_ipl_matches():
    url = f"{BASE_URL}/cricket-series/{IPL_SERIES_ID}/indian-premier-league-2025/matches"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")
    matches = []

    match_cards = soup.select(".cb-col.cb-col-100.cb-ltst-wgt-hdr .cb-col.cb-col-100.cb-mtch-blk")

    for card in match_cards:
        try:
            status = card.select_one(".cb-text-live, .cb-text-complete, .cb-text-preview")
            if status and "upcoming" not in status.text.lower():
                continue

            title = card.select_one(".text-bold").text.strip()
            time = card.select_one(".schedule-date").text.strip()
            venue = card.select_one(".cb-ovr-flo.cb-text-complete").text.strip()
            teams = " vs ".join([t.text.strip() for t in card.select(".cb-hmscg-tm-nm")])
            link = BASE_URL + card.find("a")["href"]

            matches.append({
                "title": title,
                "time": time,
                "venue": venue,
                "teams": teams,
                "link": link
            })
        except:
            continue

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
