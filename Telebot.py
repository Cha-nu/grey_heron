import telepot
import time

def handle(msg):
	chat_id = msg['chat']['id']
	command = msg['text']
	
	print('Command:  %s' , command)
	
	if command == '/start':
		bot.sendMessage(chat_id, "This bot is for detecting North Korea Trash-landen Balloons.\n ")
		print(chat_id)

token = "7340681503:AAGmzgZpPoStNrMHF2Bt536Bvs8o3dKNJ6o"
bot = telepot.Bot(token)

bot.message_loop(handle)
print ('I am listening..')

while 1:
	time.sleep(10)
