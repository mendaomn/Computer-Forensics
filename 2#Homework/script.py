#!/usr/bin/python
import sys
import os
import subprocess
import math
import time
from progress.bar import ChargingBar


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
		# look for indirect blocks first
		cmd = "istat "+fs+" "+inode+" | grep -A 10000 \"Indirect Blocks\""
		ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		grep_o = ps.communicate()[0]
		# look for direct blocks if no indirect blocks were used
		if not grep_o:
			cmd = "istat "+fs+" "+inode+" | grep -A 10000 \"Direct Blocks\""
			ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			grep_o = ps.communicate()[0]
		blocks = grep_o.split('\n')[1:-1]
		last_block = blocks[-1].split()[-1]
		# store file info
		f = {"inode":inode, "name":filename, "size":size, "block": last_block}
		files.append(f)

bar_max = len(files)
bar = ChargingBar('Progress:', max=bar_max)
# loop through files and read last block
for f in files:
	cmd = "dd if="+fs+" bs="+bsize+" skip="+f["block"]+" count=1 > tmp 2> /dev/null"
	ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	output = ps.communicate()[0]
	# compute how many bytes to expect in last block
	nblocks = int(math.ceil(int(f['size'])/float(bsize)))
	slack = nblocks*int(bsize) - int(f['size'])
	actualbytes = int(bsize) - slack
	# read slack space
	tmp = open("tmp", "rb")
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
	os.remove("tmp")
	#if hidden:
		#print hidden
	bar.next()
	time.sleep(0.2)
bar.finish()