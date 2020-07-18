#!/usr/bin/env python2.7

import numpy as np
import math
#import matplotlib.pyplot as plt

def my_range(start, end, step):     #This is a custom range function to iterate with fractional steps as well. range() works only with integers.
    while start <= end:
        yield start
        start += step

t	= open('../data/molfil_MC_3nm.txt','r')
#molfil.txt was written as: write_dump	all custom molfil.txt id type mass x y z in lammps run files
lines	= t.readlines()
t.close()

#Remove a bunch of lines, and then read coordinates & type
del lines[0:9]
a = np.array(lines)				#making array of all lines taken from file. Its now an array of strings
mat = np.empty([len(lines),len(a[1].split())])

for i in range(0,len(lines)):
	mat[i] = a[i].split()			#split array of strings column wise to get matrix of id, type, coordinates


#at = np.delete(mat,[0,1,2],axis=1)		#at is a matrix of all coordinates
#print(at)
#R = math.ceil(np.amax(at))+5			#find max of coordinates. This will be approximate Radius

ind = 0
used = []
c1 = []
c2 = []
d = 0
p = 0


#step = R/80.0
#print(step)

#the idea is to take all atom radii, and count them making a spherical shells, and calculate composition in shells
#right now we make the atom radii. LAMMPS by default has origin at (0,0,0) so we just compute sum of squares of coordinates
Rmat = np.zeros([len(mat),1])
for i in range(0,len(mat)):
	Rmat[i] = math.sqrt(mat[i,3]**2 + mat[i,4]**2 + mat[i,5]**2)
mat = np.append(mat, Rmat, axis=1)		#Appending Radii values to the matrix of coordinates
R = math.ceil(np.amax(Rmat))+5			#Finding max radius and adding 5 units to it for iteratign over later
#print(R)

step = 0.5 #R/100.0
pre = (4.0/3.0)* math.pi
radcu = [x**3 for x in my_range(1,R,step)]	#array of cube of incremental radii
vols = [x*pre for x in my_range(1,R,step)]	#array of volume of spheres of incremental radii

st = step 					#shell thickness for composition evaluation
rad = np.zeros([len(radcu),1])
cmp1 = np.zeros([len(radcu),1])
cmp2 = np.zeros([len(radcu),1])
pot_e = np.zeros([len(radcu),1])

#print(len(radcu))
print(mat.shape)
#print(mat[:,6])
print(mat)

tot = 0
ind = 0
for r in my_range(1,R,step):			#iterating over radii steps from 1 to maximum R
	rad[ind] = r
	cnt1 = 0
	cnt2 = 0
	cnt3 = 0
#	c3 = 0
	pe = 0
	n = 0
	for i in range(0,len(mat)):		#For every radius r, compare all atom coordinates and check if they fit into the shell
		if (r-3) <= Rmat[i] <= r:
			#print("hi")
			cnt3 = cnt3+1
			pe = pe + mat[i,6]	#01234567 are id type mass x y z pe radcu
			n = n + 1		#num of atoms counted in this iteration
			if mat[i,1] == 1 or mat[i,1] == 3:	#In the shell type==1/3, count it into cnt1
				cnt1 = cnt1+1
			if mat[i,1] == 2 or mat[i,1] == 4:
				cnt2 = cnt2+1	#In the shell type==2/4, count it into cnt2
			cnt3=cnt1+cnt2
	if r > 0:	
		if cnt3 != 0:
			cmp1[ind] = float(cnt1)/float(cnt3)
			cmp2[ind] = float(cnt2)/float(cnt3)
		else:
			cmp1[ind] = 0
			cmp2[ind] = 0
	else:
			cmp1[ind] = 0
			cmp2[ind] = 0
	##	cmp1.append(float(cnt1)/float(cnt3))
	##	cmp2.append(float(cnt2)/float(cnt3))
	if n>0:
		pot_e[ind] = float(pe/n)
#	print(ind,r,cmp1[ind],cmp2[ind],pot_e[ind],n)
	ind = ind+1

#print(rad)
#print(cmp1)
#print(cmp2)
comp = np.append(rad, cmp1, axis=1)
#print(comp)
comp = np.append(comp, cmp2, axis=1)
pot_e = np.append(rad, pot_e, axis=1)

np.savetxt('tmp.log.comp',comp,fmt='%5.4f %5.4f %5.4f')
np.savetxt('tmp.log.pe',pot_e,fmt='%5.4f %5.4f')
