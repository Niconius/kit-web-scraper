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

# TODO: Use somesort of dynamic sdk / certificate so that others can use the script / project
cred = credentials.Certificate('kitsc-rl-tracker-firebase-adminsdk-7n65m-b894f2fb88.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection(u'Players').document(u'KingInos')

doc_ref.set({
    "steam_id": "76561198020311715",
    "name": "KingInos",
    "team_name": "Greenkeepers",
    "steam_picture_url": "",
    "duel_rank": "",
    "duel_mmr": 0,
    "doubles_rank": "",
    "doubles_mmr": 0,
    "standard_rank": "",
    "standard_mmr": 0,
    "solo_standard_rank": "",
    "solo_standard_mmr": 0
})
