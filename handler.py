import json
from process import imageProcessing

try:
  import unzip_requirements
except ImportError:
  pass

def main(event, context):

    post_data = event['request']
    json_data = json.loads(post_data)
    image_url = json_data['imageURL']
    scar_id = json_data['scarID']
    imageURL, scarID, length, width, SA, colour = imageProcessing(image_url, scar_id)

    body = {
        "scarID": scarID,
        "imageURL": imageURL,
        "scarLength": length,
        "scarWidth": width,
        "scarSA": SA,
        "scarRGB": colour
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    #print(response)
    return response

if __name__ == "__main__":
    data = {
        "imageURL": "https://res.cloudinary.com/nikolamus/image/upload/v1556297408/wounds-scars/tfk1zzbb26d63avaj1ib.png",
        "scarID": 1
    }
    eg = {
        "request": json.dumps(data)
    }
    main(eg, '')

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    # """
    # return {
    #     "message": "Go Serverless v1.0! Your function executed successfully!",
    #     "event": event
    # }
    # """
