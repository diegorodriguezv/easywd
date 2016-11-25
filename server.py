#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import random

PORT_NUMBER = 80
PWD_SIZE = 20
SEPARATOR = "-"
combinations = []
dict = {}

def make_password():
    accum = 0
    summary = [(size,len(list)) for size,list in dict.iteritems()]
    chances = [(combi,calc_chances(combi)) for combi in combinations]
    choice = weighted_choice(chances)
    pwd = ""
    for size in choice:
        word = random.choice(dict[size])
        if pwd:
            pwd += SEPARATOR + word
        else:
            pwd += word
    return pwd 

def calc_chances(combi):
    result = 1
    for size in combi:
        result *= len(dict[size])
    return result

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"

def find_combinations(partial=[]):
    sizes = dict.keys()
    target = PWD_SIZE
    if partial:
        s = sum(partial)
        l = s + len(SEPARATOR) * (len(partial) - 1)
    else:
        l = 0
    if l == target:
        print "found combi: %s (%s)" % (partial, len(partial))
        combinations.append(partial)
    if l >= target:
        return  # if we reach the number why bother to continue
    for i in range(len(sizes)):
        size = sizes[i]
        find_combinations(partial + [size])

def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest

# load word file into a dict where:
#   key: length
#   val: list of words of that length
def load_dict():
    word_lengths = {}
    with open("dict-es.txt") as f:
        lines = f.readlines()
    from collections import defaultdict
    results = defaultdict(list)
    for line in lines:
        word = line.strip()
        wlen = len(word)
        word_lengths[word] = wlen
        results[wlen].append(word)
    return results

#This class will handle any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(make_password())
        return

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    #Wait forever for incoming http requests
    dict = load_dict()
    find_combinations()
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()

