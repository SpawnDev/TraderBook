# TraderBook
Simple Django REST API based social network, with scripts to demonstrate API functionalities.

# Dependencies
Python libraries needed to run this project are: django, clearbit, djangorestframework, djangorestframework-simplejwt. I used pip install commands to get latest versions of each.

# Setup
To access traderbook, you need to start local server, "0. Run Local Server.bat" does that. While it is running, you can access it via HTML, login to admin account or signup new user account.

# Testing API
In order to automatically test API functionality, you should use rest of .bat files in order. 1. Makes bot.config file requested in test, which can me edited manually later on to adjust settings.

All .bat files run appropriate classes from bot_functions.py file, with some user input.

project was pre-made with sb.sqlite3 file, which contains initial migrations, as well as administrator account.
