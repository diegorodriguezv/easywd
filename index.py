#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgi
import cgitb
import easywd

cgitb.enable()
print "Content-Type: text/plain;charset=utf-8"
print
args = cgi.FieldStorage()
lang = "es"
size = 20
sep = "-"
if "lang" in args:
    if args["lang"].value in ["en", "es"]:
        lang = args["lang"].value
if "size" in args:
    try:
        if int(args["size"].value) in range(4, 50 + 1):
            size = int(args["size"].value)
    except ValueError:
        pass
if "sep" in args:
    sep = args["sep"].value
html = easywd.make_password(lang, size, sep)
print html
