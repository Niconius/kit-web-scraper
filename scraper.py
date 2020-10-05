#!/usr/bin/env python3

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


if not firebase_admin._apps:
    # TODO: Use somesort of dynamic sdk / certificate so that others can use the script / project
    dirname = os.path.dirname(__file__)
    credfile = os.path.join(dirname, 'kitsc-rl-tracker-firebase-adminsdk-7n65m-b894f2fb88.json')
    cred = credentials.Certificate(credfile)
    firebase_admin.initialize_app(cred)

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(
    executable_path=sys.argv[1],
    options=chrome_options
)

db = firestore.client()

doc_snapshots = db.collection(u'Players').stream()

game_mode_rows = {
    "duel": 1,
    "doubles": 2,
    "standard": 4
}

for doc_snapshot in doc_snapshots:
    doc = db.collection(u'Players').document(doc_snapshot.id)
    steam_id = doc_snapshot.get("steam_id")
    driver.get(f'https://rocketleague.tracker.network/rocket-league/profile/steam/{steam_id}/overview')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_mmr = soup.find_all("div", class_="mmr")
    all_rank = soup.find_all("td", class_="icon-container")
    game_mode_stats = {}
    for game_mode_row in game_mode_rows:
        game_mode_stats[f"{game_mode_row}_rank"] = all_rank[game_mode_rows[game_mode_row]].find_all("img")[0]["src"]
        game_mode_stats[f"{game_mode_row}_mmr"] = int(all_mmr[game_mode_rows[game_mode_row]].text.replace(",", ""))
    page = requests.get(f'http://steamcommunity.com/profiles/{steam_id}')
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
    steam_picture_url = soup.findAll("div", {"class": "playerAvatarAutoSizeInner"})[0].findChildren("img", recursive=False)[0]["src"]
    
    doc.update({
        "steam_picture_url": steam_picture_url,
        "duel_rank": game_mode_stats["duel_rank"],
        "duel_mmr": game_mode_stats["duel_mmr"],
        "doubles_rank": game_mode_stats["doubles_rank"],
        "doubles_mmr": game_mode_stats["doubles_mmr"],
        "standard_rank": game_mode_stats["standard_rank"],
        "standard_mmr": game_mode_stats["standard_mmr"]
    })

driver.close()
