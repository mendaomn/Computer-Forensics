#!/usr/bin/python
import sys
import magic
import os

# defines
mimelist = "/etc/mime.types"

# check command line arg
if len(sys.argv) == 1:
	print "Using /etc/mime.types"
elif len(sys.argv) == 2:
	mimelist = sys.argv[1]
	print "Using "+mimelist
else:
	print "Usage: python script.py <mime.types>"
	exit()

# ask for directory to be traversed
dirname = raw_input("Insert directory to analyse: ")
print

flist = []
for root, dirs, files in os.walk(dirname):
	for fname in files:
		# guess file type
		mimetype = magic.from_file(root+"/"+fname, mime=True)
		# extract file extension
		ext = os.path.splitext(root+"/"+fname)[1][1:]
		# store tuple (filename, mimetype, extension)
		flist.append({ "name":root+"/"+fname, "type":mimetype, "ext":ext, "found": -1})

# go through /etc/mime.types (or user provided file) and for every entry check if it's a match with any of the files
# stop reading the file as soon as every file has been matched
filecount = 0
nfile = len(flist)
f = open(mimelist, "r")
for line in f:
	if filecount == nfile:
		break
	if line[0] == "#" or line == "":
		continue
	words = line.split()
	wc = len(words)
	if wc == 0:
		continue
	if wc == 1:
		mtype = words[0]
		expected_ext = "no_ext"
	if wc == 2:
		mtype = words[0]
		expected_ext = words[1]
	if wc > 2:
		mtype = words[0]
		expected_ext = words[1:len(words)]
	for curr_f in flist:
		guess = curr_f["type"]
		actual_ext = curr_f["ext"]
		filename = curr_f["name"]
		if guess == "application/octet-stream":
			curr_f["found"] = 0
			continue
		if mtype == guess:
			if wc > 2:
				for i in expected_ext: 
					if i == actual_ext:
						curr_f["found"] = 2
				if curr_f["found"] != 2:
					curr_f["found"] = 1
			if wc == 1:
				if actual_ext != "":
					curr_f["found"] = 1
				else:
					curr_f["found"] = 2
			if wc == 2:
				if expected_ext != actual_ext:
					curr_f["found"] = 1
				else:
					curr_f["found"] = 2
			if curr_f["found"] == 1:
				print "camouflaged file: "+filename
				print "  -  mime: "+guess
				print "  -  ext: "+actual_ext
				if type(expected_ext) == list:
					print "  -  expecting: "+" ".join(expected_ext)
				else:
					print "  -  expecting: "+expected_ext
				filecount += 1
			if curr_f["found"] == 2:
				print "trusted file: "+filename
				filecount += 1

f.close()
for curr_f in flist:
	if curr_f["found"] == -1:
		print "unidentified file: "+curr_f["name"]
		print "  -  "+curr_f["type"]+" is not present in mime types list" 
	if curr_f["found"] == 0:
		print "unidentified file: "+curr_f["name"]
		print "  -  mime type can't be recognised"
