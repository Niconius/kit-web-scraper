import requests
from bs4 import BeautifulSoup
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

game_mode_rows = {
    "duel": 1,
    "doubles": 2,
    "solo_standard": 3,
    "standard": 4
}

# Use the application default credentials
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'projectId': "kitsc-rl-tracker",
# })

# Use a service account
if not firebase_admin._apps:
    # TODO: Use somesort of dynamic sdk / certificate so that others can use the script / project
    cred = credentials.Certificate('kitsc-rl-tracker-firebase-adminsdk-7n65m-b894f2fb88.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

doc_snapshots = db.collection(u'Players').stream()

for doc_snapshot in doc_snapshots:
    doc = db.collection(u'Players').document(doc_snapshot.id)
    page = requests.get(f'https://rocketleague.tracker.network/profile/steam/{doc_snapshot.get("steam_id")}')
    soup = BeautifulSoup(page.content, 'html.parser')
    game_mode_stats = {}
    for game_mode_row in game_mode_rows:
        mmr = soup.findAll("div", {"class": "season-table"})[0].findChildren("table")[1].findChildren("tbody")[0].findChildren("tr")[game_mode_rows[game_mode_row]].findChildren("td")[3].contents[0]
        rank = soup.findAll("div", {"class": "season-table"})[0].findChildren("table")[1].findChildren("tbody")[0].findChildren("tr")[game_mode_rows[game_mode_row]].findChildren("td")[0].findChildren("img")[0]["src"]
        game_mode_stats[f"{game_mode_row}_rank"] = f"https://rocketleague.tracker.network/{rank}"
        game_mode_stats[f"{game_mode_row}_mmr"] = int(mmr.replace("\n", "").replace(",", ""))
    page = requests.get(f'http://steamcommunity.com/profiles/{doc_snapshot.get("steam_id")}')
    soup = BeautifulSoup(page.content, 'html.parser')
    steam_picture_url = soup.findAll("div", {"class": "playerAvatarAutoSizeInner"})[0].findChildren("img")[0]["src"]
    
    doc.update({
        "steam_picture_url": steam_picture_url,
        "duel_rank": game_mode_stats["duel_rank"],
        "duel_mmr": game_mode_stats["duel_mmr"],
        "doubles_rank": game_mode_stats["doubles_rank"],
        "doubles_mmr": game_mode_stats["doubles_mmr"],
        "standard_rank": game_mode_stats["standard_rank"],
        "standard_mmr": game_mode_stats["standard_mmr"],
        "solo_standard_rank": game_mode_stats["solo_standard_rank"],
        "solo_standard_mmr": game_mode_stats["solo_standard_mmr"],
    })
