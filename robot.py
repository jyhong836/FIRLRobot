#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Junyuan Hong
# @Date:   2014-12-10 12:30:10
# @Last Modified by:   Junyuan Hong
# @Last Modified time: 2014-12-13 12:18:14

from numpy import random
import numpy as np
import os
import matplotlib.pyplot as plt # plot, can be remove in future
import sys

import pdb # for debug, insert the `pdb.set_trace()` to program

class ROBOT_MODE():
	'''this class defined the mode of ROBOT'''
	def __init__(self, str):
		self.str = str
	def equal(self, mode):
		return (self.str == mode.str)

ROBOT_LEARNING = ROBOT_MODE("LEARNING")
ROBOT_PLAYING  = ROBOT_MODE("PLAYING")
ROBOT_RANDOM  = ROBOT_MODE("RANDOM")

class robot():
	"""learning robot for FIR"""
	fail_count = 0
	game_count = 0
	steps = 0
	max_steps = 64
	W_file_name = 'W.npy'

	def __init__(self, game_part = 2, mode = ROBOT_RANDOM, sz = 22):
		'''game_part: 1, red part; 2, green part'''
		self.mode = mode
		self.game_part = game_part
		if game_part==1:
			self.oppo_part = 2
		else:
			self.oppo_part = 1
		print "MODE: ", mode.str
		if mode.equal(ROBOT_LEARNING):
			pass# TODO create new learning model
		self.sz = sz
		self.sz2 = sz*sz

		# init matrics
		if os.path.exists(self.W_file_name):
			print "found W.npy"
			self.W = np.load(self.W_file_name)
		# else:
		# 	print "not found W.npy, use random W"
		# 	self.W = random.rand(self.sz2, self.sz2)
		else:
			print "not found W.npy, use zero W"
			# self.W = np.zeros((self.sz2, self.sz2))
			self.W = 0.1*np.eye(self.sz2)

		self.Bs = np.zeros((2, self.max_steps, self.sz2, 1))
		self.F  = np.zeros((self.sz2, 1)) # Final

		self.active_val = 10

	def __del__(self):
		'''save data to files'''
		np.save(self.W_file_name, self.W)
		print "\'Good Bye!\', Robot said."

	def next_step(self, chessboard):
		'''return the estimate step(x,y), return None if game over'''
		# Tranversal to check if the game is over
		for x in xrange(0, self.sz):
		    for y in xrange(0, self.sz):
				if chessboard[y, x] < 0:
					B = chessboard.reshape(self.sz2, 1)
					print "final chessboad:", self.steps
					self.Bs[self.game_part - 1, self.steps, :,:] = B.copy() # save the steps B
					self.Bs[self.oppo_part - 1, self.steps, :,:] = self.Bs[self.game_part - 1, self.steps, :, :] # save the steps B
					if chessboard[y, x] == -1:
					    print "red part win"
					    if self.game_part == 1:
					    	self.game_over(True)
					    else:
					    	self.game_over(False)
					else: 
					    print "green part win"
					    if self.game_part == 2:
					    	self.game_over(True)
					    else:
					    	self.game_over(False)
					return None
		# game not over, take next step
		if self.mode.equal(ROBOT_PLAYING) or self.mode.equal(ROBOT_LEARNING):
			# ROBOT_PLAYING or ROBOT_LEARNING
			B = chessboard.reshape(self.sz2, 1)
			P = np.dot(self.W, B)
			P = (B==0)*P
			PB = P.reshape(self.sz, self.sz)
			(y, x) = np.nonzero(PB==PB.max())
			# print (y,x)
			if len(x)>1:
				(x, y) = (x[random.randint(0,len(x))], y[random.randint(0,len(y))])
			else:
				(x, y) = (x[0], y[0])
			# print "ROBOT:",(x,y)

			# save steps B of robot
			print "steps:", self.steps
			self.Bs[self.game_part - 1, self.steps, :,:] = B.copy()
			# save steps B of game ai
			chessboard[y, x] = self.game_part
			self.Bs[self.oppo_part - 1, self.steps, :,:] = B.copy()
		elif self.mode.equal(ROBOT_RANDOM):
			# ROBOT_RANDOM
			(x, y) = self.random_step(chessboard)

		self.steps += 1
		return (x, y)

	def random_step(self, chessboard):
		'''place chess in a reandom valid place, which will return a tuple(x, y)'''
		x = 0
		y = 0
		invalid = True
		while invalid:
			# FIXME: for some situation, this will be endless
		    x = random.randint(0, self.sz)
		    y = random.randint(0, self.sz)
		    if chessboard[y, x]==0:
		        invalid = False
		return (x, y)

	def reset_params(self):
		'''reset the params to origin status'''
		self.steps = 0

	def game_over(self, win):
		'''
			call this method when game over. Then robot will use the
			data stored to train itself.
		'''
		self.game_count += 1
		if win:
			print "\"Yes, I'm winner!\"Robot happily said.",
		else:
			print "\"No, I lost!\"Robot sadly said.",
			self.fail_count += 1
		if self.game_part == 1:
			print "(red)"
		else:
			print "(green)"
		print "FAILED in ", self.steps," steps [",self.fail_count,"/",self.game_count,"]"

		if self.mode.equal(ROBOT_LEARNING):
			self.train_x(win) # TODO proccess the learning data

		self.reset_params()

	def find_step(self, B_cur, B_pre):
		'''
			find the different between B_cur and B_pre to determine
			which step has been taken at this step.
			return an 484x1 vector for 1 is the chess step, 0 is nothing.
		'''
		D = np.zeros((self.sz2, 1))
		(y, x) = np.nonzero(B_cur - B_pre)
		D[y[0], x[0]] = 1
		return D

	def train_x(self, win, train_round = 100):
		'''
			execute the training.
		'''
		pass
		self.__learn_self(win, train_round)
		# self.learn_oppo(win, train_round)
		self.__learn_oppo_md1_m2(win, train_round)

	def __learn_self(self, win, train_round):
		''' 
			learn from self's steps. This may be difficult for the robot to
			become a good player, since it lost most game at begining.
		'''
		print "** learn from self **"
		self.F = self.__get_estimate_P(win, np.abs(self.Bs[self.game_part - 1, self.steps, :, :]), self.Bs[self.game_part - 1, self.steps - 1, :, :])
		train_part = self.game_part
		self.__train(self.F, self.Bs[self.game_part - 1, :,:,:], self.steps - 1, train_part, train_k = 0.05, train_round = train_round)

	def __learn_oppo(self, win, train_round):
		''' 
			learn from opponent's steps. This may be easier for the robot to
			become a good player, since it's opponent win most game at begining.
			Model 1 Method 1 is used.
		'''
 		print "** learn from opponent **"
 		win = not win
		self.F = self.__get_estimate_P(win, np.abs(self.Bs[self.oppo_part - 1, self.steps, :, :]), self.Bs[self.oppo_part - 1, self.steps - 1, :, :])

		train_part = self.oppo_part
		self.__train(self.F, self.Bs[self.oppo_part - 1, :,:,:], self.steps - 1, train_part, train_k = 0.05, train_round = train_round)

	def __learn_oppo_md1_m2(self, win, train_round):
		''' 
			learn from opponent's steps. This may be easier for the robot to
			become a good player, since it's opponent win most game at begining.
			This method is deffferent from learn_oppo(), since it used the Model 1
			Method 2.
		'''
 		print "** learn from opponent **"
 		win = not win
		self.F = self.__get_estimate_P(win, np.abs(self.Bs[self.oppo_part - 1, self.steps, :, :]), self.Bs[self.oppo_part - 1, self.steps - 1, :, :])

		train_part = self.oppo_part
		self.__train_md1_m2(win, self.F, self.Bs[self.oppo_part - 1, :,:,:], self.steps - 1, train_part, train_k = 0.05, train_round = train_round)

	def __get_estimate_P(self, win, B_cur, B_pre):
		'''return the estimate of P'''
		P = self.find_step(B_cur, B_pre)
		if win:
			P = 0.008*50/self.steps*self.active_val*P
		else:
			P = 0.0008*50/self.steps*self.active_val*(B_pre==0)*(1 - P)
		return P

	def __train_md1_m2(self, win, F, Bs, steps, train_part, train_k = 1, train_round = 10):
		'''Model 1 Method 2, derivative from the train()'''
		# use first step to do some init
		# W = self.W
		print __name__, "train round:", 0,
		if self.game_part != train_part:
			for x in xrange(0, self.sz2):
				if Bs[steps, x, 0] !=0:
					Bs[steps, x, 0] = 3 - Bs[steps, x, 0]
		diff = F - np.dot(self.W, Bs[steps, :, :])
		diff_abs_max = np.max(np.abs(diff))
		if diff_abs_max==0:
			print "error: diff_abs_max is zero, exit..." # FIXME: the diff_abs_max may be zero
			sys.exit()
		# print "  max Final diff:", np.max(diff)
		# print "  min Final diff:", np.min(diff)
		self.W = self.W + train_k*Bs[steps, :, :].T*diff / diff_abs_max
		for t in xrange(steps-1, 0-1, -1):
			if self.game_part != train_part:
				for x in xrange(0, self.sz2):
					if Bs[steps, x, 0] !=0:
						Bs[steps, x, 0] = 3 - Bs[steps, x, 0]
			eP = self.__get_estimate_P(win, Bs[t+1, :, :], Bs[t, :, :])
			diff = (eP - np.dot(self.W, Bs[t, :, :]))
			diff_abs_max = np.max(np.abs(diff))
			if diff_abs_max==0:
				print "error: diff_abs_max is zero, exit..."
				sys.exit()
			self.W = self.W + train_k*Bs[t, :, :].T*diff / diff_abs_max / (t+1)

		# ------- start train round -------
		for r in xrange(1, train_round):
			print "\rtrain round:", r,"       ",
			diff = F - np.dot(self.W, Bs[steps, :, :])
			diff_max = np.max(diff)
			diff_min = np.min(diff)
			diff_abs_max = np.max(np.abs(diff))
			if diff_abs_max==0:
				print "error: diff_abs_max is zero, exit..."
				sys.exit()
			# print "  max Final diff:", diff_max
			# print "  min Final diff:", diff_min
			if diff_max < 0.01 and diff_min > -0.01: 
				break
			self.W = self.W + train_k*Bs[steps, :, :].T*diff / diff_abs_max
			for t in xrange(steps-1, 0-1, -1):
				eP = self.__get_estimate_P(win, Bs[t+1, :, :], Bs[t, :, :])
				diff = (eP - np.dot(self.W, Bs[t, :, :]))
				diff_abs_max = np.max(np.abs(diff))
				if diff_abs_max==0:
					print "error: diff_abs_max is zero, exit..."
					sys.exit()
				self.W = self.W + train_k*Bs[t, :, :].T*diff / diff_abs_max / (t+1)

		print "save W to","data/W/%04d"%self.game_count
		np.save('data/W/%04d'%self.game_count, self.W)

	def __train(self, F, Bs, steps, train_part, train_k = 1, train_round = 10):
		'''Model 1 Method 1'''
		# use first step to do some init
		# W = self.W
		print __name__, "train round:", 0,
		if self.game_part != train_part:
			for x in xrange(0, self.sz2):
				# if Bs[steps, x, 1] == 1:
				# 	Bs[steps, x, 1] = 2
				# else:
				# 	Bs[steps, x, 1] = 1
				if Bs[steps, x, 0] !=0:
					Bs[steps, x, 0] = 3 - Bs[steps, x, 0]
		diff = F - np.dot(self.W, Bs[steps, :, :])
		diff_abs_max = np.max(np.abs(diff))
		if diff_abs_max==0:
			print "error: diff_abs_max is zero, exit..."
			sys.exit()
		# print "  max Final diff:", np.max(diff)
		# print "  min Final diff:", np.min(diff)
		self.W = self.W + train_k*Bs[steps, :, :].T*diff / np.max(np.abs(diff))
		for t in xrange(steps-1, 0-1, -1):
			if self.game_part != train_part:
				for x in xrange(0, self.sz2):
					if Bs[steps, x, 0] !=0:
						Bs[steps, x, 0] = 3 - Bs[steps, x, 0]
			diff = (np.dot(self.W, Bs[t+1, :, :]) - np.dot(self.W, Bs[t, :, :]))
			diff_abs_max = np.max(np.abs(diff))
			if diff_abs_max==0:
				print "error: diff_abs_max is zero, exit..."
				sys.exit()
			self.W = self.W + train_k*Bs[t, :, :].T*diff / np.max(np.abs(diff)) / (t+1)

		# plt.imshow(self.W, origin='lower', interpolation='nearest', cmap = plt.get_cmap('copper'))
		# plt.show()

		# ------- start train round -------
		for r in xrange(1, train_round):
			print "\rtrain round:", r,"       ",
			diff = F - np.dot(self.W, Bs[steps, :, :])
			diff_max = np.max(diff)
			diff_min = np.min(diff)
			diff_abs_max = np.max(np.abs(diff))

			if diff_abs_max==0:
				print "error: diff_abs_max is zero, exit..."
				sys.exit()
			# print "  max Final diff:", diff_max
			# print "  min Final diff:", diff_min

			if diff_max < 0.01 and diff_min > -0.01: 
				break
			self.W = self.W + train_k*Bs[steps, :, :].T*diff / diff_abs_max
			for t in xrange(steps-1, 0-1, -1):
				diff = (np.dot(self.W, Bs[t+1, :, :]) - np.dot(self.W, Bs[t, :, :]))
				diff_abs_max = np.max(np.abs(diff))
				if diff_abs_max==0:
					print "error: diff_abs_max is zero, exit..."
					sys.exit()
				self.W = self.W + train_k*Bs[t, :, :].T*diff / diff_abs_max / (t+1)
		# plt.imshow(W, origin='lower', interpolation='nearest', cmap = plt.get_cmap('copper'))
		# plt.show()
		print "save W to","data/W/%04d"%self.game_count
		np.save('data/W/%04d'%self.game_count, self.W)

if __name__ == "__main__":
	pass