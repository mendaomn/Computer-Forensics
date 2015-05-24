#!/usr/bin/python
import sys
import os
import subprocess

#functions 

#check command line arg
if len(sys.argv) != 2:
	print "Usage: python script.py <filesystem>"
	exit()

#retrive filesystem from command line
fs = sys.argv[1]
fs_info = os.statvfs(fs)
bsize = fs_info.f_bsize

'''
fls -> inodes and files
for each inode:
	istat -> direct blocks
	for last block:
		dd if=megafs bs=1024 skip=12357 count=1 > lastblock
'''
# obtain list of files
cmd = "fls -r "+fs
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

# 
cmd = "dd if=fs/megafs bs=1024 skip=12357 count=1 2> /dev/null"
ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
output = ps.communicate()[0]
