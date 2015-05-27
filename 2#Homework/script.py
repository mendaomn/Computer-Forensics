#!/usr/bin/python
import sys
import os
import shutil
import subprocess
import math
import time
from progress.bar import ChargingBar

# defines
directory = "forensics_homework2_menduni_subdir"
if os.path.exists(directory):
	shutil.rmtree(directory)
tmpfile = "forensics_homework2_menduni_tmpfile"

# check command line arg
if len(sys.argv) != 2:
	print "Usage: python script.py <filesystem>"
	exit()

# retrive filesystem from command line
fs = sys.argv[1]

# store block size
cmd = "fsstat "+fs+" | grep \"Block Size\""
ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
bsize = ps.communicate()[0].split()[-1]

# obtain list of files
cmd = "fls -r -F "+fs
ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
fls_o = ps.communicate()[0]
entries = fls_o.split('\n')
files = []
for entry in entries[:-1]:
	fields = entry.split()
	if fields[0] == "r/r":
		# store inode and name
		inode = fields[1][:-1]
		filename = fields[2]
		# store size
		cmd = "istat "+fs+" "+inode+" | grep size"
		ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		grep_o = ps.communicate()[0]
		size = grep_o.split()[1]
		# store last block
		# look for direct blocks
		cmd = "istat "+fs+" "+inode+" | awk '/Direct/,/^$/'"
		ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		grep_o = ps.communicate()[0]
		blocks = grep_o.split('\n')[1:-1]
		index = 1
		for i in range(1, len(blocks)):
			if blocks[-i] != "":
				index = i
				break
		last_block = blocks[-index].split()[-1]
		# store file info
		f = {"inode":inode, "name":filename, "size":size, "block": last_block}
		files.append(f)

bar_max = len(files)
bar = ChargingBar('Progress:', max=bar_max)
# loop through files and read last block
for f in files:
	cmd = "dd if="+fs+" bs="+bsize+" skip="+f["block"]+" count=1 > "+tmpfile+" 2> /dev/null"
	ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	output = ps.communicate()[0]
	# compute how many bytes to expect in last block
	nblocks = int(math.ceil(int(f['size'])/float(bsize)))
	slack = nblocks*int(bsize) - int(f['size'])
	actualbytes = int(bsize) - slack
	# read slack space
	tmp = open(tmpfile, "rb")
	bcount = 0
	hidden=""
	try:
	    byte = tmp.read(1)
	    while byte != "":
	        bcount += 1
	        if bcount > actualbytes and ord(byte) != 0x0:
	        	hidden+=byte
	        byte = tmp.read(1)
	finally:
	    tmp.close()
	os.remove(tmpfile)
	# use subdir to store result files
	# create file named after inode and write hidden bytes 
	if hidden != "":
		if not os.path.exists(directory):
			os.makedirs(directory)
		f_out = open(directory+"/"+f["inode"], 'w')
		try:
			f_out.write(hidden)
		finally:
			f_out.close()
	bar.next()
bar.finish()