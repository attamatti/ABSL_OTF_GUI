#!/usr/bin/env python

### completely kill the processes initiated by the OTF GUI

import subprocess
import os
import glob

#### find copies of the script running
running = str(subprocess.check_output(["ps","-uef"])).split("\\n")
PIDs = []
for i in running:
	line = i.split()
	if 'new_OTF' in i:
		PIDs.append(line[1])

#### inform user
print('KILL: Found {0} instances of the script running'.format(len(PIDs)))


#### kill any running processes
if len(PIDs) > 0:
	print('KILL: Killing PIDs: {0}'.format(PIDs))
	for i in PIDs:
		subprocess.call('kill -9 {0}'.format(i),shell=True)
		print('KILL: Successfully killed {0}'.format(i))

#### kill any rsync running 
subprocess.call('pkill rsync',shell=True)
print('KILL: stopped all file syncing')

#### remove OTFFT_running file if it exists
if os.path.isfile('OTFFT_running') == True:
	subprocess.call('rm OTFFT_running',shell=True)
	print('KILL: Removed OTF')

#### remove any relion files
relionfiles = glob.glob('.gui*')
for i in relionfiles:
	subprocess.call('rm {0}'.format(i),shell=True)
	print('KILL: Removed {0}'.format(i))

#### remove any symlinks - but ask user first
links = glob.glob('Raw_data/*')
print('KILL: There are {0} file links in Raw_data'.format(len(links)))
if len(links) > 0:
	remove = input('KILL: Remove them (y/n): ')

	if remove in ['y','Y','Yes','yes','YES']:
		for i in links:
			subprocess.call('unlink {0}'.format(os.path.abspath(i)),shell=True)
		print('KILL: Removed {0} symlinks'.format(len(links)))
	else:
		print('KILL: Leaving symlinks in place')

#### my work here is done
print('KILL: Finished')
	
