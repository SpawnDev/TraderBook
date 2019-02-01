import clearbit
import json
import sys

clearbit.key = 'sk_1f384bd939bf8ad7dcd711a4d6859c3c'

if len(sys.argv) < 2:
  sys.exit('Usage: cli.py [email]')

email = sys.argv[1]
lookup = clearbit.Enrichment.find(email=email, stream=True)

if lookup != None:
  print(json.dumps(lookup['person'], sort_keys=True, indent=4))
  print(json.dumps(lookup['company'], sort_keys=True, indent=4))
else:
  print('Email not found')