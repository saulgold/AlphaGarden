from flask import Flask, request
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

# date is in MM_DD_YYYY format
@app.route('/get_overhead/<date>', methods=['GET'])
def get_overhead(date):
  numerical_date = int(date[:2] + date[3:5] + date[6:])
  extension = '.jpg' if numerical_date <= 1122020 else '.bmp'
  return storage.child('overheads/' + date + '_cal' + extension).get_url(None)
  
@app.route('/get_timelapse/<date>', methods=['GET'])
def get_timelapse(date):
  # TODO: Standardize timelapse video file name
  return storage.child('timelapses/' + date + '.mp4').get_url(None)

@app.route('/current_weather', methods=['GET'])
def current_weather():
  res = requests.get('https://api.openweathermap.org/data/2.5/weather?appid=' + openweathermap_api_key + '&q=Berekely,usa&units=imperial')
  # TODO: once api key activates, return temp
  print(res)
  return 'test'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)