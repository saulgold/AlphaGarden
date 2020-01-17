from flask import Flask
import os
import pyrebase
import requests

app = Flask(__name__)

config = {
  "apiKey": os.environ.get("FIREBASE_API_KEY"),
  "authDomain": "alphagarden-3d4f7.firebaseapp.com",
  "databaseURL": "https://alphagarden-3d4f7.firebaseio.com",
  "projectId": "alphagarden-3d4f7",
  "storageBucket": "alphagarden-3d4f7.appspot.com",
  "serviceAccount": "alphagarden-3d4f7-firebase-adminsdk-tll4n-2648401a5b.json",
}

openweathermap_api_key = os.environ.get("OPENWEATHERMAP_API_KEY")

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

@app.route('/get_file/<filename>', methods=['GET'])
def get_file(filename):
  return storage.child(filename).get_url(None)

@app.route('/current_weather', methods=['GET'])
def current_weather():
  res = requests.get('https://api.openweathermap.org/data/2.5/weather?appid=' + openweathermap_api_key + '&q=Berekely,usa&units=imperial')
  # TODO: once api key activates, return temp
  print(res)
  return 'test'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)