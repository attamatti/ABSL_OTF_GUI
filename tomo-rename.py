#!/usr/bin/env python

# give tomography files from serialEM reasonable names

import os                      # for running UNIX commands
import sys                     # for lots if utilities
import glob                     # for finding files
vers = '0.2.3'                  #version number

try:
    files = glob.glob(sys.argv[1])                                       # get all the mrcs put in list
except:                                                                  # error checking
    sys.exit('USAGE: tomo-rename <files search string>')                 # print help message if in error                                                        

if len(files) == 0:                                                  # if there are no files
    sys.exit("STOP: rename couldn't find any files to operate on")   # quit and say so

print(':: Tomo rename vers {0}::'.format(vers))         # welcome message
print('operating on {0} files'.format(len(files)))      # update user on how many files were found

commands = []                   # empty list to put the commands in

for i in files:                                             # iterate over the list
    chunk1 = i.split('[')                                   # split at [ into chunk1[0] and chunk1[1]
    first_half =  chunk1[0]                                 # 1st half of the file name
    chunk2 = chunk1[1].split(']')                           # split the 2nd half at ]
    tilt = chunk2[0]                                        # 1st half of that is the tilt
    if tilt == '-0.00':                                     # fix negative 0 tilt
        tilt = '0.00'                                       # replace it with just 0.0
    tilt = tilt.replace('.','_')                            # replace the . with p
    rest_of_filename = chunk2[1].strip('-')                 # 2nd half is rest of filename, removing the -
    newfilename = '{0}_{1}_{2}'.format(first_half,tilt,rest_of_filename)    # make new filename
    command = 'mv {0} {1}'.format(i,newfilename)            # make the command
    commands.append(command)                                # add the command to the list of commands
    

for i in commands:                                          # iterate over the list of commands
    print(i)                                                # screen barf = remove this line if you want
    os.system(i)                                            # run each
print('''Rename complete! If you use these programs to preprocess data used in publications plese cite them in your methods.		
Iadanza MG. Leeds tomography tools v1.0. https://github.com/attamatti/leeds_tomo_tools. DOI: 10.5281/zenodo.3247523''')				# citation message
