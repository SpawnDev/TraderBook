import os, sys, requests, json, fileinput
from random import randint

import clearbit

def Signup(server, api, number_of_users):
	for x in range(number_of_users):
		user = "korisnik" + str(x)
		email = user + "@gmail.com"
		password = "lozinka" + str(x)

		r = requests.post(server +"users/api/signup/", data={'username': user, 'email': email, 'password1': password, 'password2': password, 'givenName':"", 'familyName':""},
			headers={'Authorization': "Bearer " + api})
		r = r.json()
		print(r)
	print(str(number_of_users) + " Users created!")

def CreatePosts(server, api, max_posts_per_user, number_of_users):
	count = 0
	for x in range(number_of_users):
		user = "korisnik" + str(x)
		posts_user = randint(1, max_posts_per_user)

		for y in range(posts_user):
			post = "tekstU" + str(x) + "P" + str(y)
			r = requests.post(server +"users/api/post/", data={'user': user, 'post_text':post},
				headers={'Authorization': "Bearer " + api})
			r = r.json()
			print(r)
			count = count + 1
		print(str(posts_user) + " Posts created for user" + user)
	print(str(count) + " Posts created in total!")

def TokenRequest(email, password):
	server = input("Write Django development server address. Leave blank if it is: http://127.0.0.1:8000/ ")
	if server == "":
		server = "http://127.0.0.1:8000/"
		print("ye")

	r = requests.post(server+"api/token/", data={'email': email, 'password': password})
	r = r.json()
	access = r["access"]

	with open("bot.config", "a") as f:
		f.write(server + "\n")
		f.write(access + "\n")
	print("\nJWT authentication token. Lasts for 2 hours before need for refresh:")
	print(access)
	print("\nbot.config file has been updated, you can close this window now.")

def BotConfiguration():
	print("\nNow, you will be asked to setup configuration for bot activities. \n")
	number_of_users = input("How many users you wish to create: ")
	max_posts_per_user = input("Maximum number of posts per user: ")
	max_likes_per_user = input("Maximum number of likes per user: ")

	with open("bot.config", "a") as f:
		f.write(number_of_users + "\n")
		f.write(max_posts_per_user + "\n")
		f.write(max_likes_per_user + "\n")

def FirstBotActivity():
	config = [line.rstrip('\n') for line in open('bot.config')]
	server = config[0]
	api = config[1]
	number_of_users = int(config[2])
	max_posts_per_user = int(config[3])
	max_likes_per_user = int(config[4])

	Signup(server, api, number_of_users)
	CreatePosts(server, api, max_posts_per_user, number_of_users)

def Clearbit():
	clearbit.key = 'sk_1f384bd939bf8ad7dcd711a4d6859c3c'

	email = input("Type in email you want additional public data for: ")
	lookup = clearbit.Enrichment.find(email=email, stream=True)

	if lookup != None:
		print('Email found!')
		print(lookup)
	else:
		print('Email not found')
		return ["null", "null"]

def Emailhunter():
	email = input("Type in email you want to check legitimity: ")
	req = {"api_key":"82000e0248ddba37454fae879dcfd7ee1a7742d5", "email":email}
	odg = requests.get("https://api.hunter.io/v2/email-verifier", params=req)
	data = odg.json()
	data = data["data"]
	print(data)
