#!/usr/bin/python2.7 
"This is the bovo screenshot module"
import gtk.gdk as gdk
import sys
import subprocess 
import re
import numpy as np

def capbovo(bovoXID, savefile='/home/jyhong/Pictures/capbovo.png', saveformat="png"):
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
    print "screenshot shape: ",pixnum.shape
    chessboard = np.zeros((22,22))
    gap = 9.9
    off = 4
    for x in xrange(0,22):
        for y in xrange(0,22):
            # print y, x
            print pixnum[int(y*gap)+off, int(x*gap)+off, :]
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
    # for x in xrange(1,width):
    #     for y in xrange(1,height):
    #         if pixnum[y,x,0]>128: 
    #             pixnum[y,x,0] = 255
    #         else:
    #             pixnum[y,x,0] = 0
    #         if pixnum[y,x,1]>128: 
    #             pixnum[y,x,1] = 255
    #         else:
    #             pixnum[y,x,1] = 0
    #         if pixnum[y,x,2]>128: 
    #             pixnum[y,x,2] = 255
    #         else:
    #             pixnum[y,x,2] = 0
    #         if np.all(pixnum[y,x,:] < 128):
    #             pixnum[y,x,:] = 255
    if (pb != None):
        pb.save(savefile, saveformat)
        print "save file to", savefile
    else:
        print "Unable to get the screenshot."

def getBovoId():
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
    capbovo(getBovoId())
