#!/usr/bin/python
from classes.line import Line
from classes.point import Point
import subprocess

#function to convert hh:mm:ss.ns to ns
def time_conversion( str ):
	array = list()
	array = str.split(':')
	t = int(array[0])*3600+int(array[1])*60+float(array[2])
	return t

#call command and retrieve output
cmd = "tshark -r capture.pcap -2 -R tcp -T fields -e ip.src -e tcp.options.timestamp.tsval -e frame.time | sort -nk2 | uniq -u | awk '{print $1, $2, $NF}' "
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

found = list()
slopes = list()
ips = list()
#find slopes of lines between consecutive timestamps
for i in range(len(data) - 1):
	if data[i]["ip"] in ips:
		print ips
		continue
	if data[i]["ip"] != data[i+1]["ip"]:
		continue
	p1 = Point(data[i]["t"], data[i]["ts"])
	p2 = Point(data[i+1]["t"], data[i+1]["ts"])
	l = Line(p1, p2)
	#print "new line:", l, p1, p2
	for j in range (i+2, len(data)):
		p3 = Point(data[j]["t"], data[j]["ts"])
		#print "verifying", p3
		if not l.contains(p3):
			print "found natted ip:", data[j]["ip"]
			ips.append(data[j]["ip"])
	
'''
	if data[i]["ip"] not in found:
		p1 = data[i]
		p2 = data[i+1]
		if p1["ip"] != p2["ip"] or p1["ts"] == p2["ts"]:
			continue	
		if p1["ip"] not in ips:
			print "adding", p1["ip"]
			ips.append(p1["ip"])
			slopes[:] = []
		A = (p2["ts"] - p1["ts"]) / (p2["t"] - p1["t"])
		for s in slopes:
			if A - s > 100 or A-s < -100:
				found.append(p1["ip"])
				print p1["ip"], A
		slopes.append(A)
'''


