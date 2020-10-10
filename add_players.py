import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# TODO: Use somesort of dynamic sdk / certificate so that others can use the script / project
cred = credentials.Certificate('kitsc-rl-tracker-firebase-adminsdk-7n65m-b894f2fb88.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection(u'Players').document(u'RandomMonkey')

doc_ref.set({
    "steam_id": "76561198274443758",
    "name": "RandomMonkey",
    "team_name": "",
    "steam_picture_url": "",
    "duel_rank": "",
    "duel_mmr": 0,
    "doubles_rank": "",
    "doubles_mmr": 0,
    "standard_rank": "",
    "standard_mmr": 0
})
