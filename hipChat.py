import json
import requests

def sendUpdate(vendors, test):
  data = open('keys.json')
  keys = json.load(data)
  data.close()

  url = 'https://api.hipchat.com/v1/rooms/message'
  auth_token = keys['access_token']

  message = 'Hey guys! Here are the vendors at 5th and Minna for today: '
  message += ", ".join(vendors)
  message += "."

  realRoomId = '1054347'
  testRoomId = '1049099'

  room_id = testRoomId if test else realRoomId

  options = {
    "room_id": room_id,
    "auth_token": auth_token,
    "from":"Markan",
    "message":message
  }

  r = requests.get(url, params=options)
  print options
  print message

if __name__ == '__main__':
  sendUpdate(['vendor1','vendor2','vendor3'], True)
