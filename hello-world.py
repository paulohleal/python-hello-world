#!/usr/bin/python
import subprocess,os
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from datetime import datetime

PORT_NUMBER = 80

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

  data = "Default"

  #Handler for the GET requests
  def do_GET(self):
    if myHandler.data == "falha":
      self.send_response(500)
      self.send_header('Content-type','text/html')
      self.end_headers()
      self.wfile.write("Ultimo post indica falha!")
      self.wfile.write("POST = " + myHandler.data)
    else:
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      # Send the html message
      self.wfile.write("Version 2 <br>\n")
      self.wfile.write("*** Python - Hello World ! ***\n<br>")
      self.wfile.write("WELCOME_MSG: " + os.getenv('WELCOME_MSG', 'undef') )
      self.wfile.write("\n<br>")
      self.wfile.write("Hostname is: " + subprocess.check_output("uname -n", shell=True))
      self.wfile.write("\n<br>")
      self.wfile.write("Process ID: " + str(os.getpid()))
      self.wfile.write("\n<br>")
      now = datetime.now()
      self.wfile.write("Day: " + str(now.day) + "/" + str(now.month) + "/" + str(now.year))
      self.wfile.write("\n<br>")
      self.wfile.write("Time: " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
      self.wfile.write("\n<br>")
      self.wfile.write("Path: " + self.path)
      self.wfile.write("\n<br>")
      self.wfile.write("Ultimo post: " + myHandler.data)
    return


  #Handler for the POST requests
  def do_POST(self):
    if self.path=="/send":
      length = int(self.headers.getheader('content-length'))
      old = myHandler.data
      myHandler.data = self.rfile.read(length)
      self.send_response(200)
      self.end_headers()
      self.wfile.write("Era " + old + ". Foi escrito " + myHandler.data)
    else:
      self.send_response(400)
      self.end_headers()
    return


try:
  #Create a web server and define the handler to manage the
  #incoming request
  server = HTTPServer(('', PORT_NUMBER), myHandler)
  print 'Started httpserver on port ' , PORT_NUMBER

  #Wait forever for incoming htto requests
  server.serve_forever()

except KeyboardInterrupt:
  print '^C received, shutting down the web server'
  server.socket.close()
