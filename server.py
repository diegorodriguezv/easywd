#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import easywd
import argparse
from urlparse import urlparse, parse_qs


# This class will handle any incoming request from
# the browser
class MyHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        if urlparse(self.path).path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            args = parse_qs(urlparse(self.path).query)
            lang = cmd_args.language
            if "lang" in args:
                if args["lang"][0] in ["en", "es"]:
                    lang = args["lang"][0]
            size = cmd_args.size
            if "size" in args:
                try:
                    if int(args["size"][0]) in range(4, 50 + 1):
                        size = int(args["size"][0])
                except ValueError:
                    pass
            sep = cmd_args.separator
            if "sep" in args:
                sep = args["sep"][0]
            html = easywd.make_password(lang, size, sep)
            self.wfile.write(html)
        else:
            self.send_response(404)
        return


def valid_port(string):
    msg = "%s is not a valid TCP port, try 1-65535" % string
    try:
        value = int(string)
    except:
        raise argparse.ArgumentTypeError(msg)
    if not 1 <= value <= 65535:
        raise argparse.ArgumentTypeError(msg)
    return value


def valid_size(string):
    msg = "%s is not a valid size, try 4-50" % string
    try:
        value = int(string)
    except:
        raise argparse.ArgumentTypeError(msg)
    if not 4 <= value <= 50:
        raise argparse.ArgumentTypeError(msg)
    return value


parser = argparse.ArgumentParser(description="Run a minimal web server that generates easywd passwords. "
                                             "Easy for humans to write in paper, remember, say over the "
                                             "phone or over the hallway. Cryptographically secure (for "
                                             "most purposes).")
parser.add_argument("-p", "--port", help="TCP port, 8080 if omitted", type=valid_port, default=8080)
parser.add_argument("-s", "--size", help="default password size, 20 if omitted", type=valid_size, default=20)
parser.add_argument("-l", "--language", help="default language, 'en' if omitted", choices=['en', 'es'], default="en")
parser.add_argument("-sep", "--separator", help="default word separator, '-' if omitted", default="-")
cmd_args = parser.parse_args()

port_number = cmd_args.port
try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(("", port_number), MyHandler)
    print "Started HTTP server on port", port_number
    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print "^C received, shutting down the web server"
    server.socket.close()
