#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Junyuan Hong
# @Date:   2014-12-09 21:50:28
# @Last Modified by:   Junyuan Hong
# @Last Modified time: 2014-12-10 12:33:01

# Reference to the code in 
# http://blog.chinaunix.net/uid-52437-id-3068595.html

import Xlib.display as ds
import Xlib.X as X
import Xlib.ext.xtest as xtest

class mouse():
    '''mouse estimate'''
    def __init__(self):
        self.display = ds.Display()

    def press(self, buttonKey):
        '''button: 1 left; 2 middle; 3 right; 4 middle up; 5 middle down'''
        xtest.fake_input(self.display, X.ButtonPress, buttonKey)
        self.display.sync()

    def release(self, buttonKey):
        '''button: 1 left; 2 middle; 3 right; 4 middle up; 5 middle down'''
        xtest.fake_input(self.display, X.ButtonRelease, buttonKey)
        self.display.sync()

    def click(self, butonKey):
        '''button: 1 left; 2 middle; 3 right; 4 middle up; 5 middle down'''
        self.mouse_press(buttonKey)
        self.mouse_release(buttonKey)

    def click(self, buttonKey, x, y):
        '''button: 1 left; 2 middle; 3 right; 4 middle up; 5 middle down'''
        xtest.fake_input(self.display, X.MotionNotify, x = x, y = y)
        self.display.flush()
        xtest.fake_input(self.display, X.ButtonPress, buttonKey)
        self.display.sync()
        xtest.fake_input(self.display, X.ButtonRelease, buttonKey)
        self.display.sync()
        # self.display.flush()
        # print "click: ",(x,y)

    def moveto(self, x, y):
        '''move mouse to specific position(x,y)'''
        xtest.fake_input(self.display, X.MotionNotify, x = x, y = y)
        self.display.flush()

    def get_position(self):
        '''return the current position(x,y) of mouse'''
        pos = self.display.screen().root.query_pointer()._data
        return (pos['root_x'], pos['root_y'])

    def screen_size(self):
        '''return the screen size(width, height)'''
        width = self.display.screen().width_in_pixels;
        height = self.display.screen().height_in_pixels;
        return (width, height)

if __name__ == "__main__":
    m = mouse()
    m.click(1, 20, 60)
