#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Junyuan Hong
# @Date:   2014-12-10 12:30:10
# @Last Modified by:   Junyuan Hong
# @Last Modified time: 2014-12-12 13:36:47

from numpy import random
import numpy as np
import os

class ROBOT_MODE():
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
		print "MODE: ", mode.str
		if mode.equal(ROBOT_LEARNING):
			pass# TODO create new learning model
		self.sz = sz
		self.sz2 = sz*sz

		# init matrics
		if os.path.exists(self.W_file_name):
			print "found W.npy"
			self.W = np.load(self.W_file_name)
		else:
			print "not found W.npy, use random W"
			self.W = random.rand(self.sz2, self.sz2)

		self.Bs = np.zeros((self.max_steps, self.sz2, 1))
		self.F  = np.zeros((self.sz2, 1)) # Final

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
					self.Bs[self.steps, :,:] = B.copy() # save the steps B
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

			print "steps:", self.steps
			self.Bs[self.steps, :,:] = B.copy() # save the steps B

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
		elif self.mode.equal(ROBOT_RANDOM):
			# ROBOT_RANDOM
			(x, y) = self.random_step(chessboard)

		self.steps += 1
		return (x, y)

	def random_step(self, chessboard):
		'''place chess in a reandom valid place'''
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
		self.steps = 0

	def game_over(self, win):
		'''tell the robot the result, win = true for winner.'''
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
		D = np.zeros((self.sz2, 1))
		(y, x) = np.nonzero(B_cur - B_pre)
		D[y[0], x[0]] = 1
		return D

	def train_x(self, win, train_round = 10):
		# self.F = # game_part
		self.F = self.find_step(np.abs(self.Bs[self.steps, :, :]), self.Bs[self.steps - 1, :, :])
		active_val = 10
		if win:
			self.F = active_val*self.F
		else:
			self.F = 0.1*active_val*(self.Bs[self.steps - 1, :, :]==0)*(1 - self.F) # ??? FIXME: 
		# self.steps -= 1
		# if win:
		# 	train_part = game_part
		# else:
		# 	if game_part = 1:
		# 		train_part = 2
		# 	else:
		# 		train_part = 1
		train_part = self.game_part
		self.train(self.F, self.Bs, self.W, self.steps - 1, train_part, train_k = 0.1, train_round = train_round)

	def train(self, F, Bs, W, steps, train_part, train_k = 1, train_round = 10):
		print "train round:", 0
		if self.game_part != train_part:
			for x in xrange(0, self.sz2):
				if Bs[steps, x, 1] == 1:
					Bs[steps, x, 1] = 2
				else:
					Bs[steps, x, 1] = 1
		diff = F - np.dot(W, Bs[steps, :, :])
		print "  max Final diff:", np.max(diff)
		print "  min Final diff:", np.min(diff)
		W = W + train_k*Bs[steps, :, :].T*diff / np.max(diff)
		for t in xrange(steps-1, 0-1, -1):
			if self.game_part != train_part:
				for x in xrange(0, self.sz2):
					if Bs[t, x, 1] == 1:
						Bs[t, x, 1] = 2
					else:
						Bs[t, x, 1] = 1
			diff = (np.dot(W, Bs[t+1, :, :]) - np.dot(W, Bs[t, :, :]))
			W = W + train_k*Bs[t, :, :].T*diff / np.max(diff)

		for r in xrange(1, train_round):
			print "train round:", r
			diff = F - np.dot(W, Bs[steps, :, :])
			print "  max Final diff:", np.max(diff)
			print "  min Final diff:", np.min(diff)
			W = W + train_k*Bs[steps, :, :].T*diff / np.max(diff)
			for t in xrange(steps-1, 0-1, -1):
				diff = (np.dot(W, Bs[t+1, :, :]) - np.dot(W, Bs[t, :, :]))
				W = W + train_k*Bs[t, :, :].T*diff / np.max(diff)
		
if __name__ == "__main__":
	pass