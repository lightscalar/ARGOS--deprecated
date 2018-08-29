import http.server
import socketserver
import os

PORT = 8080

if __name__ == "__main__":
    web_dir = "/Users/mjl/dev/mnfi/argos/dist"
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
    print("Serving at port " + str(PORT))
    httpd.serve_forever()
