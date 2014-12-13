FIR robot
=====
This is a auto-learning robot for the bovo game(an open source FIR game). You can get all code in [github](https://github.com/jyhong836/FIRLRobot).

FIR is short for ['Five in a Row'](http://en.wikipedia.org/wiki/Gomoku). This python program is running in Ubuntu14.10. By capture the shotcut of Bovo and estimate the activities of mouse, the program (robot) will be able to behavior as a human playing the FIR. Through the games between the Bovo's AI and the FIR robot, the robot can learn how to play.

### Robot

The Model used by FIR learning robot.

* MODEL 1
	- `P_t = W*B_t`, `P` is 22x1 reshped chessboard probability matrix, `W` is linked wight matrix, `B` 22x1 reshped chessboard matrix. For `t=N`, `P_N = F`, `F` is the result of this game.
* MODEL 2
	- `P_t = W*B_t + v`, `v` is Gaussian white noise
* MODEL 3
	- `X_t = W*B + X_{t-1} + v`, `X` is the state matrix at time `t`.
	- `P_t = U*X_t` 
	- For Model 1, the U works as a max function

### Training Method

By playing FIR game with Bovo AI, the program will store the chessboard record for training W matrix. The Model Mothods below will be applied for this aim.

* Model 1
	+ Method 1 
		- W = W + k*(P_{t+1} - P_t), t = 0...N-1
		- W = W + k*(F - P_{N-1})
	+ Method 2
		- W = W + k*(T_t - P_t), t = 0...N-1, T_t is the step of the game ai at step t
		- W = W + k*(F - P_{N-1})

### INSTALL

Copy the files in `bovo-theme/spacy` to bovo spacy folder to replace the theme.

Install the neccessary python dependencies. For Debian/Ubuntu user, you can 
    
	# apt-get install python-gtk2-dev
	# apt-get install python-xlib

The 'Bovo' program has to be run before the robot running. For example, in 'Bovo' build file, execute `./bovo`

run the robot, `./FIRLRobot.py`

### About Bovo

For Ubuntu user, you can install by searching 'bovo' in 'Ubuntu Software Center'.

You can also compile the code by yourself, visiting [Bovo Icon
Bovo - Development Information](https://www.kde.org/applications/games/bovo/development). Clone it down use the code below.

	# git clone git://anongit.kde.org/bovo