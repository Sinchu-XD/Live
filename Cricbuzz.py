import httpx
from bs4 import BeautifulSoup

async def get_upcoming_ipl_matches():
    url = "https://m.cricbuzz.com/cricket-series/9237/indian-premier-league-2025/matches"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    matches = []

    for tag in soup.select("a.cb-mtch-lst-link"):
        title = tag.select_one("div.cb-col-60").text.strip() if tag.select_one("div.cb-col-60") else "Match"
        time = tag.select_one("div.cb-col-33.cb-col").text.strip() if tag.select_one("div.cb-col-33.cb-col") else "Time"
        link = f"https://m.cricbuzz.com{tag['href']}"

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
