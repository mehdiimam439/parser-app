import pyrebase


config = {
    "apiKey": "AIzaSyBsMT9l3gZTDkYUv3pCcQFHR8LeuvS4R18",
    "authDomain": "resume-parser-c757d.firebaseapp.com",
    "projectId": "resume-parser-c757d",
    "storageBucket": "resume-parser-c757d.appspot.com",
    "messagingSenderId": "985506727421",
    "appId": "1:985506727421:web:7fe95da1b903076abbc594",
    "databaseURL": "https://resume-parser-c757d-default-rtdb.firebaseio.com/",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
