# from urllib.request import urlopen
# r = urlopen('https://www.python.org')
# r.read()


import requests

# getting information about a web page

r = requests.get('https://www.google.com/')
data = r.text

print(str(dict(r.cookies)))

s = requests.session()

print(str(dict(s.cookies)))

# don't do it fast because google will send u a mess
# print("Status code: ",r.status_code)
# print("Text: ",data)
