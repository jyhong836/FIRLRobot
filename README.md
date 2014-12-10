FIR robot
=====
This is a auto-learning robot for the bovo game(an open source FIR game).

FIR is short for 'Five in Row'. This python program is running in Ubuntu14.10. By capture the shotcut of Bovo and estimate the activities of mouse, the program (robot) will be able to behavior as a human playing the FIR. Through the games between the Bovo's AI and the FIR robot, the robot can learn how to play.

INSTALL
======
Copy the files in `bovo-theme/spacy` to bovo spacy folder to replace the theme.

Install the neccessary python dependencies. For Debian/Ubuntu user, you can 
    
	# apt-get install python-gtk2-dev
	# apt-get install python-xlib

The 'Bovo' program has to be run before the robot running. For example, in 'Bovo' build file, execute `./bovo`

run the robot, `./capbovo.py`

### About Bovo

For Ubuntu user, you can install by searching 'bovo' in 'Ubuntu Software Center'.

You can also compile the code by yourself, visiting [Bovo Icon
Bovo - Development Information](https://www.kde.org/applications/games/bovo/development). Clone it down use the code below.

	# git clone git://anongit.kde.org/bovo