#!/usr/bin/python
from classes.line import Line
from classes.point import Point
import subprocess
import sys

#function to convert hh:mm:ss.ns to ns
def time_conversion( str ):
	array = list()
	array = str.split(':')
	t = int(array[0])*3600+int(array[1])*60+float(array[2])
	return t

#check command line arg
if len(sys.argv) != 2:
	print "Usage: python script.py <pcapfile>"
	exit()

#retrive filename from command line
filein = sys.argv[1]

#call command and retrieve output
cmd = "tshark -r "+filein+" -2 -R tcp -T fields -e ip.src -e tcp.options.timestamp.tsval -e frame.time | sort -nk2 | uniq -u | awk '{print $1, $2, $NF}' "
ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output = ps.communicate()[0]

#fill data structure
count = 0
data = list()
for s in output.split():
	d=dict()
	if count == 0:
		ip=s
	if count == 1:
		ts=s
	if count == 2:
		t=s
		count = 0
		d={"ip":ip, "ts":int(ts), "t":time_conversion(t)}
		data.append(d)
	else:
		count+=1

#consider each packet as a "point" P = (time_of_capture, timestamp)
#connect with a line packets having same source IP address 
#if a packet doesn't belong to the line, then more than one host are behind the same IP address
curr_ip = "init"
for i in range(len(data) - 1):
	if (curr_ip != data[i]["ip"]):
		curr_ip = data[i]["ip"]
		if data[i]["ip"] != data[i+1]["ip"]:
			continue
		p1 = Point(data[i]["t"], data[i]["ts"])
		p2 = Point(data[i+1]["t"], data[i+1]["ts"])
		l = Line(p1, p2)
		for j in range (i+2, len(data)):
			p3 = Point(data[j]["t"], data[j]["ts"])
			l.setThreshold(data[j]["ts"] * 0.3)
			if not l.contains(p3):
				print data[j]["ip"]
				break


