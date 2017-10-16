import itertools
import json
import random
import urllib2
import sys
import time
import requests
import threading
from datetime import datetime
import datetime as DT


# COLORS
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan
BL = '\033[30m' # black
UND = '\033[4m' # underline
BLINK = '\033[5m' # blink

# GET THE ADMIN FILE READY IN CASE THERE IS NO ADMIN FILE YET
admin_file = open('ADMINS.txt', 'a')
admin_file.close()

# LISTS
obj_list = []
logins = ['username:password'] #THIS IS WHERE YOUR ADMIN ACCOUNTS ARE
user_objects = [] # LIST TO HOLD OBJECTS WHEN THE USERS LOGIN

title = '''
---------------------------------------------------------------
|        ____           __                                    |
|       /  _/___  _____/ /_____ _____ __________ _____ ___    |
|       / // __ \/ ___/ __/ __ `/ __ `/ ___/ __ `/ __ `__ \   |
|     _/ // / / (__  ) /_/ /_/ / /_/ / /  / /_/ / / / / / /   |
|    /___/_/ /_/____/\__/\__,_/\__, /_/   \__,_/_/ /_/ /_/    |
|               ____        __/____/                          |
|              / __ )____  / /_                               |
|             / __  / __ \/ __/                               |
|            / /_/ / /_/ / /_                                 |
|           /_____/\____/\__/                                 |
|                                                             |
|                                        @the.red.team        |
|                                                             |
---------------------------------------------------------------'''


print(title)


print('Bot start time -> ' + str(datetime.now().date()) + ' | ' + str(datetime.now().time()))

#if len(sys.argv) < 4:
#	print('  Usage: python ' + str(sys.argv[0]) + ' [USERNAME] [PASSWORD] [PROTOCOL] [COMMENT?]\n')
#	print('Example: python ' + str(sys.argv[0]) + ' hacker_123 password123 4 True\n')
#	print('Example: python ' + str(sys.argv[0]) + ' xex.starter_pack.modz fake123 4 False\n')
#	print('Protocol:')
#	print('	1 - Follow 120 pages/day')
#	print('	2 - Follow 240 pages/day')
#	print('	3 - Follow 360 pages/day')
#	print('	4 - Follow 480 pages/day')
#	print('	5 - Follow 600 pages/day')
#	print('	6 - Follow 720 pages/day')
#	print('	7 - Follow 840 pages/day')
#	print('\nComments On?:')
#	print('	A comment chosen randomly from you list will be posted\nEvery 80th like to prevent spam flags')



# Now lets put it into one line
#try:
#	mode = int(sys.argv[3])
#except:
#	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] You did not select a valid protocol')
#	sys.exit()
	
#try:
#	global interation
#	iteration = sys.argv[4]
#	if (str(iteration) != 'False') and (str(iteration) != 'false'):
#		iteration = True
#except:
#	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] You did not select a valid comment protocol')
#	sys.exit()

#if mode == 120:
#	x = 120
#elif mode == 240:
#	x = 240
#elif mode == 360:
#	x = 360
#elif mode == 480:
#	x = 480
#elif mode == 600:
#	x = 600
#elif mode == 720:
#	x = 720
#elif mode == 840:
#	x = 840
#else:
#	x = 960



# URLS FOR VARIOUS FUNCTIONS
url = 'https://www.instagram.com/'
url_login = 'https://www.instagram.com/accounts/login/ajax/'
url_logout = 'https://www.instagram.com/accounts/logout/'

user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
				  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

class UserProfile:
	uid = ''
	conn = None
	ip = ''


# CLASS TO STORE USER INFORMATION
class bot:
	def __init__(self):
		self.tags = []
		self.comments_list = []
		self.ready_to_follow = []
		self.ready_to_like = []
		self.ready_to_comment = []
		self.commented = []
		self.liked_media = []
		self.followed_users = []
	session = None
	token = None
	x = 0
	cycle_grace_time_s = 0
	unfollow_count_global = 0
	comments = 0
	unfollow_count_global = 0
	following = 0
	followers = 0
	username = ''
	password = ''
	following_file = ''
	tag_file = ''
	comment_file = ''
	comment_bool = False
	
	liking_bool = False
	following_bool = False
		
	liking_grace = True
	following_grace = True

	running = True
	
	id = ''


# FUNCTION TO START NETWORK CAPABILITIES ON THE SERVER
def socket_create():
	global s
	global st
	try:
		host = ''
		port = 11006 #THE PORT FOR THE BOTS TO CONNECT
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Created first socket')
	except socket.error as msg:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + ']Could not create socket: ' + str(msg))
	try:
		s.bind((host, port))
		s.listen(5)
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Bound first socket')
	except socket.error as msg:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + ']Could not bind socket: ' + str(msg) + "\n" + "Retrying...")
		sys.exit()


	
# FUNCTION TO GET PROGRESS
def get_progress(obj):
	if len(obj.followed_users) > 500:
		for f in obj.followed_users:
			obj.followed_users.remove(f)
	if len(obj.liked_media) > 500:
		for l in obj.liked_media:
			obj.liked_media.remove(l)
	if len(obj.ready_to_comment) > 200:
		for c in obj.ready_to_comment:
			obj.ready_to_comment.remove(c)
	if len(obj.commented) > 500:
		for c in obj.commented:
			obj.commented.remove(c)
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(obj.username) + '] Users followed by bot -> ' + str(len(obj.followed_users)) + '/' + str(len(obj.ready_to_follow)))
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(obj.username) + '] Users unfollowed by bot -> ' + str(obj.unfollow_count_global))
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(obj.username) + '] Media liked by bot -> ' + str(len(obj.liked_media)) + '/' + str(len(obj.ready_to_like)))
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(obj.username) + '] Comments posted by bot -> ' + str(len(obj.commented)) + '/' + str(len(obj.ready_to_comment)))

#FUNCTION TO UNFOLLOW USERS
def unfollow(s, obj):
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'NOTICE'+W+'] [' + str(obj.username) + '] Starting UNFOLLOW cycle...')
	unfollow_count = 0
	with open(str(obj.username) + '_following.txt') as f:
		followed = f.readlines()

	original = len(followed)
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+T+'ACTION'+W+'] [' + str(obj.username) + '] Checking for users ready to be unfollowed -> ' + str(original))
	for user in followed:
		user = user.replace('\n', '')
		the_date, id = user.split('|')
		today = DT.date.today()
		seven_days_ago = today - DT.timedelta(days=7)
		if (datetime.strptime(the_date, '%Y-%m-%d').date() <= seven_days_ago) and (str(id) != str(obj.id)):
			url = 'https://www.instagram.com/web/friendships/' + str(id) + '/unfollow/'			
			unfollow_status = s.post(url)
			if int(unfollow_status.status_code) == 200:
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'UNFOLLOW'+W+'] [' + str(obj.username) + '] Unfollowed user with ID -> ' + str(id))
				user = user + '\n'
				followed.remove(user)
				unfollow_count = unfollow_count + 1
				obj.unfollow_count_global = obj.unfollow_count_global + 1
				time.sleep(60)
			else:
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'UNFOLLOW'+W+'] [' + str(obj.username) + '] Could not unfollow user with ID -> ' + str(id))

		if unfollow_count >= 120:
			break

	file = open(str(obj.username) + '_following.txt', 'w')
	for remaining_user in followed:
		remaining_user = remaining_user.replace('\n', '')
		file.write(remaining_user + '\n')
	file.close()
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+T+'ACTION'+W+'] [' + str(obj.username) + '] Users remaining to be unfollowed -> ' + str(len(followed)) + '/' + str(original))

# FUNCTION TO COMMENT ON MEDIA
def comment(s, media, comment, obj):
	id = media['id']
	url = 'https://www.instagram.com/web/comments/' + str(id) + '/add/'
	full_comment = {'comment_text': comment}
	post_comment = s.post(url, data = full_comment)
	if int(post_comment.status_code) == 200:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+B+'COMMENT'+W+'] [' + str(obj.username) + '] Posted comment to media ' + str(id) + ' -> ' + str(comment))
		obj.comments = obj.comments + 1
	else:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'COMMENT'+W+'] [' + str(obj.username) + '] Could not post comment to media ' + str(id) + ' -> ' + str(comment) + ' -> ' + str(post_comment.status_code))
		
# FUNCTION TO GET LIST OF MEDIA FROM TAG SEARCH
def get_media_by_tag(s, tag, obj):
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+T+'ACTION'+W+'] [' + str(obj.username) + '] Loading media from tag -> ' + str(tag))
	url = 'https://www.instagram.com/explore/tags/' + str(tag) + '/?__a=1'
	try:
		got = s.get(url)
		data = json.loads(got.text)
		media = list(data['tag']['media']['nodes'])
		return media
	except Exception, e:
		media = []
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] [' + str(obj.username) + '] There was an error -> ' + str(e))
		return media

# FUNCTION TO GET MEDIA INFO BEFORE LIKING
def get_media_info(media):
	list = []
	for med in media:
		id = str(med['owner']['id'])
		entry = id
		list.append(entry)
	return list	

# FUNCTION TO LIKE MEDIA
def like_media_list(s, med, obj):
#	for med in media:
	id = med['id']
	url = 'https://www.instagram.com/web/likes/' + str(id) + '/like/'
	try:
		if str(id) not in obj.liked_media:
			liked = s.post(url)
			obj.liked_media.append(str(id))
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+P+'LIKE'+W+'] [' + str(obj.username) + '] Liked tagged media with ID -> ' + str(id))
		else:
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'LIKE'+W+'] [' + str(obj.username) + '] Already liked tagged media with ID -> ' + str(id))
	except Exception, e:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] [' + str(obj.username) + '] There was an error in like -> ' + str(e))

# FUNCTION TO FOLLOW LIST OF MEDIA OWNERS
def follow_owner_list(s, owner, obj):
#	for owner in owners:
	if str(owner) != str(obj.id):
		url = 'https://www.instagram.com/web/friendships/' + str(owner) + '/follow/'
		try:
			if str(owner) not in obj.followed_users:
				follow = s.post(url)
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+O+'FOLLOW'+W+'] [' + str(obj.username) + '] Followed user with ID -> ' + str(owner))
				following_file = open(str(obj.username) + '_following.txt', 'a')
				following_file.write(str(DT.date.today()) + '|' + str(owner) + '\n')
				following_file.close()
				obj.followed_users.append(str(owner))
			else:
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'FOLLOW'+W+'] [' + str(obj.username) + '] Already following user with ID -> ' + str(owner))
		except Exception, e:
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] [' + str(obj.username) + '] There was an error in follow -> ' + str(e))
	else:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ACTION'+W+'] [' + str(obj.username) + '] Cannot follow yourself -> ' + str(owner))


# FUNCTION TO RESOLVE USERNAME TO INSTAGRAM ID
def get_user_id_by_login(s, username):
	url = 'https://www.instagram.com/' + str(username) + '/?__a=1'
	info = s.get(url)
	data = json.loads(info.text)
	id = data['user']['id']
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(username) + '] Instagram ID -> ' + str(id))

	return id
	
# FUNCTION TO GET FOLLOWER/FOLLOWS COUNT
def get_follow_counts(s, username):
	url = 'https://www.instagram.com/' + str(username) + '/?__a=1'
	try:
		r = s.get(url)
		user_info = json.loads(r.text)

		follows = user_info['user']['follows']['count']
		followers = user_info['user']['followed_by']['count']
		
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(username) + '] Followers -> ' + str(followers))
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(username) + '] Following -> ' + str(follows))


		return follows, followers
	except Exception, e:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] [' + str(username) + '] There was an error getting following/follower count -> ' + str(e))
	

# FUNCTION TO LOGIN AND GATHER INFO
def login(obj):

	# ESTABLISH REQUEST SESISON
	obj.session = requests.Session()
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+W+'LOGIN'+W+'] [' + str(obj.username) + '] Attempting to login...')
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+W+'LOGIN'+W+'] [' + str(obj.username) + '] Username -> ' + str(obj.username))
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+W+'LOGIN'+W+'] [' + str(obj.username) + '] Password -> ' + ('*' * len(obj.password)))
	obj.session.cookies.update({
		'sessionid': '',
		'mid': '',
		'ig_pr': '1',
		'ig_vw': '1920',
		'csrftoken': '',
		's_network': '',
		'ds_user_id': ''
	})
	login_post = {
		'username': obj.username,
		'password': obj.password
	}
	obj.session.headers.update({
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': accept_language,
		'Connection': 'keep-alive',
		'Content-Length': '0',
		'Host': 'www.instagram.com',
		'Origin': 'https://www.instagram.com',
		'Referer': 'https://www.instagram.com/',
		'User-Agent': user_agent,
		'X-Instagram-AJAX': '1',
		'X-Requested-With': 'XMLHttpRequest'
	})
	#s.
	# ACTUALLY LOGIN HERE
	r = obj.session.get(url)
	obj.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
	time.sleep(5 * random.random())
	login = obj.session.post(
		url_login, data=login_post, allow_redirects=True)
	obj.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
	csrftoken = login.cookies['csrftoken']
	time.sleep(5 * random.random())

	# DETERMINE WHETHER OR NOT IT WAS SUCCESSFUL
	if login.status_code == 200:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'LOGIN'+W+'] [' + str(obj.username) + '] Successful login')
		r = obj.session.get('https://www.instagram.com/')
		finder = r.text.find(obj.username)
		if finder != -1:
			obj.id = str(get_user_id_by_login(obj.session, obj.username))
			obj.following, obj.followers = get_follow_counts(obj.session, obj.username)
			login_status = True
		else:
			login_status = False
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'LOGIN'+W+'] [' + str(obj.username) + '] Your login credentials were incorrect')
			obj.running = False
	else:
		obj.running = False
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'LOGIN'+W+'] [' + str(obj.username) + '] There was a connection error when trying to login')
		
	return obj.session, csrftoken

# FUNCTION TO LOGOUT ONCE THE WORK IS DONE
def logout(obj, s, csrftoken):
	try:
		logout_post = {'csrfmiddlewaretoken': csrftoken}
		logout = s.post(url_logout, data=logout_post)
		login_status = False
		print('\n[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'LOGOUT'+W+'] [' + str(obj.username) + '] Successful logout')
		for rem_obj in obj_list:
			if rem_obj.username == obj.username:
				obj_list.remove(rem_obj)
				break
	except Exception, e:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'LOGOUT'+W+'] [' + str(obj.username) + '] There was an error while logging out -> ' + str(e))
		




# FUNCTION TO CONTROL FOLLOW PROTOCOL
def follow_time(s, obj):
	count = 0
	while obj.running == True:
		for owner in obj.ready_to_follow:
			if obj.running == False:
				break
			obj.following_grace = False
			obj.following_bool = True
			follow_owner_list(s, owner, obj)
			obj.ready_to_follow.remove(owner)
			count = count + 1

			# THIS IS TO MAINTIAN YOUR DAILY RATE
			if count < 120:
				time.sleep(30)
			elif count >= 120:
				count = 0
				obj.following_grace = True
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'NOTICE'+W+'] [' + str(obj.username) + '] Finished FOLLOW cycle | waiting ' + str(obj.cycle_grace_time_s) + ' until next cycle')
				unfollow_thread = threading.Thread(target = unfollow, args = (s, obj,))
				unfollow_thread.daemon = True
				unfollow_thread.start()
				time.sleep(obj.cycle_grace_time_s)
		time.sleep(5)
		if obj.following_bool == True:
			obj.following_bool = False

# FUNCTION TO CONTROL LIKE PROTOCOL
def like_time(s, obj):
	iteration_count = 0
	count = 0
	while obj.running == True:
		for med in obj.ready_to_like:
			if obj.running == False:
				break
			obj.liking_grace = False
			obj.liking_bool = True
			like_media_list(s, med, obj)
			obj.ready_to_like.remove(med)
			count = count + 1

			# COMMENT
			#iteration_count = iteration_count + 1
			#if (iteration_count >= 80) and (iteration == True):
			#	iteration_count = 0
			#	try:
			#		comment(s, med, random.choice(comments_list))
			#	except Exception, e:
			#		print('Ahhh shit -> ' + str(e))
			# THIS IS TO MAINTIAN YOUR DAILY RATE
			if count < 120:
				time.sleep(5)
			elif count >= 120:
				count = 0
				obj.liking_grace = True
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'NOTICE'+W+'] [' + str(obj.username) + '] Finished LIKE cycle | waiting ' + str(obj.cycle_grace_time_s) + ' until next cycle')
				time.sleep(obj.cycle_grace_time_s)
		time.sleep(5)
		if obj.liking_bool == True:
			obj.liking_bool = False	
			
# FUNCTION TO CONTROL COMMENT RATE
def comment_time(s, obj):
	if str(obj.comment_bool) == 'True':
		print('[!] Comments will be posted...')
	while obj.running == True:
		if str(obj.comment_bool) == 'True':
			for com in obj.ready_to_comment:
				if obj.running == False:
					break
				try:
					if com not in obj.commented:
						comment(s, com, random.choice(obj.comments_list), obj)
						obj.ready_to_comment.remove(com)
						obj.commented.append(com)
				except Exception, e:
					print('Ahhhhh shit -> ' + str(e))
				time.sleep(400)
				if len(obj.ready_to_comment) == 0:
					print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'NOTICE'+W+'] [' + str(obj.username) + '] Finished COMMENT cycle | waiting until next LIKE cycle')
		else:
			time.sleep(5)

# FUNCTION TO CONTROL TIMING PROTOCOL
def timing(s, obj):
	while obj.running == True:
		if ((obj.liking_grace != True) and (obj.liking_bool == True)) or ((obj.following_grace != True) and (obj.following_bool == True)):
			time.sleep(300)
			obj.following, obj.followers = get_follow_counts(s, obj.username)
			get_progress(obj)
			try:
				file_entry = '         username: ' + str(obj.username) + '\n'
				file_entry = file_entry + '        following: ' + str(obj.following) + '   \n'
				file_entry = file_entry + '        followers: ' + str(obj.followers) + '   \n'
				file_entry = file_entry + '  followed by bot: ' + str(len(obj.followed_users)) + '/' + str(len(obj.ready_to_follow)) + '\n'
				file_entry = file_entry + 'unfollowed by bot: ' + str(obj.unfollow_count_global) + '   \n'
				file_entry = file_entry + '     liked by bot: ' + str(len(obj.liked_media)) + '/' + str(len(obj.ready_to_like)) + '\n'
				file_entry = file_entry + ' commented by bot: ' + str(len(obj.commented)) + '/' + str(len(obj.ready_to_comment)) + '\n'
				file_entry = file_entry + '          running: ' + str(obj.running) + '\n'

			except Exception as e:
				file_entry = str(e)
			file = open(str(obj.username) + '_progress.txt', 'w')
			file.write(file_entry)
			file.close()
		else:
			time.sleep(10)

def check_running(obj):
	file = open('stop_clients.txt', 'a')
	file.close()
	while obj.running == True:
		with open('stop_clients.txt') as f:
			stop_clients = f.readlines()

		for client in stop_clients:
			client_username, client_password = client.replace('\n', '').split(':::')
			if (str(client_username) == str(obj.username)) and (str(client_password) == str(obj.password)):
				obj.running = False
				stop_clients.remove(client)
		if obj.running == False:
			file = open('stop_clients.txt', 'w')
			for new_client in stop_clients:
				file.write(new_client)
			file.close()
		time.sleep(1)

def file_check():
	while 1:
		try:
			with open('stop_clients.txt') as f:
				stop_clients = f.readlines()
	
			for file_client in stop_clients:
				match = False
				username, password = file_client.replace('\n', '').split(':::')
				for obj in obj_list:	
					if (str(obj.username) == str(username)) and (str(obj.password) == str(password)):
						match = True
	
				if match == False:
					stop_clients.remove(file_client)
	
			if len(obj_list) == 0:
				asdf = open('stop_clients.txt', 'w')
				asdf.close()
			rebuild = open('stop_clients.txt', 'w')
			for new_client in stop_clients:
				rebuild.write(new_client)
			rebuild.close()
		
			time.sleep(1)
		except Exception as e:
			print('[!] Error in file_check -> ' + str(e))


def obj_driver(new_user):
	try:	
		new_user = new_user.replace('\n', '')
		# LOGIN INFO
		obj = bot()
		obj.username, obj.password, new_protocol, obj.comment_bool = new_user.split(':::')

		obj.x = new_protocol
			
		# LOGIN AND GET USER INFO
		obj.session, obj.token = login(obj)

		# START A LIKE TIMER
		like_thread = threading.Thread(target=like_time, args=(obj.session, obj,))
		like_thread.daemon = True
		like_thread.start()

		# START A FOLLOW TIME
		follow_thread = threading.Thread(target=follow_time, args=(obj.session, obj,))
		follow_thread.daemon = True
		follow_thread.start()
		
		# START A COMMENT THREAD
		comment_thread = threading.Thread(target = comment_time, args = (obj.session, obj,))
		comment_thread.daemon = True
		comment_thread.start()

		# START A PROGRESS THREAD
		progress_thread = threading.Thread(target = timing, args = (obj.session, obj,))
		progress_thread.daemon = True
		progress_thread.start()

		# CHECK IF STILL RUNNING
		check_running_thread = threading.Thread(target = check_running, args = (obj,))
		check_running_thread.daemon = True
		check_running_thread.start()

		# SET THE BOTS PACE
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(obj.username) + '] Daily target follow count -> ' + str(new_protocol))

		obj.cycle_grace_time_s = (((24 - (( 60 * (int(obj.x) / 120)) / 60)) * 60) * 60) / (int(obj.x) / 120)

		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(obj.username) + '] There will be a total of ' + str(int(new_protocol)/120) + ' cycles')
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(obj.username) + '] Your cyclic grace period will be -> ' + str(obj.cycle_grace_time_s) + ' seconds')
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] [' + str(obj.username) + '] Your comment iteration is -> ' + str(obj.comment_bool))

		obj_list.append(obj)

		while obj.running == True:
			if (obj.liking_bool == False) and (obj.following_bool == False):

				# POPULATE TAG LIST
				obj.tags = []

				
				file = open(str(obj.username) + '_tags.txt', 'a')
				file.close()
				with open(str(obj.username) + '_tags.txt') as f:
					lines = f.readlines()
				if len(lines) == 0:
					obj.running = False
					break
				
	#			# LOAD THE LIST OF TAGS
				for line in lines:
					if str(line).replace('\n', '') not in obj.tags:
						obj.tags.append(str(line).replace('\n', ''))
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+W+'ACTION'+W+'] [' + str(obj.username) + '] Tags loaded -> ' + str(len(obj.tags)))
				
				
				# POPULATE COMMENTS LIST
				obj.comments_list = []

				
				comment_file = open(str(obj.username) + '_comments.txt', 'a')
				comment_file.close()
				with open(str(obj.username) + '_comments.txt') as cf:
					comment_lines = cf.readlines()
					

				for comment_line in comment_lines:
					if str(comment_line).replace('\n', '') not in obj.comments_list:
						obj.comments_list.append(str(comment_line).replace('\n', ''))
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+W+'ACTION'+W+'] [' + str(obj.username) + '] Comments loaded -> ' + str(len(obj.comments_list)))

				#s.
				for tag in obj.tags:
					if obj.running == False:
						break
					# GET BOT TODO LIST READY
					media = get_media_by_tag(obj.session, str(tag), obj)
					for med in media:
						if med not in obj.ready_to_like:
							obj.ready_to_like.append(med)
							obj.ready_to_comment.append(med)
					print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+T+'ACTION'+W+'] [' + str(obj.username) + '] Media loaded -> ' + str(len(obj.ready_to_like)))
						
					# GET MEDIA OWNERS
					owners = get_media_info(media)
					for own in owners:
						if own not in obj.ready_to_follow:
							obj.ready_to_follow.append(own)
					print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+T+'ACTION'+W+'] [' + str(obj.username) + '] Media owners found -> ' + str(len(obj.ready_to_follow)))
				

					time.sleep(10)
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'NOTICE'+W+'] [' + str(obj.username) + '] Finished retrieving all media | Waiting for next cycle to retrieve more')
			else:
				time.sleep(1)
		logout(obj, obj.session, obj.token)

	except KeyboardInterrupt:
		logout(obj, obj.session, obj.token)
		sys.exit()



# USER INTERFACE
def clientHandler(obj):

	# HELP MENU FOR THE USER
	help = '\n!clear - Clear the screen\n'
	help = help + '!help - Display this menu\n'
	help = help + '!ID - List UIDs and IPs of connected bots\n'
	help = help + '!keyLog <bot id> - Stream bot key strokes in real time\n'
	help = help + '!keyLog stop <bot id> - Stop streaming bot key strokes in real time\n'
	help = help + '!exit - Exit your session\n\n'

	obj.conn.send(str.encode(str(title) + '\n\n\n--------------------------------------------------------\n' + str(help) + '\n--------------------------------------------------------\n\n'))

	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Client handler started')


	# WHILE LOOP TO CONITNUOUSLY TAKE COMMANDS FROM USER
	# THIS WILL NOT EXIT UNLESS THE USER ENTERS '!exit' OR THE USER DISCONNECTS
	while 1:
		try:
			obj.conn.send(str.encode('[' + str(len(bot_objects)) + ']' + str(obj.uid) + '@KeyLogger> '))
			cmd = str(obj.conn.recv(1024).decode('ascii')).replace('\n', '').replace('\r', '')
			if cmd == '!ID':
				obj.conn.send(str.encode('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] GETTING VICTIM IDs\n'))
				for bot in bot_objects:
					obj.conn.send(str.encode('Bot ID -> ' + str(bot.uid) + ' | IP -> ' + str(bot.ip) + '\n'))
			elif cmd == '!clear':
				obj.conn.send(str.encode(chr(27) + "[2J"))
			elif cmd == '!help':
				obj.conn.send(str.encode(help))
			elif cmd == '!exit':
				obj.conn.close()
				user_objects.remove(obj)
				break

		except Exception as e:
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] There was an error -> ' + str(e))
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Client disconnected: ' + obj.uid + '')
			try:
				user_objects.remove(obj)
			except:
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Exception')
				break



# FUNCTION TO ALLOW THE CLIENT TO LOGIN TO THE SERVER
def inter_login(obj):
	valid = False
	counte = 0
	attempts = 0
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Login thread started')
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
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Attempted: ' + str(attempts))
		cred = username + ':' + password
		cred = cred.replace('\n', '').replace('\r', '')
		with open('ADMINS.txt') as f:
			from_file = f.readlines()

		for line in from_file:
			print(line.replace('\n', ''))
			if line.replace('\n', '') not in logins:
				print('Added new login to local list')
				logins.append(line.replace('\n', ''))

		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Credentials presented: ' + cred)
		cont = False
		if cred in logins:
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Successful ADMIN login')
			logn = open('login.txt', 'a')
			logn.write('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Successful Administrator login with ' + str(username) + ' from IP: ' + str(obj.ip) + '\n')
			logn.close()
			obj.conn.send(str.encode('Valid Administrator Login\n\n\n\n'))
			time.sleep(2)
			obj.conn.send(str.encode(chr(27) + "[2J"))


			# THE USER HAS OFFICIALLY LOGGED IN HERE
			obj.conn.send(str.encode('\n\n\t\t\t\t\tInstagram Bot Terminal\n\n' + dev + '\n\n'))
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Sending to a clientHandler thread')
			valid = True
			if attempts < 5:
				obj.uid = str(username)
				user_objects.append(obj)
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] len(user_objects) -> ' + str(len(user_objects)))
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Logged in users\n------------------------------------')
				for user in user_objects:
					print(user.uid)
				print('------------------------------------')
				clientHandler(obj)
			break
		if attempts >= 4:
			attempts = 10
			obj.conn.send(str.encode('You have provided invalid credentials too many times. Connection will now close...\n'))
			obj.conn.close()
			break



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
		logn.write('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Got a user connection from: ' + str(obj.ip) + '\n')
		logn.close()

		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] Starting login thread')
		user_thread = threading.Thread(target = inter_login, args = (obj,))
		user_thread.daemon = True
		user_thread.start()

		time.sleep(0.5)



try:
	yup = threading.Thread(target = file_check)
	yup.daemon = True
	yup.start()
	while 1:
		estab = open('new_clients.txt', 'a')
		estab.close()
	
		targ_client = ''

		with open('new_clients.txt') as f:
			clients = f.readlines()
		if len(clients) != 0:
	
			for client in clients:
				new_thread = threading.Thread(target = obj_driver, args = (client,))
				new_thread.daemon = True
				new_thread.start()
				clients.remove(client)
			file = open('new_clients.txt', 'w')
			for re_client in clients:
				file.write(re_client)
			
			file.close()
	
		time.sleep(1)
except KeyboardInterrupt:
	for obj in obj_list:
		obj.running = False
	time.sleep(5)
	sys.exit()
