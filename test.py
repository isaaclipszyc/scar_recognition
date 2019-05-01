import requests
import json

url =  "https://5newc9wj62.execute-api.us-east-1.amazonaws.com/default/scar-recognition-new-dev-scar-recognition"

post_json = json.dumps({"scarID": 1,
				        "imageURL": "https://res.cloudinary.com/nikolamus/image/upload/v1556297408/wounds-scars/tfk1zzbb26d63avaj1ib.png"})

response  = requests.post(url = url, json = post_json)
print(response)
