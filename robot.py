#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Junyuan Hong
# @Date:   2014-12-10 12:30:10
# @Last Modified by:   Junyuan Hong
# @Last Modified time: 2014-12-10 13:54:46

import random

class ROBOT_MODE():
	def __init__(self, str):
		self.str = str
	def equal(self, mode):
		return (self.str == mode)

ROBOT_LEARNING = ROBOT_MODE("LEARNING")
ROBOT_PLAYING  = ROBOT_MODE("PLAYING")

class robot():
	"""learning robot for FIR"""
	fail_count = 0
	game_count = 0
	steps = 0

	def __init__(self, game_part = 2, mode = ROBOT_PLAYING):
		self.mode = mode
		self.game_part = game_part
		if mode.equal(ROBOT_LEARNING):
			pass # TODO create new learning model

	def next_step(self, chessboard, sz = 22):
		'''return the estimate step(x,y), return None if game over'''
		# Tranversal to check if the game is over
		for x in xrange(0, sz):
		    for y in xrange(0, sz):
		        if chessboard[y, x] < 0:
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
		# place chess in a reandom validate place
		x = 0
		y = 0
		invalid = True
		while invalid:
		    x = random.randint(0, sz-1)
		    y = random.randint(0, sz-1)
		    if chessboard[y, x]==0:
		        invalid = False

		self.steps += 1
		return (x, y)

	def game_over(self, win):
		'''tell the robot the result, win = true for winner.'''
		self.game_count += 1
		if win:
			print "\"Yes, I'm winner!\"Robot happily said."
		else:
			print "\"No, I lost!\"Robot sadly said."
			self.fail_count += 1
		print "FAILED in ", self.steps," steps [",self.fail_count,"/",self.game_count,"]"
		if self.mode.equal(ROBOT_LEARNING):
			pass # TODO proccess the learning data
		
if __name__ == "__main__":
	pass