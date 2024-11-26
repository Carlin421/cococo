import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("coco-7f24e-firebase-adminsdk-xf6rb-d85cf66aba.json")
firebase_admin.initialize_app(cred)