#!/usr/bin/python
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

#gather timestamps and ips from output
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
#perform subtraction among timestamps
for i in range(len(data) - 1):
	if data[i]["ip"] not in found:
		p1 = data[i]
		p2 = data[i+1]
	if p1["ip"] != p2["ip"]:
		continue	
	A = (p2["ts"] - p1["ts"]) / (p2["t"] - p1["t"])
	if A > 300:
		print "found", p1["ip"], A
		found.append(p1["ip"])
		continue



