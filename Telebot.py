import telepot
import time
import os
import requests
import subprocess
import json
import socket

#telegram msg handle
def handle(msg):
	chat_id = msg['chat']['id']
	command = msg['text']
	
	
	print('Command: ', command)
	
	if command == '/start':
		bot.sendMessage(chat_id, "This bot is for detecting North Korea Trash-landen Balloons.\n ")
		print(chat_id)
	
	if command == '/run':
		os.system("python webcam.py")
		print("webcam run")
		bot.sendMessage(chat_id, "A suspected balloon object has been detected!\n ")
		bot.sendMessage(chat_id, "location: " + str(latitude) + ", " + str(longitude) + "\nCity: " + city)
		bot.sendPhoto(chat_id, photo = open("photo.jpg", 'rb'))
        # pixhawk.py run
        subprocess.run(['python3', 'pixhawk.py'])
        send_location_to_pixhawk(latitude, longitude)

# socket을 사용하여  pixhawk에게 gps 좌표를 보냄
def send_location_to_pixhawk(latitude, longitude, city):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))  # 서버 IP와 포트 설정
    
    data = f"{latitude},{longitude}"
    client_socket.send(data.encode())
    
    client_socket.close()

#get location based on ip	
def getLocationIpstack(api_key):
    try:
        result = subprocess.run("curl ifconfig.co", shell=True, capture_output=True, text=True)
        ip = result.stdout.strip()
        
        print(ip)
        
        url = f"http://api.ipstack.com/{ip}?access_key={api_key}"
        response = requests.get(url)
        data = json.loads(response.text)
        
        global latitude
        global longitude
        global city

        latitude = data["latitude"]
        longitude = data["longitude"]
        city = data["city"]

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
		


token = "7340681503:AAGmzgZpPoStNrMHF2Bt536Bvs8o3dKNJ6o"
api_key = "a0a0f44a512653fae3fe2c9eb83d8e12"
bot = telepot.Bot(token)

getLocationIpstack(api_key)


bot.message_loop(handle)
print ('I am listening..')

while 1:
	time.sleep(10)
