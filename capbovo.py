#!/usr/bin/python2.7 
"This is the bovo screenshot module"
import gtk.gdk as gdk
import sys
import subprocess 
import re
import numpy as np

class FIRLRobot(object):
    """FIRLRobot is a self-learning robot for FIR(Five in Row)"""
    def __init__(self):
        super(FIRLRobot, self).__init__()
        self.xid = self.getBovoId()

    def get_chessboard(self):#, savefile='/home/jyhong/Pictures/capbovo.png', saveformat="png"):
        '''return the 22x22 chessboard, 1 is red part, 2 is green part, negative means game over'''
        bovoXID = self.xid
        win = gdk.window_foreign_new(bovoXID)
        if win==None:
            print 'can not find window:',bovoXID
            return
        sz = win.get_size()
        width = sz[0]-110-9
        height = sz[1]-80-8
        pb = gdk.Pixbuf(gdk.COLORSPACE_RGB, False, 8, width, height)
        pb = pb.get_from_drawable(win, win.get_colormap(),9,48,0,0,width, height)
        # width = int(width/2)
        # height = int(height/2)
        # pb = pb.scale_simple(width, height, gdk.INTERP_TILES)
        pixnum = pb.get_pixels_array()
        sz = pixnum.shape
        print "screenshot shape: ",sz
        if sz[0] > 300 or sz[1]>300:
            print "WARN: the screenshot is too large, may take too much time in anlysis the pictures"
        chessboard = np.zeros((22,22))
        gap = 9.9
        off = 4
        for x in xrange(0,22):
            for y in xrange(0,22):
                if pixnum[int(y*gap)+off, int(x*gap)+off, 0] == 255:
                    chessboard[y, x] = 1
                elif pixnum[int(y*gap)+off, int(x*gap)+off, 1] ==255:
                    chessboard[y, x] = 2
                if pixnum[int(y*gap)+off, int(x*gap)+off, 1] ==215:
                    chessboard[y, x] = -1
                elif pixnum[int(y*gap)+off, int(x*gap)+off, 1] ==215:
                    chessboard[y, x] = -2
                pixnum[int(y*gap)+off, int(x*gap)+off, :] = 255 
        print chessboard
        # # save screenshot to file
        # if (pb != None):
        #     pb.save(savefile, saveformat)
        #     print "save file to", savefile
        # else:
        #     print "Unable to get the screenshot."
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
    rob.get_chessboard()
