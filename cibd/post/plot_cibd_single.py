#!/usr/bin/env python3

##################################################################
##PLOT.PY							##                               
##just playing around with matlplotlib features			##
##Dependencies	:						##
##Influences	:						##
##################################################################
## ver.	: 2019--, Syamal Praneeth Chilakalapudi, KIT, INT	##                            
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################

import sys,os
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *
import numpy
import math
import matplotlib.pyplot as plt
from ovito.vis import Viewport
from PySide2.QtCore import Qt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from sklearn.metrics import mean_squared_error
from plotting import plot_four
from plotting import plot_one


#l=[sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]]
l=[sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]]

def rmse_cluster(filnam,R,endquer):
  #go to beginning or end of frame (before dep or after dep)
  pipeline = import_file(filnam)
  n=pipeline.source.num_frames-1
  if endquer == 0:
    n=0
  elif endquer == 1:
    n=n

  sel_sub = ExpressionSelectionModifier(expression = 'i_int != 0')
  pipeline.modifiers.append(sel_sub)
  del_clus= DeleteSelectedModifier()
  pipeline.modifiers.append(del_clus)
  data = pipeline.compute()
  ft= max(data.particles['Position'][:,2])
  print('Filmtop',ft)
  del pipeline.modifiers[0]  
  del pipeline.modifiers[0]

  data = pipeline.compute(n)

  #isolate shell atoms
  pipeline.modifiers.append(ExpressionSelectionModifier(expression = 'i_int != 3'))
  data = pipeline.compute(n)
  pipeline.modifiers.append(DeleteSelectedModifier())
  data = pipeline.compute(n)

#  print(len(data.particles['Particle Type']))

  #find COM of cluster
  export_file(data, "tmp.xyz", "xyz", columns = ["Particle Type","Position.X", "Position.Y", "Position.Z"])
  t, x, y, z = [], [], [], []
  fil= open('tmp.xyz', 'r')
  next(fil)
  next(fil)
  next(fil)
  for line in fil:
    values = [float(s) for s in line.split()]
    t.append(values[0])
    x.append(values[1])
    y.append(values[2])
    z.append(values[3])
  xcom = sum(x)/len(x)
  ycom = sum(y)/len(y)
  zcom = sum(z)/len(z)

  print('COM:',xcom,ycom,zcom)

  #find R from COM
  Ravg = numpy.full((len(x),1),R)
  xsq = numpy.square(numpy.subtract(x,xcom))
  ysq = numpy.square(numpy.subtract(y,ycom))
  zsq = numpy.square(numpy.subtract(z,zcom))
  R_hf = numpy.add(xsq,ysq)
  R = numpy.sqrt(numpy.add(R_hf,zsq))

  #RMSE
  mse=mean_squared_error(Ravg, R)
  rmse=math.sqrt(mse)
  #Rc
  zshf = [y-zcom for y in z]
#  Rup= max(zshf.min(),zshf.max(),key=abs) 
#  Rd= min(zshf.min(),zshf.max(),key=abs)
  Rmx = max(zshf,key=abs)
#  Rd = min(zshf,key=abs)
#  Rc= Rmx - zcom
  C_ht=max(zshf)-min(zshf)
  print(filnam[22:],rmse,Rmx,C_ht)
  return [rmse,Rmx,C_ht]

def vis_cluster_slice(filnam,case,endquer):
  #load file in pipeline
  pipeline = import_file(filnam)
  n=pipeline.source.num_frames-1
#  print(n)
#  if endquer == 0:
#    data = pipeline.source.compute(n)
#  elif endquer == 1:
#    data = pipeline.source.compute(0)

  #colour modifier
  pipeline.modifiers.append(ColorCodingModifier(property = 'i_int',start_value=1,end_value=3, gradient = ColorCodingModifier.Magma()))
  #slice
  pipeline.modifiers.append(SliceModifier(normal=(1,0,0)))
  data = pipeline.compute()
  #vis and output
  pipeline.add_to_scene()
  vp = Viewport()
  vp.type = Viewport.Type.Ortho
  vp.camera_pos = (-0.932023,0.935124, 33.0832)
  vp.camera_dir = (-1, 0, 0)
  vp.fov = 72.2929
  if endquer == 1:
    vp.render_image(size=(800,600), filename=fil[22:]+"_slice.png", background=(1,1,1), frame=n)
  elif endquer == 0:
    vp.render_image(size=(800,600), filename=fil[22:]+"_slice.png", background=(1,1,1), frame=0)
  pipeline.remove_from_scene()
  #delete pipeline

#for all values of dep: vis cluster slice
#get rmse values, plot rmse values


Tab=numpy.zeros((len(l)+1,3))
cnt=0
i=50
fil='../data/lammpstrj.dep.cibd_3nm_'+str(i)+'eV'
[Tab[cnt,0],Tab[cnt,1],Tab[cnt,2]]=rmse_cluster(fil,15,0)
xlab=['Undeposited']
cnt+=1

#os._exit(1)

for i in l:
#  fil=['../data/lammpstrj.dep.cibd_3nm_'+str(x)+'eV' for x in l]
  fil='../data/lammpstrj.dep.cibd_3nm_'+str(i)+'eV'
  [Tab[cnt,0],Tab[cnt,1],Tab[cnt,2]]=rmse_cluster(fil,15,1)
  vis_cluster_slice(fil,i,1)
  xlab.append(str(i)+'eV')
  cnt+=1

#print(Tab)

fig,ax = plt.subplots()
ax2=ax.twinx()
ax3=ax.twinx()

x = numpy.arange(len(xlab))+1

p1,=ax.plot(x, Tab[:,0],'b^-', label = '$RMSD_{shell}$')
p2,=ax2.plot(x, Tab[:,1],'rs-', label = '$R_{curvature}$')
p3,=ax3.plot(x,Tab[:,2],'g*-',label = '$Z-thick_{clus}$')
plt.xticks(x, xlab,rotation=45)

fig.suptitle('Single'+fil[27]+'nm $Cu_{50}Zr_{50}$ Cluster Deposited States', fontsize=14)
#ax.set_yticks(numpy.round(numpy.linspace(ax.get_ybound()[0], ax.get_ybound()[1]),3),10)
#ax2.set_yticks(numpy.round(numpy.linspace(ax2.get_ybound()[0], ax2.get_ybound()[1]),3),5)
#ax.set_xlabel('xlab',fontsize=12)
ax.set_ylabel('RMSD of the Shell Atoms',fontsize=12)
ax2.set_ylabel('Radius of Curvature $R_{curvature}$ $(\AA)$',fontsize=12)
ax3.set_ylabel('Thickness of cluster in Z axis $Z-thick_{clus}$ $(\AA)$',fontsize=12)
ax.tick_params(axis="x",which="in",direction="in",bottom=True, top=True) #,colors=p1.get_color())
ax.tick_params(axis="y",which="both",direction="in",left=True, right=False,colors=p1.get_color())
ax2.tick_params(axis="y",which="both",direction="in",left=False,right=True,colors=p2.get_color())
ax3.tick_params(axis="y",which="both",direction="in",right=True,colors=p3.get_color())

ax.yaxis.label.set_color(p1.get_color())
ax2.yaxis.label.set_color(p2.get_color())
ax3.yaxis.label.set_color(p3.get_color())

ax.spines["left"].set_color(p1.get_color())
ax2.spines["right"].set_color(p2.get_color())
ax3.spines["right"].set_color(p3.get_color())
ax3.spines["right"].set_position(("axes", 1.2))

fig.legend(bbox_to_anchor=(0.3, 0.7, 0.2, 0.2),loc=3)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])#
fig.savefig('clus_'+fil[27]+'nm.png')
plt.clf()
plt.close()



os._exit(1)

[f1,f2,f3,f4,n,x1,y1,x2,y2,x3,y3,x4,y4,xl,yl,ti,l1,l2,l3,l4]=['tmp.log.asp_'+str(l[0])+"eV",
'tmp.log.asp_'+str(l[1])+"eV",'tmp.log.asp_'+str(l[2])+"eV",'tmp.log.asp_'+str(l[3])+"eV",
'clus_asph',
0,1,0,1,0,1,0,1,
'Timesteps',
r'Asphericity $R_Z / R_{XY}$',
'Cluster Asphericity: Single Cluster Deposition',
str(l[0])+"eV",str(l[1])+"eV",str(l[2])+"eV",str(l[3])+"eV"]
plot_four(f1,f2,f3,f4,n,x1,y1,x2,y2,x3,y3,x4,y4,xl,yl,ti,l1,l2,l3,l4)

