#!/usr/bin/env python2.7
import sys.os
##################################################################
##MAP_EVAL.PY							##                               
##								##
##Dependencies	:						##
##Influences	:						##
##################################################################
## ver.	: 2019--, Syamal Praneeth Chilakalapudi, KIT, INT	##                            
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################

xhi=sys.argv[0]
xlo=sys.argv[1]
yhi=sys.argv[2]
ylo=sys.argv[3]
dt=sys.argv[4]
#At a given z, we take a rectangular sheet and divide into cubes of sheet thickness
z=0 #At the given value of z

#then, within the given cube, we evaluate the ratio: #cu/(#cu+#zr). ratio value b/w 0 and 1
#
#if #cu and #zr both are 0, then there is a void        : assign ratio -1
#if #cu == 0, then there is no Copper                   : assign ratio 0
#if #zr == 0, then its a pure copper region             : assign ratio 1

for i in range(xlo,xhi,dt):
	for j for in range(ylo,yhi,dt):
		 #write x,y,f values to file



#assign volume of the cube a colour based on ratio
#scatter plot at given heights

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

def ratio_eval(x,y,z):
	xp=x+6
	yp=y+6
	zh=z-3	#floor the z, please!
	xl=z+3
	for a in myrange(x,xp,1):
		for b in myrange(y,yp,1):
			for c in myrange(zl,zh,1):
				for <file line iteration>:
					if (h>x & h<xp & k>y & k<yp & l>zl & l<zh):
						if (<> == 1 | ==3): count copper
						if (<> == 2 | ==4): count zirconium
	
	if (zr neq 0):
		r= cu/(cu+zr)
	else
		r=-1
