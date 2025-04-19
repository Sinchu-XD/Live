# CricGuruTerminal.py
import time
import httpx
import os

RAPIDAPI_KEY = "7d3b7f92b5mshb73a3d1bff87355p1c15aajsn23b6207b41be"  # replace with your actual RapidAPI Key
headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "cricket-live-line1.p.rapidapi.com"
}

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_match_list():
    url = "https://cricket-live-line1.p.rapidapi.com/live-match-list"
    response = httpx.get(url, headers=headers)
    data = response.json()
    matches = data.get("data", [])
    for idx, match in enumerate(matches[:5], start=1):  # show top 5
        print(f"{idx}. {match['team1']} vs {match['team2']} - Match ID: {match['match_id']}")
    return matches

def fetch_live_data(match_id):
    with httpx.Client() as client:
        score_res = client.get(f"https://cricket-live-line1.p.rapidapi.com/match-detail?match_id={match_id}", headers=headers)
        score_data = score_res.json()
        
        comm_res = client.get(f"https://cricket-live-line1.p.rapidapi.com/commentary?match_id={match_id}", headers=headers)
        comm_data = comm_res.json()

        return score_data, comm_data

def format_output(score, commentary):
    striker = score.get("striker", {}).get("name", "Unknown")
    non_striker = score.get("non_striker", {}).get("name", "Unknown")
    overs = score.get("overs", "??")
    runs = score.get("score", "N/A")
    
    ball = commentary[0].get("ball", "??.?")
    text = commentary[0].get("text", "")
    
    return f"""
CRICKET GURU LIVE:

{ball} 🎾 {runs}

{striker.upper()} ON STRIKE ✔️

🅾️ {overs} OVER 🅾️

📟 SCORECARD 📟
{striker} :- {score['striker'].get('runs', 0)}({score['striker'].get('balls', 0)})
{non_striker} :- {score['non_striker'].get('runs', 0)}({score['non_striker'].get('balls', 0)})

📢 {text}
""".strip()

def main():
    print("📡 Fetching Live Matches...\n")
    matches = get_match_list()
    choice = input("\nEnter match number (1-5) to watch live: ")

    try:
        match = matches[int(choice) - 1]
    except:
        print("Invalid match number.")
        return

    match_id = match["match_id"]
    print(f"🎬 Starting Live Feed for Match ID: {match_id}\n")

    last_ball = ""

    try:
        while True:
            score_data, comm_data = fetch_live_data(match_id)

            if not comm_data.get("commentary"):
                print("Waiting for live commentary...")
                time.sleep(5)
                continue

            latest_comm = comm_data["commentary"][0]
            if latest_comm["text"] != last_ball:
                clear()
                output = format_output(score_data, comm_data["commentary"])
                print(output)
                last_ball = latest_comm["text"]
            
            time.sleep(8)
    except KeyboardInterrupt:
        print("\n🛑 Live session ended.")

if __name__ == "__main__":
    main()
