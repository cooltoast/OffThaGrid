import json
import requests

def sendUpdate(vendors):
  data = open('keys.json')
  keys = json.load(data)
  data.close()

  url = 'https://api.hipchat.com/v1/rooms/message'
  auth_token = keys['access_token']

  if not vendors:
    message = 'Hey guys. Unfortunately there are no vendors at 5th and Minna today.'
  else:
    message = 'Hey guys! Here are the vendors at 5th and Minna for today: '
    message += ", ".join(vendors)
    message += "."

  room_id = keys['room_id']

  options = {
    "room_id": room_id,
    "auth_token": auth_token,
    "from":"Markan",
    "message":message
  }

  r = requests.get(url, params=options)
  print message

if __name__ == '__main__':
  sendUpdate(['vendor1','vendor2','vendor3'], True)
