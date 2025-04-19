import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://www.cricbuzz.com"

async def get_live_matches():
    url = f"{BASE_URL}/cricket-match/live-scores"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    matches = soup.select(".cb-col.cb-col-100.cb-ltst-wgt-hdr .cb-col.cb-col-100.cb-col-rt.cb-font-12")
    match_list = []

    for match in matches:
        try:
            title = match.find("a").text.strip()
            link = BASE_URL + match.find("a")["href"]
            match_list.append({"title": title, "link": link})
        except:
            continue

    return match_list

async def get_score_and_commentary(link):
    async with httpx.AsyncClient() as client:
        res = await client.get(link)
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        score = soup.select_one(".cb-font-20.text-bold").text.strip()
        status = soup.select_one(".cb-text-live").text.strip()
        comms = soup.select(".cb-col.cb-col-100.cb-com-ln")
        last_ball = comms[0].text.strip() if comms else "No commentary yet."
    except:
        score, status, last_ball = "N/A", "Match not started or ended", "No commentary"

    return score, status, last_ball
  
