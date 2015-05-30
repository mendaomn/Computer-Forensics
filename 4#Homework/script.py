#!/usr/bin/python
import sys
import os
import shutil

# check command line arg
if len(sys.argv) != 3:
    print "Usage: python script.py <img1> <img2>"
    exit()

# defines
outputdir1 = "forensics_menduni_outputdir1"
outputdir2 = "forensics_menduni_outputdir2"
logfile = "forensics_menduni_logfile"

# clean directories
def clean_dirs():
    if os.path.exists(outputdir1):
        shutil.rmtree(outputdir1)
    os.makedirs(outputdir1)
    if os.path.exists(outputdir2):
        shutil.rmtree(outputdir2)
    os.makedirs(outputdir2)

# print in space-separated columns
def print_in_columns(data):
    rows = [ line.strip().split('#') for line in data ]
    cols = zip(*rows)
    col_widths = [ max(len(value) for value in col) for col in cols ]
    format = '          '.join(['%%%ds' % width for width in col_widths ])
    for row in rows:
      print format % tuple(row)

# imports
from filecmp import dircmp
import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
import volatility.utils as utils
import volatility.plugins.linux as linux

# load up some pseudo data
registry.PluginImporter()
config = conf.ConfObject()
registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrspace.BaseAddressSpace)

# default config 
base_conf = {'profile': 'LinuxUbuntu1404x64', 
    'use_old_as': None, 
    'kdbg': None, 
    'help': False, 
    'kpcr': None, 
    'tz': None, 
    'pid': None, 
    'output_file': None, 
    'physical_offset': None, 
    'conf_file': None, 
    'dtb': None, 
    'output': None, 
    'info': None, 
    'location': "file:///"+sys.argv[1], 
    'plugins': None, 
    'debug': None, 
    'cache_dtb': True, 
    'filename': None, 
    'cache_directory': None, 
    'verbose': None, 'write':False}

# set the default config
for k,v in base_conf.items():
    config.update(k, v)

# output container initialization
rows = []
header = "PID#Pages that matches#Pages that are different"
rows.append(header)

#config.PID = "1036, 1132, 548, 974, 978, 984, 985, 988"

pslist = linux.pslist.linux_pslist(config)
proc_maps = linux.proc_maps.linux_proc_maps(config)
pagedump = linux.dump_map.linux_dump_map(config)

fdo = open(logfile, "w+")
#count = 0

# for every pid
pid = "nopid"
for task in pslist.calculate():
    if task.mm:
       #if count == 3:
       #     break
        print "Analysing PID: "+str(task.pid)
        clean_dirs()
        config.PID = str(task.pid)

        # dump img1's pages
        config.LOCATION = "file:///"+sys.argv[1]
        config.DUMP_DIR = outputdir1
        pagedump.render_text(fdo, proc_maps.calculate())

        # dump img2's pages
        config.LOCATION = "file:///"+sys.argv[2]
        config.DUMP_DIR = outputdir2
        pagedump.render_text(fdo, proc_maps.calculate())

        # compare dumps
        dcmp = dircmp(outputdir1, outputdir2) 
        row = config.PID + "#" + str(len(dcmp.same_files)) + "#" + str(len(dcmp.diff_files))
        rows.append(row)

        #count += 1

# print result
print_in_columns(rows)

fdo.close()
