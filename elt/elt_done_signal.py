from http.server import HTTPServer, SimpleHTTPRequestHandler
from os import getenv


# Get the hostname and port from environment variables
hostname = str(getenv('HOSTNAME'))
port_no = int(getenv('PORT_NO'))

# Create an HTTP server
httpd = HTTPServer((hostname, port_no), SimpleHTTPRequestHandler)

# Run the server for 30 seconds
print(f"Server started at http://{hostname}:{port_no}")
httpd.timeout = 30
httpd.handle_request()  # Handle a single request, then stop
print("Server stopped after 30 seconds.")