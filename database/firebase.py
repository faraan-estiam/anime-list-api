import firebase_admin, pyrebase
from firebase_admin import credentials
from firebase_config import firebaseConfig

cred = credentials.Certificate('anime-list-api-private-key.json')
firebase_admin.initialize_app(cred)

firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()