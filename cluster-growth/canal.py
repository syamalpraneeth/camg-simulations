import numpy as np
import os
import time


def analysis(lmp, comm, rnk, num):

    n = lmp.get_natoms()
    X = np.zeros(1)
    Y = np.zeros(1)
    global msum
    msum = 0
    for i in range(0, num):
        if i == rnk:
            m = lmp.extract_global("nlocal", 0)
            arr1 = np.zeros(m)
            # print(arr1.shape,i,m)
            arr2 = np.zeros(m)
            cvec = lmp.extract_fix("f4", 1, 1, 0, 0)
            ids1 = lmp.extract_atom("id", 0)
            ind = 0
# Element by element copying of at IDs and cluster compute value to a local array
            for x in ids1:
                arr1[ind] = x  # python array indexes from 0
                ind = ind+1
                if ind == m:
                    break
            ind = 0
            for y in cvec:
                arr2[ind] = y
                ind = ind+1
                if ind == m:
                    break
# Append local array to a list, all data will be collected on rank 0
            if i > 0:
                X = comm.recv(source=(rnk-1) % num)
                Y = comm.recv(source=(rnk-1) % num)
            Y = np.append(Y, arr1)  # ,axis=0)
            X = np.append(X, arr2)  # ,axis=0)

            if i == 0:
                X = np.delete(X, 0, 0)
                Y = np.delete(Y, 0, 0)
            comm.send(X, dest=(rnk+1) % num)
            comm.send(Y, dest=(rnk+1) % num)
            time.sleep(0.02)
# Data from all procs will be collected onto rank 0
    if rnk == 0:
        X = comm.recv(source=(rnk-1) % num)
        Y = comm.recv(source=(rnk-1) % num)
# sort cluster compute by atom ID
        Z = [x for _, x in sorted(zip(Y, X))]
# Find out value of the highest cluster number from list
        maxc = 1
        for idx in range(0, n):
            if maxc < int(Z[idx]):
                maxc = int(Z[idx])
# Collect clusters of same cluster IDs together
        clumps = [[] for x in range(0, maxc)]
        for i in range(0, n):
            clumps[int(Z[i]-1)].append(i+1)
# Choosing the biggest cluster out of all the clusters to be our main cluster
        cluster = []
        ind = 0
        mx = 0
        for x in clumps:
            lgt = len(x)
            if lgt > mx:
                cluster = x
                mx = lgt
# Storing all cluster atoms in an array
        cltr = np.array(cluster)
        size = int(len(cltr))
# np.savetxt('clus.txt',cltr,newline='\n',fmt='%i')		#to print out an array to file
        cmdstr = "group keep id "
        for j in range(0, size):
            cmdstr += str(cltr[j])
            cmdstr += " "
    else:
        cmdstr = None
    comm.Barrier()
    # value of command is now in all processes
    cmdstr = comm.bcast(cmdstr, root=0)
    lmp.command(cmdstr)
    return None
