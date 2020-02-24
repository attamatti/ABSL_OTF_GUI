#!/usr/bin/env python

########################  UPDATE THIS PATH  ##############################
filespath = '/fbs/emsoftware2/LINUX/fbscem/scripts/ABSL_OTF_GUI/'
##########################################################################

import subprocess
import os
import sys
import glob

try:
    from tkinter import *
    from tkinter import filedialog
    from tkinter import messagebox
except:
    sys.exit('\nERROR: Python 3 is required! - use module load anaconda3/2018.12')

## hello
vers = '0.6'
print('ABSL OTF file transfer utility vers {0}'.format(vers))

if '--help' in sys.argv or '-h' in sys.argv or '-help' in sys.argv:
    subprocess.call('cat {0}README.txt'.format(filespath),shell=True)
    sys.exit()

## check that all of the files needed to run the gui are available
files = glob.glob('{0}/*.*'.format(filespath))
filesfound=True
for i in ['new_OTF.sh','gui_ctffindrun.job','gui_importrun.job','gui_motioncorrrun.job']:
    if '{0}{1}'.format(filespath,i) not in files:
        filesfound=False
        print('ERROR: The file {0} was not found ABSL_OTF_GUI.py was not set up properly... Check the README file!'.format(i))
if filesfound == False:
    sys.exit('ERROR: Search path was: {0}\nERROR: Setup problem... exiting'.format(filespath))

## general config
submission_path = '{0}new_OTF.sh'.format(filespath)
root = Tk()
root.title('ABSL OTF-FT {0}'.format(vers))
root.configure(background='white')

## title and logos
title = Label(root,text='OTF File Transfer Utility'.format(vers))
title.grid(column=1,row=0,columnspan=2)
title.configure(background='white')

logo = PhotoImage(file='{0}absl100px.gif'.format(filespath))
image= Label(image=logo)
image.grid(column=0,row=0)
image.configure(background='white')

leedslogo = PhotoImage(file='{0}uni-of-leeds-logo.gif'.format(filespath))
image= Label(image=leedslogo)
image.grid(column=3,row=0,columnspan=2)
image.configure(background='white')

## data section
datalabel = Label(root,text='Data: ')
datalabel.grid(column=0,row=1)
datalabel.configure(background='white')

data = Entry(root,width=50)
data.grid(column=1,row=1,columnspan=2)
data.configure(background='white')

def getdata():
   folder_selected = filedialog.askdirectory()
   data.insert(0,folder_selected)
btn = Button(root, text="Select dir", command=getdata)
btn.grid(column=3, row=1)

def datahelp():
    messagebox.showinfo("Help","Select your data from the offload server\nit will be in /offload1 (Krios 1) or /offload2 (Krios 2)")
datahelp = Button(root,text = "help", command = datahelp)
datahelp.grid(column=4,row=1)


## project name section
PNlabel = Label(root,text='Project name: ')
PNlabel.grid(column=0,row=2)
PNlabel.configure(background='white')

PN = Entry(root,width=50)
PN.grid(column=1,row=2,columnspan=2)

def PNhelp():
    messagebox.showinfo("Help","Give a name for you project directory\n it will be made on /absl/Equipment")
PNhelp = Button(root,text = "help", command = PNhelp)
PNhelp.grid(column=4,row=2)

## time section
timelabel = Label(root,text='Run length (h): ')
timelabel.grid(column=0,row=3)
timelabel.configure(background='white')

time = Entry(root,width=50)
time.grid(column=1,row=3,columnspan=2)

def timehelp():
    messagebox.showinfo("Help","How long will the data collection be in hours")
timehelp = Button(root,text = "help", command = timehelp)
timehelp.grid(column=4,row=3)


## spot for running message to appear
runmsg = Label(root,text=''.format(vers))
runmsg.grid(column=1,row=4,columnspan=2)
runmsg.configure(background='white')

## the run function
def do_it():
    print('run it!')
    if os.path.isdir('Raw_data') == False:
        subprocess.call('mkdir Raw_data',shell=True)
    ## check the data path
    ## catch dave's error
    dataval = data.get()
    if dataval in ['/offload1','/offload2']:
        messagebox.showerror('ERROR',"It appears that you are trying to sync the ENTIRE {0} server\nMake sure to double click and open the directory you want to sync.".format(dataval))
        datacheck=False
    ## make sure one of the offload servers has been selected
    if len(dataval) > 1:
        datacheck= True  
        offload = dataval.split('/')[1]
        if offload == 'offload1':
            destination = '/absl/Equipment/KRIOS1/'
        elif offload == 'offload2':
            destination = '/absl/Equipment/GATAN/DoseFractions/'
        else:
            messagebox.showerror('ERROR',"That doesn't look like an offload server to me!")
            datacheck=False
    else:
        messagebox.showerror('ERROR','No data directory selected!')
        datacheck=False
    ## check the project name
    PNval = PN.get()  
    if len(PNval) > 1:
        PNcheck= True  
    else:
        messagebox.showerror('ERROR','No project dir name specified!')
        PNcheck=False
    if ' ' in PNval:
        messagebox.showerror('ERROR','NO SPACES IN PROJECT NAMES!\nYou should know better!')
        PNcheck=False
    ## check the time requested
    try:
        timeval=(int(time.get())*60*60)
        timecheck = True
    except:
       messagebox.showerror('ERROR','Run length value is invalid!')
       timecheck=False
    ## if it's all good start the transfer
    if timecheck == True and PNcheck == True and datacheck == True:
        subprocess.call('cp {0}/gui_ctffindrun.job .gui_ctffindrun.job'.format(filespath),shell=True)
        subprocess.call('cp {0}/gui_importrun.job .gui_importrun.job'.format(filespath),shell=True)
        subprocess.call('cp {0}/gui_motioncorrrun.job .gui_motioncorrrun.job'.format(filespath),shell=True)
        subprocess.call('touch .gui_projectdir',shell=True)
        subprocess.call('nohup {0} {1} {2} {3} {4} {5} &'.format(submission_path,dataval,destination,PNval,offload,timeval),shell=True)
        print('RUNNING: nohup {0} {1} {2} {3} {4} {5} &'.format(submission_path,dataval,destination,PNval,offload,timeval))
        runningfile = open('OTFFT_running','w')
        runningfile.write('{0};{1};{2}'.format(dataval,PNval,timeval))
        runningfile.close()
        runmsg.config(text='File transfer is running you can now close the GUI and set up Relion',foreground='green')
        doit.config(text='KILL',foreground='red',command=kill)

## kill function - only active if running
def kill():
    running = str(subprocess.check_output(["ps","-uef"])).split("\\n")
    for i in running:
        line = i.split()
        if 'new_OTF.sh' in i:
            PID = line[1]
    try:
        subprocess.call('kill -9 {0}'.format(PID),shell=True)
        subprocess.call('pkill rsync',shell=True)
        subprocess.call('rm OTFFT_running',shell=True)
        print('OTF file transfer has been stopped')
        runmsg.config(text='File transfer killed; restart the GUI to begin again',foreground='red')

    except:
        messagebox.showerror("ERROR","Some sort of error has occured\nERROR: please kill the job manually and restart the GUI")

doit = Button(root, text="Run", command=do_it,width=20)
doit.grid(column=1, row=5)
    
## if the transfer is already running
if os.path.isfile('OTFFT_running') == True:
    doit.config(text='KILL',foreground='red',command=kill)
    runmsg.config(text='File transfer is already running',foreground='green')
    try:
        vals = open('OTFFT_running','r').readlines()[0].split(';')
        data.insert(0,vals[0])
        data.config(state='disabled')
        PN.insert(0,vals[1])
        PN.config(state='disabled')
        time.insert(0,str(int(vals[2])/360))
        time.config(state='disabled')
        btn.config(state='disabled')
    except:
        sys.exit('\nERROR: There was a problem reading OTFFT_running\nERROR: delete it, manually kill any file transfer (see README), and start over')



## the quit function
def close_window (): 
    root.destroy()
quit = Button(root, text="Quit", command=close_window,width=20)
quit.grid(column=2, row=5)

root.mainloop()
