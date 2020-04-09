import numpy as np
import math
#import matplotlib.pyplot as plt

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

t	= open('molfil.txt','r')
lines	= t.readlines()
t.close()

#Remove a bunch of lines and, read coordinates & type
del lines[0:9]
a = np.array(lines)
mat = np.empty([len(lines),len(a[1].split())])

for i in range(0,len(lines)):
	mat[i] = a[i].split()

at = np.delete(mat,[0,1],axis=1)		#mat is a matrix of type and coordinates
R = math.ceil(np.amax(at))+2			#find max of coordinates. This will be approximate Radius

ind = 0
used = []
c1 = []
c2 = []
d = 0


step = R/80.0
print(step)

Rmat = np.zeros([len(mat),1])
for i in range(0,len(mat)):
	Rmat[i] = math.sqrt(mat[i,2]**2 + mat[i,3]**2 + mat[i,4]**2)
mat = np.append(mat, Rmat, axis=1)		#Appending Radii values to the matrix of coordinates

pre =  (4.0/3.0) *math.pi
radcu = [x**3 for x in my_range(0,R,step)]
vols = [x*pre for x in my_range(0,R,step)]

st = step 						#shell thickness for composition evaluation
cmp1 = np.zeros([len(mat),1])
cmp2 = np.zeros([len(mat),1])

for r in my_range(1,R,step):
	cnt1 = 0
	cnt2 = 0
	cnt3 = 0
	for i in range(0,len(mat)):
		if (r-2) < mat[i,5] < r:
			cnt3 = cnt3+1
			if mat[i,1] == 1:
				cnt1 = cnt1+1
			if mat[i,1] == 2:
				cnt2 = cnt2+1
	#print(r,float(cnt1)/float(cnt3),float(cnt2)/float(cnt3))
	#cmp1[ind] = float(cnt1)/float(cnt3)
	ind = ind+1
	print(ind,r,cnt1,cnt2,cnt3) #,cmp1[ind])
#print(cmp1)
