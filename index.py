#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import easywd
import cgi

cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

# cgi.test()
# print "Hello World!"
# defaults = {lang:"es", size:20, sep:"-"}
lang = "es"
size = 20
sep = "-"
args = cgi.FieldStorage()
if "lang" in args:
    if args["lang"][0] in ["en", "es"]:
        lang = args["lang"][0]
    if "size" in args:
        try:
            if int(args["size"][0]) in range(4, 50 + 1):
                size = int(args["size"][0])
        except ValueError:
            pass
    if "sep" in args:
        sep = args["sep"][0]
html = easywd.make_password(lang, size, sep)
print html
