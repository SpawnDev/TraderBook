import os, sys, requests, json, fileinput
from random import randint

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traderbook.settings')
try:
	from django.core.management import execute_from_command_line
except ImportError as exc:
	raise ImportError(
		"Couldn't import Django. Are you sure it's installed and "
		"available on your PYTHONPATH environment variable? Did you "
		"forget to activate a virtual environment?"
	) from exc
execute_from_command_line(sys.argv)

import django
django.setup()

from users.models import User, Post, Like

def LikePosts(server, api, number_of_users, max_likes_per_user):
	user_list = User.objects.order_by("-posts")
	usercount = user_list.count()
	print(user_list[0])
	for x in range(0, usercount-1):
		while user_list[x].likes < max_likes_per_user:
			posts = Post.objects.exclude(user = user_list[x].id).order_by("likes")
			print(posts)
			print(posts[0])
			if posts[0].likes != 0:
				break
			
			toLikeUser = posts[0].user
			print("to like user - " + str(toLikeUser))
			toLikeUserPosts = User.objects.get(username = toLikeUser).posts
			print(toLikeUserPosts)
			likingUser = user_list[x].username
			print(likingUser)
			user = toLikeUser
			post = randint(1, toLikeUserPosts)

			r = requests.post(server +"users/api/like/", data={'likingUser': likingUser, 'upvote': "True", 'user': user, 'post': str(post)},
				headers={'Authorization': "Bearer " + api})
			print("ODGOVOR:")
			print(r.content)
			user_list[x].likes = user_list[x].likes+1

	print(str(number_of_users) + " Users created!")

def SecondBotActivity():
	config = [line.rstrip('\n') for line in open('bot.config')]
	server = config[0]
	api = config[1]
	number_of_users = int(config[2])
	max_posts_per_user = int(config[3])
	max_likes_per_user = int(config[4])

	LikePosts(server, api, number_of_users, max_likes_per_user)

	print("\n Post liking has successfully finished. You can now go to HOST:PORT/admin panel and login with email: spawnthapro@gmail.com")
	print("\n email: spawnthapro@gmail.com")
	print("\n passw: admin")
	print("\n and review what has been done.")