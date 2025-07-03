import firebase_admin
from firebase_admin import credentials, firestore, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r'C:\Users\TahaK\Desktop\AQ Monitoring\AQ_back\secret_firebase.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': '',
    'storageBucket': ''
})

# Get Firestore client
firestore_db = firestore.client()

def save_data_to_firebase(sensor_data):
    db.collection('sensor_readings').add(sensor_data)

# Get Realtime Database reference
realtime_db = db.reference('/')
