#!/usr/bin/env python2.7
from __future__ import division

import sys,os
import bisect
import numpy as np
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import colors
np.set_printoptions(threshold=sys.maxsize)

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
filno=str(sys.argv[7])
st=sys.argv[8]

#defining custom functions
def myrange(start, end, step):	#custom range function for arbitary step values
    while start <= end:
        yield start
        start += step

def truncate(n, decimals=0):	#truncate decimals
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

#snippet modified from: https://www.geeksforgeeks.org/python-program-for-binary-insertion-sort/
def find_ge(a, x): #Find leftmost item greater than or equal to x
	i = bisect.bisect_left(a, x)
#	print(i)
	if x==a[i]:
		return i+1
	else: return i
 #   raise ValueError

#------------------------------------------------------------------------------------End of functions

t       = open(st+'/tmp.coords','r')
lines   = t.readlines()
t.close()

a = np.array(lines)
mat = np.empty([len(lines),len(a[1].split())])
for i in range(0,len(lines)):
        mat[i] = a[i].split()
#print(mat.shape)

cmat = np.array(mat)

dt2=dt/2
count=0
ndels=0
zma=z+dt2
zmi=z-dt2
iter=0

#print(zmi,z,zma)

#----------------------------------------------SEPARATE OUT PARTICLES IN Z-RANGE
entry=[]
#print(mat)
for index in cmat:
        if (index[3]<zmi or index[3]>zma):
                entry=np.append(entry,iter)
        iter+=1

#print(np.shape(entry))
#print(np.shape(mat))
mat=np.delete(mat,entry,axis=0)
#print(np.shape(mat))
#print(mat)

#----------------------------------------------SORT PARTICLES INTO A GRID
prod = int((1+(xhi-xlo)//(dt))*(1+(yhi-ylo)//(dt)))
#print(prod)
#print(np.amin(mat[:,1]))
#print(np.amax(mat[:,1]))
grid = np.zeros((prod,4)) #making a coordinate grid
rat = np.full((prod,1),-1) #making a column for ratios
grid=np.append(grid,rat,axis=1)
#print(np.shape(grid))
#print(np.shape(rat))
#print(grid)

xsp=np.arange(xlo+dt2,xhi+dt2,dt)
ysp=np.arange(ylo+dt2,yhi+dt2,dt)
xsp=np.arange(xlo,xhi+dt,dt)
ysp=np.arange(ylo,yhi+dt,dt)
asda=np.meshgrid(xsp,ysp)
#print(asda)
#print(np.shape(asda))
#print(xlo)
#print(xhi)
#print(ylo)
#print(yhi)
#print(xsp)
#print(ysp)
#print(np.shape(ysp))

cnt=int(0)
cnty=int(0)
#At a given z, we take a rectangular sheet and divide into cubes of sheet thickness
for x in xsp:
	for y in ysp:
#		print(cnt,x,y)
#		print(cnt)
#		grid[cnt,0] = int(cnt)
		grid[cnt,0] = float(x)
		grid[cnt,1]= float(y)
		cnt+=1
		cnty+=1
#	print(cnty)
#print(np.shape(grid))
#print(grid)

#iterate over the matrix of coords and atom types, allocate which grid they belong to and count total atoms in the grid.
itera=0
for c in mat:
#	print(c)
	a=find_ge(xsp,c[1]) #abscissa look up
	b=find_ge(ysp,c[2]) #ordinate look up
	index=int(b-1+((a-1)*(1+(xhi-xlo)//(dt))))
#	index=int((b-1)+((a-1)*((xhi-xlo)//(dt))))
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
#		diff = float(grid[i,2] - grid[i,3])
#		if diff < 0: grid[i,4] = -1
#		elif diff == 0: grid[i,4] = 0
#		else: grid[i,4] = 1
		grid[i,4]=float(grid[i,2]/(grid[i,2]+grid[i,3]))
#		grid[i,4]=float(10**(grid[i,2]/(grid[i,2]+grid[i,3])))
#		print(float(d[5]))

l=len(xsp)
l2=len(ysp)
#print(l)

#print(np.sum(grid,axis=0))
#print(grid)
#plt.hexbin(grid[:,0],grid[:,1],C=grid[:,4])
#fig, ax = plt.hist2d(grid[:,0],grid[:,1],bins=[l,l],weights=grid[:,4])
fig, ax = plt.subplots()
#assign volume of the cube a colour based on ratio

#h = ax.hist2d(grid[:,0],grid[:,1],bins=[l,l2],weights=grid[:,4],vmin=-1,vmax=1) #,cmap='gray')plt.axvline(x=0.2)
#plt.axvline(x=23.4)
#plt.axvline(x=-3)
#plt.axvline(x=27)
#plt.axvline(x=10)
#plt.axhline(y=-1.8)
#plt.axhline(y=10)
h = ax.hist2d(grid[:,0],grid[:,1],bins=[l-1,l2-1],weights=grid[:,4],vmin=-1,vmax=1) #,cmap='gray')
plt.xlabel('X')
plt.ylabel('Y')

minor_ticks = xsp
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(minor_ticks, minor=True)
ax.grid(which='minor')
cbar = plt.colorbar(h[3],ax=ax)
cbar.set_label('Compositional variation')
fig.suptitle('elemental composition heatmap @ Z='+str(z)+'dt='+str(dt), fontsize=16)
#cmap=plt.cm.get_cmap('gray')
#plt.view_colormap('viridis')
ax.set_aspect(aspect=1)
	#ax.set_xlim([xlo,xhi])
	#ax.set_ylim([ylo,yhi])
#fig1 = plt.figure(1,figsize(6.4,2))
#plt.show()
#string={:03d}'.format(filno)
#string=format(sysi.argv[7],'002')
string=filno.zfill(3)
#print(string)
plt.savefig(st+'/heatmap_'+string+'_'+str(dt)+'.png',format='png',dpi=600)

#os.remove(st+'/tmp.coords')
