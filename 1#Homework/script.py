#!/usr/bin/python
from subprocess import check_output
import shlex

#call command and retrieve output
cmd = "tshark -r capture.pcap -2 -R tcp -T fields -e ip.src -e ip.dst -e tcp.options.timestamp.tsval -e tcp.options.timestamp.tsecr"
args = shlex.split(cmd)
output = check_output(args)

#gather timestamps and ips from output
count = 0
data = list()
ts=0
for s in output.split():
	d=dict()
	if count == 0:
		ip=s
	if count == 2:
		ts=s
	if count == 3:
		count = 0
		d={"ip":ip, "ts":ts}
		data.append(d)
	else:
		count+=1

#perform subtraction among timestamps
for d in data:
	ts1 = d["ts"]
	print ts1
