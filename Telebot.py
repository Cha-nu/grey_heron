import telepot
import time

def handle(msg):
	chat_id = msg['chat']['id']
	command = msg['text']
	
	print('Command:  %s' , command)
	
	if command == '/start':
		bot.sendMessage(chat_id, "This bot is for detecting North Korea Trash-landen Balloons.\n ")

token = "7022578473:AAFNQzYIXD_8gE8IW7ca9lNuFO1Md3140fg"
bot = telepot.Bot(token)

bot.message_loop(handle)
print ('I am listening..')

while 1:
	time.sleep(10)
