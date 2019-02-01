from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import generic
from django.test.client import RequestFactory

from django.shortcuts import render, redirect
import requests, json, clearbit, sys

from django.http import HttpResponse
from django.template import loader
from .forms import SignupForm, PostForm, LikeForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User, Post, Like

def clearData(email):
	clearbit.key = 'sk_1f384bd939bf8ad7dcd711a4d6859c3c'

	email = email
	lookup = clearbit.Enrichment.find(email=email, stream=True)

	if lookup != None:
		print('Email found!')
		name = str(lookup['person']["name"]["givenName"])
		surname = str(lookup['person']["name"]["familyName"])
		rez = [name, surname]
		return rez
	else:
		print('Email not found')
		return ["null", "null"]


def myaccount(request):
	print("Radi eheheeee!!")
	posts_list = Post.objects.order_by("-created")
	template = loader.get_template("myaccount.html")
	context = {"posts_list": posts_list}
	return HttpResponse(template.render(context, request))

def emailcheck(email):
	req = {"api_key":"82000e0248ddba37454fae879dcfd7ee1a7742d5", "email":email}
	odg = requests.get("https://api.hunter.io/v2/email-verifier", params=req)
	data = odg.json()
	data = data["data"]
	print("Shit tekst - " + str(data["gibberish"]))
	print("SMTP check - " + str(data["smtp_check"]))
	if (data["gibberish"] == False and data["smtp_check"] == True):
		return True
	else:
		return False

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		print(request.POST.get('email'))
		huntercheck = emailcheck(request.POST.get('email'))
		if form.is_valid() and huntercheck == True:
			lookup = clearData(request.POST.get('email'))

			username = request.POST.get('username')
			raw_password = request.POST.get('password1')

			post_values = request.POST.copy()
			post_values["givenName"] = lookup[0]
			post_values["familyName"] = lookup[1]
			form = SignupForm(post_values)
			user = form.save()
			login(request, user)
			return redirect('home')
	else:
		form = SignupForm()
	return render(request, 'signup.html', {'form': form})

class SignupBot(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		form = SignupForm(data=request.data)
		huntercheck = emailcheck(request.data.get('email'))
		if form.is_valid() and huntercheck == True:
			lookup = clearData(request.data.get('email'))

			post_values = request.data.copy()
			if post_values["givenName"] == "":
				post_values["givenName"] = lookup[0]
			if post_values["familyName"] == "":
				post_values["familyName"] = lookup[1]

			form = SignupForm(post_values)
			form.save()
			return Response(form.data)
		return Response(form.errors)

class PostBot(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		form = PostForm(data=request.data)
	
		post_values = request.data.copy()
		user = User.objects.get(username = post_values["user"])
		post_values["user"] = str(user.id)
		form = PostForm(post_values)

		if form.is_valid():
			form.save()
			user.posts = user.posts+1
			user.save()
			return Response(form.data)
		return Response(form.errors)

class LikeBot(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		form = LikeForm(data=request.data)
	
		post_values = request.data.copy()
		user = User.objects.get(username = post_values["user"])
		liker = User.objects.get(username = post_values["likingUser"])

		userPosts = Post.objects.filter(user = str(user.id)).order_by('post_text')
		post = userPosts[int(post_values["post"])-1]

		post_values["user"] = str(liker.id)
		post_values["post"] = str(post.id)
		form = LikeForm(post_values)

		if post_values["upvote"] == "True":	# Like comment
			print("yeaaah, upvote!")

			try:
				Like.objects.get(user=liker.id, post=post.id)
				return Response(print("You already liked it!" + str(liker.id) + " post - " + str(post.id)))
			except Like.DoesNotExist:
				if form.is_valid():
					form.save()
					liker.likes = liker.likes+1
					liker.save()
					post.likes = post.likes+1
					post.save()
					return Response(form.data)
				return Response(form.errors)

		else:								# Unlike comment
			print("Dislike!")

			try:
				like = Like.objects.get(user=liker.id, post=post.id)
				print("got it")
				like.delete()
				liker.likes = liker.likes-1
				liker.save()
				post.likes = post.likes-1
				post.save()
				return Response(form.data)
			except Like.DoesNotExist:
				return Response(print("You can't dislike not liked comment..."))
		return Response(form.errors)
