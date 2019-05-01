from http.server import BaseHTTPRequestHandler
from object_size import imageProcessing
import json

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(str("Image processing").encode())
        return

    def do_POST(self):
        self.send_response(200)
        content_length = int(self.headers.get('Content-length'))
        post_data = self.rfile.read(content_length)
        json_data = json.loads(post_data)
        image_url = json_data['imageURL']
        scar_id = json_data['scarID']
        imageURL, scarID, length, width, SA, colour = imageProcessing(image_url, scar_id)
        post_json = json.dumps({"scarID": scarID,
				"imageURL": imageURL,
				"scarLength": length,
				"scarWidth": width,
				"scarSA": SA,
				"scarRGB": colour})
        self.wfile.write(post_json)
        return