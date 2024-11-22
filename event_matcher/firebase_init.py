import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("coco-7f24e-firebase-adminsdk-xf6rb-875d97284f.json")
firebase_admin.initialize_app(cred)