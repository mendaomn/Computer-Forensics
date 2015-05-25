#!/usr/bin/python
import sys
import magic
import os.path

#defines
mimelist = "/etc/mime.types"
filename = "badfile.fag"

# check command line arg
if len(sys.argv) == 1:
	print "Using /etc/mime.types"
elif len(sys.argv) == 2:
	mimelist = sys.argv[1]
	print "Using "+mimelist
else:
	print "Usage: python script.py <mime.types>"
	exit()

# get mime type through magic bindings
guess = magic.from_file(filename, mime=True)
actual_ext = os.path.splitext(filename)[1][1:]
print guess, actual_ext
# check such a type against /etc/mime.types or input file
#### extract extension corresponding to such a mime type from mime.types
#### compare expected extension with actual one

# !!!! some type has more than one exT!!


f = open(mimelist, "r")
for line in f:
	if line[0] == "#" or line == "":
		continue
	words = line.split()
	if len(words) == 2:
		mtype = words[0]
		expected_ext = words[1]
	else:
		mtype = line
		expected_ext = ""
	print mtype, expected_ext
	if mtype == guess and expected_ext != actual_ext:
		print "File "+filename+" camouflaged"
f.close()

