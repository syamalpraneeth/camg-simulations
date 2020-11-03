#!/usr/bin/env python2

import os , sys
import matplotlib.pyplot as plt
from plotting import plot_one
from plotting import plot_two
from plotting import plot_three

# simple test of log tool


en=sys.argv[3]
print(en)
logfil="../log.cibd_3nm_"+str(en)+"eV"
#print(logfil)
lg = log(logfil)

 #print "# of vectors =",lg.nvec
#print "length of vectors =",lg.nlen
#print "names of vectors =",lg.names
#time,temp,press = lg.get("Step","Temp","Press")
#lg.write("tmp.log") #all the thermostuff

lg.write("tmp.log.asp_"+str(en)+"eV","Step","v_asp")

#print "all done ... type CTRL-D to exit Pizza.py"
#sys.exit() ===> raises exception. So I used below line from link: https://stackoverflow.com/questions/173278/is-there-a-way-to-prevent-a-systemexit-exception-raised-from-sys-exit-from-bei
os._exit(1)


