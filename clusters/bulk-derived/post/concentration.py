import numpy as np
import math
#import matplotlib.pyplot as plt

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

t	= open('molfil.txt','r')
#molfil.txt was written as: write_dump	all custom molfil.txt id type x y z f_ff3 in lammps run files
lines	= t.readlines()
t.close()

#Remove a bunch of lines and, read coordinates & type
del lines[0:9]
a = np.array(lines)
mat = np.empty([len(lines),len(a[1].split())])

for i in range(0,len(lines)):
	mat[i] = a[i].split()

at = np.delete(mat,[0,1],axis=1)		#mat is a matrix of type and coordinates
#r = math.fabs(math.ceil(np.amin(at))-5)			#find max of coordinates. This will be approximate Radius
r = math.ceil(np.amax(at))+2

cnt1 = 0
cnt2 = 0
cnt3 = 0
ind = 0
used = []
c1 = []
c2 = []
d = 0

step = math.floor(r/30)
print(r)
print(step)

for i in my_range(1,r,step):
	a2 = 1
	for j in mat:
		if j[0] not in used:
			if (j[2]**2 + j[3]**2 + j[4]**2 < i**2):
				#print(j)
				used.append(j[0])
				cnt3 = cnt3+1
				if (j[1] == 1):
					cnt1 = cnt1+1
				elif (j[1] == 2):
					cnt2 = cnt2+1
	d = d+1
	ind = ind+1
	print(i,d, cnt1, cnt2)
	c1.append([i,cnt1])
	c2.append([i,cnt2])

pre =  (4.0/3.0) *math.pi
radcu = [x**3 for x in my_range(0,r,step)]
vols = [x*pre for x in my_range(0,r,step)]
print(pre)
