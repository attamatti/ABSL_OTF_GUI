=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    GUI for ABSL OTF
University of Leeds use ONLY
=-=-=-=-=-=-=-=-=-=-=-=-=-=-

:: INSTALLATION ::

1) put all of the files somewhere

2) Update the submission_path and filespath variables in lines 11 and 12
	- submission_path should point to your copy of new_OTF.sh
	- filespath should point to the directory where the files are located (make sure there is a '/' on the end)	

:: RUNNING ::

1) make sure you are using python 3 (currently the command is: module load anaconda3/2018.12)

2) make your project directory 

3) run the GUI from inside the project directory

:: TROUBLESHOOTING ::

THE PROGRAM THINKS IT'S RUNNING - BUT IT'S NOT...

1) run the command: rm OTFFT_running


MANUALLY STOPPING THE PROGRAM:

The processes started by this script are nohupped and therefore a bit hard to kill manually.
If you need to kill this after it has started running:

1) run the the command: ps -ef | grep '/bin/sh'

2) get the PID of the running script from the output above

3) run the command: kill -9 <PID>

4) run the command: pkill rsync

5) run the command: rm OTFFT_running


