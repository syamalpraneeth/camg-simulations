#!/usr/bin/env python2.7
from __future__ import division

import sys,os
import numpy as np

##################################################################
##MAP_EVAL.PY							##                               
##								##
##Dependencies	:						##
##Influences	:						##
##################################################################
## ver.	: 2019--, Syamal Praneeth Chilakalapudi, KIT, INT	##                            
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################

xlo=float(sys.argv[1])
xhi=float(sys.argv[2])
ylo=float(sys.argv[3])
yhi=float(sys.argv[4])
dt=int(sys.argv[5])
z=int(sys.argv[6])
st=sys.argv[7]

def myrange(start, end, step):
    while start <= end:
        yield start
        start += step

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def ratio_eval(x,y,z,dt,mlist = []):
	xp=x+dt
	yp=y+dt
	dt2=dt/2
	zl=z-dt2	#floor the z, please!
	zh=z+dt2
	cu=0
	zr=0
	for a in myrange(x,xp,1):
		for b in myrange(y,yp,1):
			for c in myrange(zl,zh,1):
#				filsiz=len(mlist)
				for it in mlist:
					t=it[0]
					h=it[1]
					k=it[2]
					l=it[3]
					if (h>=x and h<=xp and k>=y and k<=yp and l>=zl and l<=zh):
					#if coords fall within this box
						if ((t == 1) or (t ==3)): cu=cu+1
						if ((t == 2) or (t ==4)): zr=zr+1
#	print(cu,zr)
	if ((cu == 0) and (zr == 0)):
		r= -1
	else:
		r = cu/(cu+zr)
		r = truncate(r,3)
	print(r)
	return r

t       = open(st+'/tmp.coords','r')
#molfil.txt was written as: write_dump  all custom molfil.txt id type x y z f_ff3 in lammps run files
lines   = t.readlines()
t.close()

#Remove a bunch of lines and, read coordinates & type
#del lines[0:9]
a = np.array(lines)
mat = np.empty([len(lines),len(a[1].split())])

for i in range(0,len(lines)):
        mat[i] = a[i].split()
#print(mat)

#At a given z, we take a rectangular sheet and divide into cubes of sheet thickness
#At the given value of z

#then, within the given cube, we evaluate the ratio: #cu/(#cu+#zr). ratio value b/w 0 and 1
#
#if #cu and #zr both are 0, then there is a void        : assign ratio -1
#if #cu == 0, then there is no Copper                   : assign ratio 0
#if #zr == 0, then its a pure copper region             : assign ratio 1
#print(len(lines))
ratio=[] #np.empty([len(lines),4])
i=0
#print(mat)
val=np.empty([1,4])
print(val)
for x in myrange(np.amin(mat[:,1]),np.amax(mat[:,1]),dt):
	for y in myrange(np.amin(mat[:,2]),np.amax(mat[:,2]),dt):
		for c in range(1,dt):
			val[0,0]=x
			val[0,1]=y
			val[0,2]=z
			val[0,3]=ratio_eval(x,y,z,dt,mat)
			ratio.append(val)
#			print(ratio)
#			print(val)
#		print(i,ratio[i,:])
		with open("test.txt","a") as f:
			line = str(x)+","+str(y)+","+str(val[0,3])+'\n'	#write x,y,f values to file
			f.write(line)	
a=np.array(ratio)
print(a)
#assign volume of the cube a colour based on ratio
#scatter plot at given heights


