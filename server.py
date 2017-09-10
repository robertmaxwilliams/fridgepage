#!/usr/bin/env python
 
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import urllib
import time

def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    address = s.getsockname()[0]
    print("My ip is: ", address)
    s.close()
    return address
    

def read_html(path):
    with open(path, 'rb') as file:
        return file.read()
   # with open(path, 'r') as myfile:
    #  return myfile.read().replace('\n', '')

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        parsed_path = urlparse.urlparse(self.path)
        print(parsed_path)
        if len(parsed_path.path) < 3:
            self.wfile.write(read_html("index.html"))
            return
        #message =str(parsed_path.query)
        #print("message???:",  message)
 
        # Send message back to client
        #message = "Hello world!"

        # Write content as utf-8 data
        self.wfile.write(read_html(parsed_path.path[1:]))
        return

  def do_POST(self):
    arduino.write('off'.encode())
    length = int(self.headers['Content-Length'])
    post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
    # You now have a dictionary of the post data
    print("Toggle light")
    #self.wfile.write(read_html().encode("utf-8"))
    self.wfile.write(read_html("index.html"))

    time.sleep(0.1)
    arduino.write('on'.encode())
 
    
#setup arduino
import serial
#has to be modified if unplugged
arduino = serial.Serial('/dev/cu.usbserial-AL00UA1L', 9600, timeout=.1)
    
def run():
  arduino.write('on'.encode())
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = (get_ip(), 80)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run() 
