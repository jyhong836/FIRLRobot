#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Junyuan Hong
# @Date:   2014-12-09 19:19:28
# @Last Modified by:   Junyuan Hong
# @Last Modified time: 2014-12-12 10:15:04
"This is the bovo screenshot module"
import gtk.gdk as gdk
import sys
import subprocess 
import re
import numpy as np
import time
import robot

import mouse

class FIRLRobot(object):
    """FIRLRobot is a self-learning robot for FIR(Five in Row)"""
    win_offset_x = 9
    win_offset_y = 48
    chess_gap = 9.8
    chess_off = 6
    chessboard_sz = 22
    def __init__(self):
        super(FIRLRobot, self).__init__()
        self.xid = self.getBovoId()

        # init window
        self.win = gdk.window_foreign_new(self.xid)
        if self.win==None:
            print 'can not find window:',self.xid
            return
        self.win.set_keep_above(True) # keep the window always above
        sz = self.win.get_size()
        self.width = sz[0]-110-9
        self.height = sz[1]-80-8
        print "screenshot shape: ",(self.width,self.height)
        if self.width > 300 or self.height>300:
            print "WARN: the screenshot is too large, may take too much time in anlysis the pictures"
        if self.height!=222:
            print "ERROR: not correct window height, please keep minimizing the Bovo's window"
            return
        (self.win_x, self.win_y) = self.win.get_root_origin()
        # print "win at",(self.win_x, self.win_y) # for ubuntu14.10 result is (65, 52)

        # init Pixbuf
        self.pbuf = gdk.Pixbuf(gdk.COLORSPACE_RGB, False, 8, self.width, self.height)
        self.pixnum = self.pbuf.get_pixels_array()

        # self.chessboards = Queue.Queue(2)
        self.queuelen = 2;
        self.chessboards = np.zeros((self.queuelen, 22,22))
        self.chbptr = 0

        # init mouse device
        self.mouse = mouse.mouse()

        # init robot
        self.rob  = robot.robot(mode = robot.ROBOT_PLAYING)

    def loop(self, max_steps = 10000, wait_time=1):
        '''loop for learning, wait \'wait_time\' length time every step'''
        step = 0
        self.new_game()
        time.sleep(1)
        print "start loop..."
        while True:
            cb = self.get_chessboard()
            # pos = self.gowhere()
            pos = self.rob.next_step(cb)
            if pos==None:
                self.new_game()
            else:
                (x, y) = pos
                self.put_chess(x, y)
            step+=1
            print "step",step,"...ok"
            if step >= max_steps:
                break
            time.sleep(1)
        print "loop end"

    def put_chess(self, x, y):
        if x <0 or y <0 or x >=self.chessboard_sz or y >= self.chessboard_sz:
            print "ERROR step, out of range (",x,",",y,")"
            return
        (x, y) = (int(x*self.chess_gap)+self.chess_off + self.win_offset_x, int(y*self.chess_gap)+self.chess_off + self.win_offset_y)
        (self.win_x, self.win_y) = self.win.get_origin()
        (x0, y0) = self.mouse.get_position()
        self.mouse.click(1, x + self.win_x, y + self.win_y)
        # self.mouse.moveto(x + self.win_x, y + self.win_y)
        # self.win.set_events(gdk.ENTER_NOTIFY | gdk.BUTTON_PRESS | gdk.BUTTON_RELEASE)
        self.mouse.moveto(x0, y0)

    def new_game(self):
        print "* start a new game"
        (self.win_x, self.win_y) = self.win.get_origin()
        (x0, y0) = self.mouse.get_position()
        self.mouse.click(1, 16 + self.win_offset_x + self.win_x, -23 + self.win_offset_y + self.win_y)
        self.mouse.moveto(x0, y0)
        print "click: ",(16 + self.win_offset_x, -23 + self.win_offset_y)

    def get_chessboard(self):#, ):
        '''return the 22x22 chessboard, 1 is red part, 2 is green part, negative means game end'''
        # bovoXID = self.xid
        
        # # TEST CODE should be remove in future
        # savefile='/home/jyhong/Pictures/capbovo.png'
        # saveformat="png"
        # # end TEST CODE
        
        self.pbuf = self.pbuf.get_from_drawable(self.win, self.win.get_colormap(),self.win_offset_x,self.win_offset_y,0,0,self.width, self.height)
        # width = int(width/2)
        # height = int(height/2)
        # pb = pb.scale_simple(width, height, gdk.INTERP_TILES)
        self.pixnum = self.pbuf.get_pixels_array()
        # sz = pixnum.shape
        # chessboard = np.zeros((22,22))
        self.chbptr = (self.chbptr + 1)%self.queuelen # move to new ptr firstly
        chessboard = self.chessboards[self.chbptr, :, :]
        for x in xrange(0,self.chessboard_sz):
            for y in xrange(0,self.chessboard_sz):
                iy = int(y*self.chess_gap)+self.chess_off
                ix = int(x*self.chess_gap)+self.chess_off
                if self.pixnum[iy, ix, 0] > 0:
                    chessboard[y, x] = 1
                elif self.pixnum[iy, ix, 1] > 0:
                    chessboard[y, x] = 2
                else:
                    chessboard[y, x] = 0
                if self.pixnum[iy, ix, 2] > 0 :
                    chessboard[y, x] = -chessboard[y, x]
                # # TEST CODE should be remove in future
                # if self.pixnum[iy, ix, 2]>0:print self.pixnum[iy, ix, :]
                # self.pixnum[iy, ix, :] = 255 
                # # end TEST CODE
        # print chessboard
        # # TEST CODE should be remove in future
        # # save screenshot to file
        # if (self.pbuf != None):
        #     self.pbuf.save(savefile, saveformat)
        #     print "save file to", savefile
        # else:
        #     print "Unable to get the screenshot."
        # # end TEST CODE
        return chessboard

    def getBovoId(self):
        '''return the Bovo window XId, if failed return None'''
        p = subprocess.Popen("xwininfo -tree -int -name Bovo | grep Bovo",\
                shell=True,\
                stdout = subprocess.PIPE,\
                stdin = subprocess.PIPE)
        p.wait()
        xid = p.stdout.read()
        matchObj = re.search(r'\d+', xid, re.IGNORECASE)
        if matchObj:
            xid = int(matchObj.group(0))
            print "XID:",xid 
            return xid
        else:
            print "no Bovo running"
            return None

if __name__ == "__main__":
    rob = FIRLRobot()
    # rob.get_chessboard()
    arg = sys.argv
    # The game rounds should be set but not the max steps
    if len(arg)>1:
        rob.loop(max_steps = int(arg[1]))
    else:
        rob.loop(max_steps = 20)
