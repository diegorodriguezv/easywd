#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import easywd
import cgi

cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

lang = "es"
size = 20
sep = "-"
args = cgi.FieldStorage()
if "lang" in args:
    if args["lang"] in ["en", "es"]:
        lang = args["lang"]
if "size" in args:
    try:
        if int(args["size"]) in range(4, 50 + 1):
            size = int(args["size"])
    except ValueError:
        pass
if "sep" in args:
    sep = args["sep"]
html = easywd.make_password(lang, size, sep)
print html
