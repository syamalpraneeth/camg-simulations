#!/usr/bin/env python3

##################################################################
##								##                               
##								##
##Dependencies	:						##
##Influences	:						##
##################################################################
## ver.	: 2019--, Syamal Praneeth Chilakalapudi, KIT, INT	##                            
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################

import os, sys
from ovito.io import *
from ovito.modifiers import *
import numpy
import math
import matplotlib.pyplot as plt
from ovito.vis import Viewport

def ovito_voro(fil,case,delsub):

    pipeline = import_file(fil)
    # Set atomic radii (required for polydisperse Voronoi tessellation).
    atom_types = pipeline.source.data.particles['Particle Type'].types
    atom_types[0].radius = 1.40   # Cu atomic radius (atom type 1 in input file)
    atom_types[1].radius = 1.60   # Zr atomic radius (atom type 2 in input file)
    if delsub==1:
        atom_types[2].radius = 1.40   # Cu atomic radius (atom type 1 in input file)
        atom_types[3].radius = 1.60   # Zr atomic radius (atom type 2 in input file)

    data = pipeline.compute()
    at_typ_ind =  data.particles['Particle Type']
    print('Initial Total number of atoms in file',fil," is :",len(at_typ_ind))

    if delsub==1:
        pipeline.modifiers.append(ExpressionSelectionModifier(expression = 'ParticleType < 3'))
        data = pipeline.compute()
        pipeline.modifiers.append(DeleteSelectedModifier()) #Delete all substrate atoms
        data = pipeline.compute()

    # Output an image file of the situation that I am evaluating below
    pipeline.add_to_scene()
    vp = Viewport()
    vp.type = Viewport.Type.Perspective
    vp.camera_pos = (247.653,-179.174, 375.894)
    vp.camera_dir = (-0.62888, 0.4386, -0.6412)
    vp.fov = math.radians(60)
    vp.render_image(size=(800,600), filename=fil[5:]+".png", background=(1,1,1), frame=8)
    pipeline.remove_from_scene()

    # Set up the Voronoi analysis modifier.
    voro = VoronoiAnalysisModifier(
        compute_indices = True,
        use_radii = True,
        edge_threshold = 0.1
    )
    pipeline.modifiers.append(voro)
                      
    data = pipeline.compute() # Let OVITO compute the results.
    atom_types =  data.particles['Particle Type']
    print('Total number of atoms in file before del',fil," is :",len(atom_types))

    if delsub == 1:    
#        #Keep only middle chunk of material, to remove surface atoms
#        exp= 'abs(Position.X)<=90 && abs(Position.Y)<=90 && (Position.Z>20 && Position.Z<=55)'
#        pipeline.modifiers.append(ExpressionSelectionModifier(expression = exp))
#        pipeline.modifiers.append(InvertSelectionModifier(operate_on='particles'))
        pipeline.modifiers.append(ConstructSurfaceModifier(radius = 2.8, select_surface_particles=True))
        data = pipeline.compute()
        
        pipeline.modifiers.append(DeleteSelectedModifier()) #Delete all substrate atoms
        data = pipeline.compute()

    # Output an image file of the situation that I am evaluating below
    pipeline.add_to_scene()
    vp = Viewport()
    vp.type = Viewport.Type.Perspective
    vp.camera_pos = (247.653,-179.174, 375.894)
    vp.camera_dir = (-0.62888, 0.4386, -0.6412)
    vp.fov = math.radians(60)
    vp.render_image(size=(800,600), filename=fil[5:]+"_del.png", background=(1,1,1), frame=8)
    pipeline.remove_from_scene()

    # Access computed Voronoi indices.
    # This is an (N) x (M) array, where M is the maximum face order.
    voro_indices = data.particles['Voronoi Index']
    atom_types =  data.particles['Particle Type']
    print('Total number of atoms in file after del',fil," is :",len(atom_types))
    e_del = []

    for elem in range(0,len(atom_types)):
        if case==0:         
            if delsub==1:
               if atom_types[elem] < 3:
                   e_del.append(elem)
        elif case!=0:
            if atom_types[elem] != case:
                e_del.append(elem)
    voro_ind=numpy.delete(voro_indices,e_del,axis=0)
    print('Voro_indices',numpy.shape(voro_ind),'Case',str(case))
    tot_atms=len(voro_indices)
    print("Number of atoms in file ",fil,", Case",case,": ",len(voro_ind))
    return [voro_ind,tot_atms]

# This helper function takes a two-dimensional array and computes a frequency 
# histogram of the data rows using some NumPy magic. 
# It returns two arrays (of equal length): 
#    1. The list of unique data rows from the input array
#    2. The number of occurences of each unique row
# Both arrays are sorted in descending order such that the most frequent rows 
# are listed first.
def voro(fil,case,delsub):
    siz=8
    sz=siz-1
    a,N = ovito_voro(fil,case,delsub)
    ca = numpy.ascontiguousarray(a).view([('', a.dtype)] * a.shape[1])
    unique, indices, inverse = numpy.unique(ca, return_index=True, return_inverse=True)
    counts = numpy.bincount(inverse)
    sort_indices = numpy.argsort(counts)[::-1]
    sort2=sorted(sort_indices[0:sz])

    print(numpy.shape(counts))
    print(numpy.shape(indices))

    height = []
    bars = []
    ht=[]
    brs=[]

#    ind= a[indices[sort_indices[0:siz]]]
#    cnts=counts[sort_indices[0:siz]]

    # Print the most frequent histogram entries.
#    for i in range(0,len(cnts)):
#        print("%s\t%i\t(%.1f %%)" % (tuple(ind[i,2:6]),
#                                 cnts[i],
#                                 100.0*float(cnts[i])/N))
#        h=100.0* (cnts[i])/(N)
#        height.append(float('%.3f' % h))
#        bars.append('<'+str(ind[i,2])+' '+str(ind[i,3])+' '+str(ind[i,4])+' '+str(ind[i,5])+'>')
#    print('---------------')

    ind= a[indices[sort2]]
    cnts=counts[sort2]
    for i in range(0,len(cnts)):
#        print("%s\t%i\t(%.1f %%)" % (tuple(ind[i,2:6]),
 #                                cnts[i],
  #                               100.0*float(cnts[i])/N))
        h=100.0* (cnts[i])/(N)
        ht.append(float('%.3f' % h))
        brs.append('<'+str(ind[i,2])+' '+str(ind[i,3])+' '+str(ind[i,4])+' '+str(ind[i,5])+'>')

    return [ht, brs];

#def voro(fil,case): #, c):
#    # Compute frequency histogram.
#    ind, counts,N = row_histogram(fil,case)
##    print('size ind',len(ind),'size counts',len(counts))
#    ticks = numpy.empty((10,1))
#    height = []
#    bars = []

#    # Print the most frequent histogram entries.
#    for i in range(0,len(counts)):
#        print("%s\t%i\t(%.1f %%)" % (tuple(ind[i,2:6]),
#                                 counts[i],
#                                 100.0*float(counts[i])/N))
#        h=100.0* (counts[i])/(N)
#        height.append(float('%.3f' % h))
#        bars.append('<'+str(ind[i,2])+' '+str(ind[i,3])+' '+str(ind[i,4])+' '+str(ind[i,5])+'>')
#    return [height,bars];

def voro_data_bulk(fil):
    h1,b1=voro(fil,0,0) #,'All')
    h2,b2=voro(fil,1,0)  #,'Cu-centered')
    h3,b3=voro(fil,2,0)  #,'Zr-centered')
    return [h1,b1,h2,b2,h3,b3];

def voro_data_film(fil):
    h1,b1=voro(fil,0,1)
    h2,b2=voro(fil,3,1)
    h3,b3=voro(fil,4,1)
    return [h1,b1,h2,b2,h3,b3];

def voro_plot_species(h1,b1,h2,b2,h3,b3,h4,b4,e1,e2,e3,siz,species,typ):
    if species==0:
        case='All'
    elif species==1 or species ==3:
        case='Cu'
    elif species==2 or species ==4:
        case='Zr'
    else:
        raise ValueError('species value only 0,1 or 2!')
    if typ==1:
        comm='As Prepared'
        tag='asp'
    elif typ==2:
        comm='Annealed'
        tag='ann'
    else:
        raise ValueError('typ value only 1 or 2!')

    if b1!=b2 or b2!=b3 or b3!=b4 or b4!=b1:
        print('MG',case,b1)
        print(str(e1)+'meV',case,b2)
        print(str(e2)+'meV',case,b3)
        print(str(e3)+'meV',case,b4)
        print('WARNING: This function is only designed for when b1,b2,b3,b4 are equal')

    fig, ax= plt.subplots(1,1,figsize=(12,12))

    w=0.2
    y1 = numpy.arange(len(b1))+1

    ax.set_ylabel('.', color=(0, 0, 0, 0),labelpad=10)

    fig.suptitle('VP for '+str(siz)+'nm $Cu_{50}Zr_{50}$ ('+comm+') : '+case+' atoms', fontsize=20) #, pad=20)
    fig.text(0.5, 0.01, 'Polyhedron Index', ha='center', fontsize='22')
    fig.text(0.01, 0.5, 'Atomic Fraction (at %)', va='center', rotation='vertical',fontsize='20')

    plt.sca(ax)


    p1=ax.bar(y1, h1, width=0.25, label='MG',color='black', edgecolor='black')
    p2=ax.bar(y1+ w, h2, width=0.25, label=str(e1)+'meV',color='white',     edgecolor='black',hatch=".")
    p3=ax.bar(y1+2*w, h3, width=0.25, label=str(e2)+'meV',color='white',  edgecolor='black',hatch="\\")
    p4=ax.bar(y1+3*w, h4, width=0.25, label=str(e3)+'meV',color='white', edgecolor='black',hatch="O")
 
    plt.xticks(y1, b1,rotation=90)

    #plt.legend(handles=[p1],loc='lower right',frameon=False,fontsize=20)
    ax.legend(fontsize=20)

#    ax.invert_yaxis()
    ax.set_ylim([0,7])
    ax.set_ylabel(' ',fontsize=18)
    ax.yaxis.set_label_position('left')
    ax.tick_params(axis="x",direction="in",left='off',labelsize=20)
    ax.tick_params(axis="y",direction="in", bottom="on",top='on',labelsize=20)
    plt.subplots_adjust(bottom=0.4, top=0.8)

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])#
    plt.savefig('voronoi_Cu50Zr50_'+str(siz)+'nm_'+tag+'_'+case+'.png')
    plt.clf()
    plt.close()

def voro_plot_case(h1,b1,h2,b2,h3,b3,siz,val,typ):
    if val=='mg':
        case='MG'
    elif isinstance(val,int)==True:
        case=str(val)+'meV'

    if typ==1:
        comm='As Prepared'
        tag='asp'
    elif typ==2:
        comm='Annealed'
        tag='ann'
    else:
        raise ValueError('typ value only 1 or 2!')

    fig, ax= plt.subplots(1,3,sharex=True,figsize=(12,12))
    y1 = numpy.arange(len(b1))+1
    y2 = numpy.arange(len(b2))+1
    y3 = numpy.arange(len(b3))+1

    ax[0].set_ylabel('.', color=(0, 0, 0, 0),labelpad=10)
    fig.suptitle('VP for '+str(siz)+'nm $Cu_{50}Zr_{50}$: '+case+' '+comm, fontsize=20) #, pad=20)
    fig.text(0.01, 0.5, 'Polyhedron Index', va='center', rotation='vertical',fontsize='22')
    fig.text(0.5, 0.01, 'Atomic Fraction (at %)', ha='center',fontsize='20')

    plt.sca(ax[0])
    p1=ax[0].barh(y1, h1, height=0.25, label='All',color='black', edgecolor='black')
    plt.yticks(y1, b1) #,rotation=90)
    plt.legend(handles=[p1],loc='lower right',frameon=False,fontsize=20)
    ax[0].invert_yaxis()
    ax[0].set_xlim([0,7])
    ax[0].set_xlabel('around all atoms',fontsize=18)
    ax[0].xaxis.set_label_position('top') 
    ax[0].tick_params(axis="y",direction="in",left='off',labelsize=20)
    ax[0].tick_params(axis="x",direction="in", bottom="on",top='on',labelsize=20)
    for i, v in enumerate(h1):
        ax[0].text(v + 0.25, i+1 , str(v), color='blue', fontweight='bold')
    plt.subplots_adjust(bottom=0.4, top=0.8)

    plt.sca(ax[1])
    p2=ax[1].barh(y2, h2, height=0.25,label='Cu',color='black', edgecolor='black')
    plt.yticks(y2, b2) #,rotation=90)
    plt.legend(handles=[p2],loc='lower right',frameon=False,fontsize=20)
    ax[1].invert_yaxis()
    ax[1].set_xlim([0,7])
    ax[1].set_xlabel('around Cu atoms',fontsize=18)
    ax[1].xaxis.set_label_position('top')
    ax[1].tick_params(axis="y",direction="in",left='off',labelsize=20)
    ax[1].tick_params(axis="x",direction="in", bottom="on",top='on',labelsize=20)
    for i, v in enumerate(h2):
        ax[1].text(v + 0.25, i+1 , str(v), color='blue', fontweight='bold')
    plt.subplots_adjust(bottom=0.4) #, top=0.8)

    plt.sca(ax[2])
    p3=ax[2].barh(y3, h3, height=0.25, label='Zr',color='black', edgecolor='black')
    plt.yticks(y3, b3) #,rotation=90)
    plt.legend(handles=[p3],loc='lower right',frameon=False,fontsize=20)
    ax[2].invert_yaxis()
    ax[2].set_xlim([0,7])
    ax[2].set_xlabel('around Zr atoms',fontsize=18)
    ax[2].xaxis.set_label_position('top')
    ax2 = ax[2].twiny()
    ax2.set_xlabel("hi",fontsize=40,color='white',labelpad=4)
    ax2.xaxis.set_label_position('bottom')
    ax2.tick_params(axis="x",top='off',labelsize=0)
    ax[2].tick_params(axis="y",direction="in",left='off',labelsize=20)
    ax[2].tick_params(axis="x",direction="in", bottom="on",top='on',labelsize=20)
    for i, v in enumerate(h3):
        ax[2].text(v + 0.25, i +1, str(v), color='blue', fontweight='bold')
    plt.subplots_adjust(bottom=0.4) #, top=0.8)

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])#
    plt.savefig('voronoi_Cu50Zr50_'+str(siz)+'nm_'+tag+'_'+case+'.png')
    plt.clf()
    plt.close()

def voro_plot_layer(h1,b1,h2,b2,h3,b3,siz,species,typ):
    if species==0:
        case='All'
    elif species==1 or species ==3:
        case='Cu'
    elif species==2 or species ==4:
        case='Zr'
    else:
        raise ValueError('species value only 0,1 or 2!')
    if typ==1:
        comm='As Prepared'
        tag='asp'
    elif typ==2:
        comm='Annealed'
        tag='ann'
    else:
        raise ValueError('typ value only 1 or 2!')

    if b1!=b2 or b2!=b3 or b3!=b1:
        print('lay 1',case,b1)
        print('lay 2',case,b2)
        print('lay 3',case,b3)
        print('WARNING: This function is only designed for when b1,b2,b3 are equal')

    fig, ax= plt.subplots(1,1,figsize=(12,12))

    w=0.2
    y1 = numpy.arange(len(b1))+1

    ax.set_ylabel('.', color=(0, 0, 0, 0),labelpad=10)
    fig.suptitle('VP for '+str(siz)+'nm $Cu_{50}Zr_{50}$ ('+comm+') : '+case+' atoms', fontsize=20) #, pad=20)
    fig.text(0.01, 0.5, 'Polyhedron Index', va='center', rotation='vertical',fontsize='22')
    fig.text(0.5, 0.01, 'Atomic Fraction (at %)', ha='center',fontsize='20')

    plt.sca(ax)


    p1=ax.barh(y1, h1, height=0.25, label='layer 1',color='black', edgecolor='black')
    p2=ax.barh(y1+ w, h2, height=0.25, label='layer 2',color='white',     edgecolor='black',hatch=".")
    p3=ax.barh(y1+2*w, h3, height=0.25, label='layer 3',color='white',  edgecolor='black',hatch="\\")
 
    plt.yticks(y1, b1) #,rotation=90)

    #plt.legend(handles=[p1],loc='lower right',frameon=False,fontsize=20)
    ax.legend(fontsize=20)

    ax.invert_yaxis()
    ax.set_xlim([0,7])
    ax.set_xlabel(' ',fontsize=18)
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis="y",direction="in",left='off',labelsize=20)
    ax.tick_params(axis="x",direction="in", bottom="on",top='on',labelsize=20)
    plt.subplots_adjust(bottom=0.4, top=0.8)

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])#
    plt.savefig('voronoi_Cu50Zr50_layrs_'+str(siz)+'nm_'+tag+'_'+case+'.png')
    plt.clf()
    plt.close()

