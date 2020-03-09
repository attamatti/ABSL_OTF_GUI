=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    GUI for ABSL OTF
University of Leeds use ONLY
=-=-=-=-=-=-=-=-=-=-=-=-=-=-

::::: INSTALLATION :::::

1) put all of the files somewhere

2) update the filespath variables in line 3 if necessary
	- filespath should point to the directory where the files are located (make sure there is a '/' on the end)	


::::: UPDATING :::::

1) In the directory where the program is installed run the command:
	
	git pull 

2) check that the filespath variable in line 3 is still correct

::::: RUNNING :::::

1) make sure you are using python 3 (currently the command is: module load anaconda3/2018.12)

2) make your project directory 

3) run the GUI from inside the project directory

4) Setup your Import/Motioncorr/CTF in Relion as normal

5) to kill the process press the kill button, if this causes an error follow the instructions for killing a job manually

::::: OPTIONAL FLAGS :::::

--help		Print a help/troubleshooting message and exit

--kill 		Hard kill every process associated with the GUI
		only use this if the 'kill' button in the GUI
		returns an error

