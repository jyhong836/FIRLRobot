#!/usr/bin/python2.7 
"This is the bovo screenshot module"
import gtk.gdk as gdk
import sys

def capbovo(bovoXID, savefile='/home/jyhong/Pictures/capbovo.png', saveformat="png"):
    win = gdk.window_foreign_new(bovoXID)
    if win==None:
        print 'can not find window:',bovoXID
        return
    sz = win.get_size()
    pb = gdk.Pixbuf(gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1])
    pb = pb.get_from_drawable(win, win.get_colormap(),0,0,0,0,sz[0],sz[1])
    print pb.get_pixels()
    if (pb != None):
        pb.save(savefile, saveformat)
        print "save file to ", savefile
    else:
        print "Unable to get the screenshot."

if __name__ == "__main__":
    capbovo(int(sys.argv[1]))
