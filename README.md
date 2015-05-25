# Computer-Forensics
Collection of exercises in computer forensics, related to the class taken at EURECOM

## Homework 1
Write a simple python script that, by invoking tshark, prints the IPs that are likely natted using the TCP timestamp option.
Requirements:
self-contained python script that uses tshark for the packet analysis
the tool should receive a pcap file as parameter and print the IP addresses that are likely natted.
you can test your script on this little pcap file

## Homework 2
Write a script that, using SleuthKit, checks all the sector slack at the end of each file in a ext3 partition and dumps the ones that contain data.
Requirements:
self-contained python script that either use the SleuthKit bindingins or invoke it as a subprocess
the tool should check all file in a filesystem specified as parameter
shows a progress bar to tell the user the percentage of files analyzed so far
for each file that has data in the slack space, create a file in a subdirectory named with the inode number and containing the slack bytes

## Homework 3
Write a python script to detect camouflaged files. The script should use the python magic bindings compare the results with the mime types (extracted from /etc/mime.types by default or by a file specified as parameter)
The script should take as input a directory and recursively analyze its content.

## Homework 4
Collect a memory snapshot of a linux machine. Install volatility 2.4 (use the official release, not the development version), build the profile for your linux dump, and test that it works by listing the processes in the memory image. Then, using volatily as a library (example), write a tool that accepts as parameters two snapshot taken from the same machine at different times (e.g., 15 minutes one after the other) and for each processes (uniquely identified by its PID), list the number of pages that are different between the two snapshots. (you can find an example to list the process pages here
For instance, the output should be like:

| PID  | Pages that matches | Pages that are different |
|------|--------------------|--------------------------|
| 1234 | 55                 | 32                       |
| 1235 | 122                | 1                        |
| ...  | ...                | ...                      |
