# TraderBook
Simple Django REST API based social network, with scripts to demonstrate API functionalities.

# Dependencies
Python libraries needed to run this project are: django, clearbit, djangorestframework, djangorestframework-simplejwt and python-dotenv. I used pip install commands to get latest versions of each.

# Setup
To make traderbook and test fuctionalities, you need to make migrations and create superuser/admin for server. Make sure to remember your superuser email and password for later.

After that you should run server and you are good to go!

# Testing API
In order to test API functionality, you should use functions provided in "bot_functions.py" file. I recommend opening a python instance in same folder, and run demostration like following:

import above mentioned file

	import bot_functions as bf

First you'll need to make a token for superuser in order to create multiple users via API:

	bf.token_request()

Next, you should edit 'bot.config' file, you can do it manually, or use a command:

	bf.bot_configuration()

In order to finish first task of singing up users and making posts, you can use following function:

	bf.first_bot_activity()

After it has been done, you can initialize second task of liking algo like so:

	bf.second_bot_activity()

Here all main requests are finished. Additionally, you can test out Clearbit implementation with following:

	bf.clearbit()

And Emailhunter by running its test function:

	bf.emailhunter()

# Feedback notes:

*API keys hardcoded inline* Fixed, now it uses environment variables to read API keys.

*Mixed tabs and spaces across files* Fixed, standardized everything to use tabs.

*Shipped SQLite file with applied migrations* Previously, I shipped it like this to make setup more convenient, but after further reading, now I understand why is it bad practice. Fixed.

*CamelCase top-level function names* Fixed, didn't pay enough attention to it, updated to lower_case_with_underscores as advised in PEP-8

*Post and like counts are prone to RC* I am not quite sure what did you mean by RC abbreviation.

*Too much print code. It’s not a production code, but it’s not a helloworld personal project either* Fixed, As someone who's been mainly working on personal projects, I do agree I use print code more often than I should. Definitely should have addressed that before sending out.

*Batch scripts* Fixed, working on personal projects and scripts did accustom me some to bad practices. Actively working on overcoming it.

*Way overkilled batch scripts* New update, fresh with 100% less batch scripts!
