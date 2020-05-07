#!/usr/bin/env python2.7
from __future__ import division

import sys,os
import bisect
import numpy as np
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import colors

##################################################################
##MAP_EVAL.PY							##                               
##								##
##Dependencies	:						##
##Influences	:						##
##################################################################
## ver.	: 2019--, Syamal Praneeth Chilakalapudi, KIT, INT	##                            
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################

#take inputs from command line
xlo=float(sys.argv[1])
xhi=float(sys.argv[2])
ylo=float(sys.argv[3])
yhi=float(sys.argv[4])
dt=int(sys.argv[5])
z=int(sys.argv[6])
st=sys.argv[7]

#defining custom functions
def myrange(start, end, step):	#custom range function for arbitary step values
    while start <= end:
        yield start
        start += step

def truncate(n, decimals=0):	#truncate decimals
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def ratio_eval(x,y,z,dt,mlist = []): #evaluate ratio of cu to TOTAL atoms
	xp=x+dt
	yp=y+dt
	dt2=dt/2
	zl=z-dt2
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
#	print(r)
	return r

#snippet modified from: https://www.geeksforgeeks.org/python-program-for-binary-insertion-sort/
def find_ge(a, x): #Find leftmost item greater than or equal to x
	i = bisect.bisect_left(a, x)
 #   if i != len(a):
	return i
 #   raise ValueError

#------------------------------------------------------------------------------------End of functions

t       = open(st+'/tmp.coords','r')
lines   = t.readlines()
t.close()

a = np.array(lines)
mat = np.empty([len(lines),len(a[1].split())])
for i in range(0,len(lines)):
        mat[i] = a[i].split()
#print(mat) #.shape)

""" print commands block
print(xlo)
print(xhi)
print(ylo)
print(yhi)
"""

prod = int(((xhi-xlo)//(dt))*((yhi-ylo)//(dt)))
#print(prod)
#print(np.amin(mat[:,1]))
#print(np.amax(mat[:,1]))
grid = np.zeros((prod,4)) #making a coordinate grid
rat = np.full((prod,1),-2) #making a column for ratios
grid=np.append(grid,rat,axis=1)
#print(np.shape(grid))
#print(np.shape(rat))
#print(grid)

cnt=int(0)
#At a given z, we take a rectangular sheet and divide into cubes of sheet thickness
for x in myrange(xlo,xhi-dt,dt):
	for y in myrange(ylo,yhi-dt,dt):
#		print(cnt,x,y)
#		print(cnt)
#		grid[cnt,0] = int(cnt)
		grid[cnt,0] = float(x)
		grid[cnt,1]= float(y)
		cnt+=1
#print(np.shape(grid))
#print(grid)

"""
#then, within the given cube, we evaluate the ratio: #cu/(#cu+#zr). ratio value b/w 0 and 1
#
#if #cu and #zr both are 0, then there is a void        : assign ratio -1
#if #cu == 0, then there is no Copper                   : assign ratio 0
#if #zr == 0, then its a pure copper region             : assign ratio 1
#print(len(lines))
#ratio=[] #np.empty([len(lines),4])

i=0
#print(mat)
val=np.empty([1,4])
#print(val)

for x in myrange(np.amin(mat[:,1]),np.amax(mat[:,1]),dt):
	for y in myrange(np.amin(mat[:,2]),np.amax(mat[:,2]),dt):
	#	for c in range(1,dt):
		val[0,0]=x+(dt/2)
		val[0,1]=y+(dt/2)
		val[0,2]=z
#		val[0,3]=ratio_eval(x,y,z,dt,mat)
		ratio.append(val)
#		print(ratio)
#		print(val)
#		print(i,ratio[i,:])
		with open("test.txt","a") as f:
			line = str(x)+","+str(y)+","+str(val[0,3])+'\n'	#write x,y,f values to file
			f.write(line)
		i=i+1
	print(i)
a=np.array(ratio)
#print(a)
"""

xsp=np.arange(xlo,xhi,dt)
ysp=np.arange(ylo,yhi,dt)
cu = np.ones((prod,1))
zr = np.zeros((prod,1))

#iterate over the matrix of coords and atom types, allocate which grid they belong to and count total atoms in the grid.
itera=0
for c in mat:
	a=find_ge(xsp,c[1]) #abscissa look up
	b=find_ge(ysp,c[2]) #ordinate look up
#	index=int(a+((b)*((xhi-xlo)//(dt))))
	index=int((b-1)+((a-1)*((xhi-xlo)//(dt))))
#	print(a,b,index)
#	print(c[0])
	if (c[0]==1 or c[0]==3): grid[index,2]+=1
	elif (c[0]==2 or c[0]==4): grid[index,3]+=1
	itera+=1

#evalutate ratio allocate ratio value in grid
for i in range(0,len(grid)):
	if ((grid[i,2]!=0) or (grid[i,3])!=0):
#		fs=float(grid[i,2]/(grid[i,2]+grid[i,3]))
#		if fs>=0.5:grid[i,4]=float(grid[i,2]/(grid[i,2]+grid[i,3]))
#		grid[i,4]=float(math.exp(grid[i,2]/(grid[i,2]+grid[i,3])))
		diff = float(grid[i,2] - grid[i,3])
		if diff < 0: grid[i,4] = -1
		elif diff == 0: grid[i,4] = 0
		else: grid[i,4] = 1
#		grid[i,4]=float(grid[i,2]/(grid[i,2]+grid[i,3]))
#		grid[i,4]=float(10**(grid[i,2]/(grid[i,2]+grid[i,3])))
#		print(float(d[5]))

"""
matrix=np.matrix(grid)
print(matrix)
with open('outfile.txt','wb') as f:
	for line in matrix:
		np.savetxt(f, line, fmt='%.2f')
"""

l=len(xsp)
#plt.hexbin(grid[:,0],grid[:,1],C=grid[:,4])
#fig, ax = plt.hist2d(grid[:,0],grid[:,1],bins=[l,l],weights=grid[:,4])
fig, ax = plt.subplots()
#assign volume of the cube a colour based on ratio
h = ax.hist2d(grid[:,0],grid[:,1],bins=l,weights=grid[:,4],vmin=-2,vmax=1,cmap='gray')
plt.xlabel('X')
plt.ylabel('Y')
cbar = plt.colorbar(h[3],ax=ax)
cbar.set_label('Compositional variation')
fig.suptitle('elemental composition heatmap @ Z='+str(z), fontsize=16)
#cmap=plt.cm.get_cmap('gray')
#plt.view_colormap('viridis')
ax.set_aspect(aspect=1)
#fig1 = plt.figure(1,figsize(6.4,2))
#plt.show()
plt.savefig(st+'/heatmap2_'+str(z)+'.png',format='png',dpi=600)

os.remove(st+'/tmp.coords')
