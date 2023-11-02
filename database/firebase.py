import firebase_admin, pyrebase
from firebase_admin import credentials
import json
from dotenv import dotenv_values

env=dotenv_values('.env')

cred = credentials.Certificate(json.loads(env['FIREBASE_SERVICE_ACCOUNT_KEY']))
firebase_admin.initialize_app(cred)

firebase=pyrebase.initialize_app(json.loads(env['FIREBASE_CONFIG']))
db=firebase.database()
firebase_auth=firebase.auth()