#!/usr/bin/python2.7 
"This is the bovo screenshot module"
import gtk.gdk as gdk
import sys
import subprocess 
import re
import numpy as np
import time
import random
# import Queue

import mouse

class FIRLRobot(object):
    """FIRLRobot is a self-learning robot for FIR(Five in Row)"""
    def __init__(self):
        super(FIRLRobot, self).__init__()
        self.xid = self.getBovoId()
        self.win_offset_x = 9
        self.win_offset_y = 48
        self.chess_gap = 9.8
        self.chess_off = 5
        self.chessboard_sz = 22

        # init window
        self.win = gdk.window_foreign_new(self.xid)
        if self.win==None:
            print 'can not find window:',self.xid
            return
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

        self.mouse = mouse.mouse()

    def loop(self, max_steps = 10000, wait_time=1):
        '''loop for learning, wait \'wait_time\' length time every step'''
        step = 0
        while True:
            cb = self.get_chessboard()
            (x, y) = self.gowhere()
            self.put_chess(x, y)
            step+=1
            if step > max_steps:
                break
            print "step",step,"...ok"
            time.sleep(1)
        print "loop end"

    def put_chess(self, x, y):
        if x <0 or y <0 or x >=self.chessboard_sz or y >= self.chessboard_sz:
            print "ERROR step, out of range (",x,",",y,")"
            return
        print "click at",(x, y)
        (x, y) = (int(x*self.chess_gap)+self.chess_off + self.win_offset_x, int(y*self.chess_gap)+self.chess_off + self.win_offset_y)
        (self.win_x, self.win_y) = self.win.get_origin()
        self.mouse.click(1, x + self.win_x, y + self.win_y)
        print "click at",(x + self.win_x, y + self.win_y)

    def gowhere(self):
        x = 0
        y = 0

        notcorrect = True
        while notcorrect:
            x = random.randint(0, self.chessboard_sz-1)
            y = random.randint(0, self.chessboard_sz-1)
            if self.chessboards[self.chbptr, y, x]==0:
                notcorrect = False

        return (x, y)

    def get_chessboard(self):#, ):
        '''return the 22x22 chessboard, 1 is red part, 2 is green part, negative means game over'''
        # bovoXID = self.xid
        
        # TEST CODE should be remove in future
        # savefile='/home/jyhong/Pictures/capbovo.png'
        # saveformat="png"
        # end TEST CODE
        
        self.pbuf = self.pbuf.get_from_drawable(self.win, self.win.get_colormap(),self.win_offset_x,self.win_offset_y,0,0,self.width, self.height)
        # width = int(width/2)
        # height = int(height/2)
        # pb = pb.scale_simple(width, height, gdk.INTERP_TILES)
        self.pixnum = self.pbuf.get_pixels_array()
        # sz = pixnum.shape
        # chessboard = np.zeros((22,22))
        chessboard = self.chessboards[self.chbptr, :, :]
        self.chbptr = (self.chbptr + 1)%self.queuelen
        for x in xrange(0,self.chessboard_sz):
            for y in xrange(0,self.chessboard_sz):
                if self.pixnum[int(y*self.chess_gap)+self.chess_off, int(x*self.chess_gap)+self.chess_off, 0] == 255:
                    chessboard[y, x] = 1
                elif self.pixnum[int(y*self.chess_gap)+self.chess_off, int(x*self.chess_gap)+self.chess_off, 1] ==255:
                    chessboard[y, x] = 2
                if self.pixnum[int(y*self.chess_gap)+self.chess_off, int(x*self.chess_gap)+self.chess_off, 1] ==215:
                    chessboard[y, x] = -1
                elif self.pixnum[int(y*self.chess_gap)+self.chess_off, int(x*self.chess_gap)+self.chess_off, 1] ==215:
                    chessboard[y, x] = -2
                # TEST CODE should be remove in future
                # pixnum[int(y*self.chess_gap)+self.chess_off, int(x*self.chess_gap)+self.chess_off, :] = 255 
                # end TEST CODE
        # print chessboard
        # TEST CODE should be remove in future
        # # save screenshot to file
        # if (self.pbuf != None):
        #     self.pbuf.save(savefile, saveformat)
        #     print "save file to", savefile
        # else:
        #     print "Unable to get the screenshot."
        # end TEST CODE
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
    rob.loop(max_steps = 10)
