import httpx
from bs4 import BeautifulSoup

MOBILE_URL = "https://m.cricbuzz.com/cricket-series/9237/indian-premier-league-2025/matches"

async def get_upcoming_ipl_matches():
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient() as client:
        res = await client.get(MOBILE_URL, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")
    matches = []

    for card in soup.select("div.match-list > div"):
        try:
            title = card.find("a").text.strip()
            link = "https://m.cricbuzz.com" + card.find("a")["href"]
            details = card.find("div", class_="schedule-date").text.strip()
            matches.append({
                "title": title,
                "time": details,
                "link": link
            })
        except Exception:
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
