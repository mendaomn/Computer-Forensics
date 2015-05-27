#!/usr/bin/python
import sys
import os

# defines


# check command line arg
if len(sys.argv) != 1:
	print "Usage: python script.py <image1> <image2>"

import volatility.conf as conf
import volatility.registry as registry
registry.PluginImporter()
config = conf.ConfObject()
import volatility.commands as commands
import volatility.addrspace as addrspace
registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrspace.BaseAddressSpace)
config.parse_options()
config.PROFILE="LinuxUbuntu1404x64"
config.LOCATION = "/home/marv/Scrivania/dump1138"
import volatility.plugins.linux as linux
p = linux.pslist(config)
for process in p.calculate():
	print process



Listing processes in memory image:
python vol.py linux_pslist -f ../dump1138 --profile=LinuxUbuntu1404x64

Listing pages addresses of process 1798:
python vol.py -f ../dump1138 --profile=LinuxUbuntu1404x64 -p 1798 linux_memmap | less

Listing details of process memory, including heaps, stacks, and shared libraries
python vol.py -f ../dump1138 --profile=LinuxUbuntu1404x64 -p 1798 linux_proc_maps | less

Reading from memory
python vol.py -f ../dump1138 --profile=LinuxUbuntu1404x64 -p 1798 linux_dump_map -s 0x0000000000400000 --dump-dir outputdir