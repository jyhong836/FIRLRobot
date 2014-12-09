#!/usr/bin/python2.7
import subprocess 
import re

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

if __name__=="__main__":
    xid = getBovoId()
