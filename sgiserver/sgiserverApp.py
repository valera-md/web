# server handling logic
#from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.server import HTTPServer, CGIHTTPRequestHandler
# enable CGI execution
import cgitb
cgitb.enable()

# config root  directory
# CGIHTTPRequestHandler.cgi_directories = ['/']
CGIHTTPRequestHandler.cgi_directories = ['/pages']

# create the server object
#webServer = HTTPServer(("127.0.0.1", 8000), SimpleHTTPRequestHandler) # Factory - design pattern
webServer = HTTPServer(("127.0.0.1", 8000), CGIHTTPRequestHandler)

# run the server
print("SERVER RUNNING ...")
webServer.serve_forever()

# 127.0.0.1:8000 - открыть в браузере, в браузере открывается корневая, рут папка, которая открыта в visual studio code
# 127.0.0.1:8000/pages/home.py
# attrib +r profile.py - назначает атрибут только для чтения файлу с именем profile.py