__author__ = 'MarioJ'

import HttpClient
import sys

# get the parameter that references URL
url = sys.argv[1]

# Instance the Http Client to make request from server
client = HttpClient.Client(str(url))

# Make POST request to server and get response
response = client.POST()

# print response on the screen
print response