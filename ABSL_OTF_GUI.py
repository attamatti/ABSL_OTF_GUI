#!/usr/bin/env python

import subprocess
import os
import sys

try:
    from tkinter import *
    from tkinter import filedialog
    from tkinter import messagebox
except:
    sys.exit('\nERROR: Python 3 is required! - use module load anaconda3/2018.12')




## Hello
vers = '0.4'
submission_path = '/fbs/emsoftware2/LINUX/fbsmi/scripts/workshop/GUI_otf/new_OTF.sh'
filespath = '/fbs/emsoftware2/LINUX/fbsmi/scripts/workshop/GUI_otf/'

## general config
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

    dataval = data.get()  
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

    PNval = PN.get()  
    if len(PNval) > 1:
        PNcheck= True  
    else:
        messagebox.showerror('ERROR','No project dir name specified!')
        PNcheck=False

    try:
        timeval=(int(time.get())*60*60)
        timecheck = True
        print(timeval)
    except:
       messagebox.showerror('ERROR','Run length value is invalid!')
       timecheck=False
    
    if timecheck == True and PNcheck == True and datacheck == True:
        subprocess.call('nohup {0} {1} {2} {3} {4} {5} &'.format(submission_path,dataval,destination,PNval,offload,timeval),shell=True)
        print('RUNNING: nohup {0} {1} {2} {3} {4} {5} &'.format(submission_path,dataval,destination,PNval,offload,timeval))
        runningfile = open('OTFFT_running','w')
        runningfile.write('{0};{1};{2}'.format(dataval,PNval,timeval))
        runningfile.close()
        runmsg.config(text='File transfer is running you can now close the GUI',foreground='green')
        doit.config(text='KILL',foreground='red',command=kill)

def kill():
    running = str(subprocess.check_output(["ps","-u"])).split("\\n")
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
        messagebox.showerror("ERROR","Some sort of error has occuerd\nplease kill the job manually and restart the GUI")

doit = Button(root, text="Run", command=do_it,width=20)
doit.grid(column=1, row=5)
    
## make it inactive if already running
if os.path.isfile('OTFFT_running') == True:
    doit.config(text='KILL',foreground='red',command=kill)
    runmsg.config(text='File transfer is already running',foreground='green')
    vals = open('OTFFT_running','r').readlines()[0].split(';')
    data.insert(0,vals[0])
    data.config(state='disabled')
    PN.insert(0,vals[1])
    PN.config(state='disabled')
    time.insert(0,str(int(vals[2])/360))
    time.config(state='disabled')
    btn.config(state='disabled')


## the quit function
def close_window (): 
    root.destroy()
quit = Button(root, text="Quit", command=close_window,width=20)
quit.grid(column=2, row=5)

root.mainloop()
