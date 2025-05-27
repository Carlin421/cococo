import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("coco-7f24e-firebase-adminsdk-xf6rb-430d1c6d68.json")
firebase_admin.initialize_app(cred)