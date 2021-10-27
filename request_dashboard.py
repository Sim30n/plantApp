import requests

# TODO: 
# - while 200
# - localhost env. 
#

r = requests.get("localhost")
print(r.status_code)