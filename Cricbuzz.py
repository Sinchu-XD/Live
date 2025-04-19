import requests
import argparse

API_KEY = "814d366d83msh97b8ba89155c2a8p140352jsn4c9a3b3bb565"  # Replace with your actual RapidAPI Key
API_HOST = "cricket-live-line1.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

# ✅ Fetch Upcoming Matches
def get_upcoming_matches():
    url = "https://cricket-live-line1.p.rapidapi.com/matches/upcoming"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        matches = response.json()
        print("\nUpcoming Matches:\n")
        for i, match in enumerate(matches):
            print(f"{i+1}. {match['team1']} vs {match['team2']} - {match['date']} | Match ID: {match['match_id']}")
    else:
        print(f"Failed to fetch matches. Status code: {response.status_code}")

# ✅ Fetch Live Score of Match
def get_live_score(match_id):
    url = f"https://cricket-live-line1.p.rapidapi.com/match/{match_id}/score"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        score = response.json()
        print(f"\nLive Score for Match ID {match_id}:\n")
        print(f"{score['team1']}: {score['team1_score']}")
        print(f"{score['team2']}: {score['team2_score']}")
    else:
        print(f"Failed to fetch score. Status code: {response.status_code}")

# ✅ Fetch Ball-by-Ball Commentary
def get_live_commentary(match_id):
    url = f"https://cricket-live-line1.p.rapidapi.com/match/{match_id}/commentary"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        commentary = response.json()
        print(f"\nLive Commentary for Match ID {match_id}:\n")
        for ball in commentary:
            print(f"Over {ball['over']}.{ball['ball']}: {ball['text']}")
    else:
        print(f"Failed to fetch commentary. Status code: {response.status_code}")

# ✅ Command Line Interface
def main():
    parser = argparse.ArgumentParser(description="Cricket Live Line CLI Tool")
    parser.add_argument('--test', choices=['upcoming', 'score', 'commentary'], required=True, help="What to test")
    parser.add_argument('--match_id', type=str, help="Match ID (required for score or commentary)")

    args = parser.parse_args()

    if args.test == "upcoming":
        get_upcoming_matches()
    elif args.test == "score":
        if not args.match_id:
            print("❌ Please provide --match_id to fetch score.")
            return
        get_live_score(args.match_id)
    elif args.test == "commentary":
        if not args.match_id:
            print("❌ Please provide --match_id to fetch commentary.")
            return
        get_live_commentary(args.match_id)

if __name__ == "__main__":
    main()
