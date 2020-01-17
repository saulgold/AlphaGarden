from flask import Flask
import os
import pyrebase

app = Flask(__name__)

config = {
  "apiKey": os.environ.get("FIREBASE_API_KEY"),
  "authDomain": "alphagarden-3d4f7.firebaseapp.com",
  "databaseURL": "https://alphagarden-3d4f7.firebaseio.com",
  "projectId": "alphagarden-3d4f7",
  "storageBucket": "alphagarden-3d4f7.appspot.com",
  "serviceAccount": "alphagarden-3d4f7-firebase-adminsdk-tll4n-2648401a5b.json",
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

@app.route('/get_file/<filename>', methods=['GET'])
def get_file(filename):
  return storage.child(filename).get_url(None)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)