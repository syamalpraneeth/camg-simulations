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
from ovito.vis import *
import numpy
import math
import matplotlib.pyplot as plt
from ovito.vis import Viewport
from PySide2.QtCore import Qt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

def ovito_pote(fil,val,delsub):
    if val=='mg':
        case='MG'
    elif isinstance(val,int)==True:
        case=str(val)+'meV'

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
    if delsub == 1: vp.camera_pos = (247.653,-179.174, 375.894)
    else: vp.camera_pos = (244.629,-240.204, 267.718)
    vp.camera_dir = (-0.62888, 0.4386, -0.6412)
    if delsub == 1:  vp.fov = math.radians(60)
    else: vp.fov = vp.fov = math.radians(35)
    vp.render_image(size=(800,600), filename=fil[10:]+".png", background=(1,1,1), frame=8)
    pipeline.remove_from_scene()

    atom_types =  data.particles['Particle Type']
    print('Total number of atoms in file before del',fil," is :",len(atom_types))

    #Output only 
    modifier = HistogramModifier(bin_count=100, property='c_c2')
    pipeline.modifiers.append(modifier)
    histfil='tmp.histo_'+case
    export_file(pipeline, histfil, "txt/table", key="histogram[c_c2]")

    if delsub == 1:    
        surfmod=ConstructSurfaceModifier(radius = 2.8, select_surface_particles=True)
        pipeline.modifiers.append(surfmod)
        surfmod.vis.enabled=False
        data = pipeline.compute()
        pipeline.modifiers.append(DeleteSelectedModifier()) #Delete all substrate atoms
        data = pipeline.compute()

    # Output an image file of the situation that I am evaluating below
    pipeline.add_to_scene()
    vp = Viewport()
    vp.type = Viewport.Type.Perspective
    if delsub == 1: vp.camera_pos = (247.653,-179.174, 375.894)
    else: vp.camera_pos = (244.629,-240.204, 267.718)
    vp.camera_dir = (-0.62888, 0.4386, -0.6412)
    if delsub == 1:  vp.fov = math.radians(60)
    else: vp.fov = vp.fov = math.radians(35)    
    vp.render_image(size=(800,600), filename=fil[10:]+"_del.png", background=(1,1,1), frame=8)
    pipeline.remove_from_scene()

    atom_types =  data.particles['Particle Type']
    print('Total number of atoms in file after del',fil," is :",len(atom_types))

    pipeline.modifiers.append(ExpressionSelectionModifier(expression = 'ParticleType==2 || ParticleType ==4'))
    pipeline.modifiers.append(DeleteSelectedModifier())

    pipeline.modifiers.append(CoordinationAnalysisModifier(cutoff = 5.0, number_of_bins = 200))
    data = pipeline.compute()
    rdffil='tmp.rdf_'+case
    numpy.savetxt(rdffil, data.tables['coordination-rdf'].xy())
    
    z=20
    t=20
    pipeline.modifiers.append(SliceModifier(distance=z,normal=(0,0,1),slab_width=t))
    ol = TextLabelOverlay(
    text = r'Slice @ Z='+str(z)+', Slab width = '+str(t)+'$\AA$ for Cu50Zr50 film '+case,
    alignment = Qt.AlignHCenter ^ Qt.AlignTop,
    offset_y = 0.020,
    font_size = 0.03,
    text_color = (0,0,0))

    pipeline.add_to_scene()
    vp = Viewport()
    vp.overlays.append(ol)
    vp.type = Viewport.Type.Top
    if delsub == 1:  vp.camera_pos = (0,0, 0)
    else:  vp.camera_pos = (36.84,36.84,36.845)
    vp.camera_dir = (0, 0, -1)
    if delsub == 1:  vp.fov = 123
    else: vp.fov = 83.34
    vp.render_image(size=(800,600), filename=fil[10:]+"_slice.png", background=(1,1,1), frame=8)
    pipeline.remove_from_scene()

    color_mod = ColorCodingModifier(property = 'c_c2',start_value=-3.79,end_value=-2.73)
    pipeline.modifiers.append(color_mod)

    ol2 = ColorLegendOverlay(
    modifier = color_mod,
    title = 'P.E./ Cu atom:',
    alignment = Qt.AlignRight ^ Qt.AlignBottom,
    orientation = Qt.Vertical,
    offset_y = 0.04,
    font_size = 0.08,
#    label1 = 'Highest',
#    label2 = 'Lowest',
    format_string = '%.2f eV')
    
    pipeline.add_to_scene()
    vp = Viewport()
    vp.overlays.append(ol)
    vp.overlays.append(ol2)
    vp.type = Viewport.Type.Top
    if delsub == 1:  vp.camera_pos = (0,0, 0)
    else:  vp.camera_pos = (36.84,36.84,36.845)
    vp.camera_dir = (0, 0, -1)
    if delsub == 1:  vp.fov = 123
    else: vp.fov = 83.34
    vp.render_image(size=(800,600), filename=fil[10:]+"_slice-color.png", background=(1,1,1), frame=8)
    pipeline.remove_from_scene()
    return []

def pe_plot_species(c1,c2,c3,c4,siz,typ):
    i=0
    for c in [c1,c2,c3,c4]:
        x1, y1 = [], []
        fil= open('tmp.histo_'+c, 'r')
        next(fil)
        next(fil)
        for line in fil:
            values = [float(s) for s in line.split()]
            x1.append(values[0])
            y1.append(values[1])
        fil.close()
#        print(x1))
#        print(len(y1))
        if i == 0:
            x = numpy.zeros((len(x1),4))
            y = numpy.zeros((len(y1),4))
        x[:,i] = numpy.array(x1).reshape(len(x1))
        y[:,i] = numpy.array(y1).reshape(len(y1))
        i+=1
#    print(x)
#    print(y)

    y_norm = y / y.max(axis=0)
#    print(y_norm)

    if typ==1:
        comm='As Prepared'
        tag='asp'
    elif typ==2:
        comm='Annealed'
        tag='ann'
    else:
        raise ValueError('typ value only 1 or 2!')

    fig, (ax,ax2)= plt.subplots(1,2,figsize=(10,5),sharey=True)

    fig.suptitle('Potential Energy per atom: '+str(siz)+'nm $Cu_{50}Zr_{50}$ CAMGs ('+comm+')', fontsize=20) #, pad=20)

    plt.sca(ax)

    p1=ax.plot(x[:,0],y_norm[:,0], label=c1)
    p2=ax.plot(x[:,1],y_norm[:,1], label=c2)
    p3=ax.plot(x[:,2],y_norm[:,2], label=c3)
    p4=ax.plot(x[:,3],y_norm[:,3],':' ,label=c4)
    p1=ax2.plot(x[:,0],y_norm[:,0], label=c1)
    p2=ax2.plot(x[:,1],y_norm[:,1], label=c2)
    p3=ax2.plot(x[:,2],y_norm[:,2], label=c3)
    p4=ax2.plot(x[:,3],y_norm[:,3], ':',label=c4)
 
    ax.legend(fontsize=12, bbox_to_anchor=(1.15, 0.4), loc='upper right')

    ax.set_xlabel('P.E. per Zr Atom (eV)', fontsize=18)
    ax2.set_xlabel('P.E. per Cu Atom (eV)', fontsize=18)
    ax.set_ylabel('Normalised Counts ',fontsize=18)
    ax.yaxis.set_label_position('left')
    ax.tick_params(axis="both",direction="in",bottom=True, top=True, left=True, right=False,labelsize=14)
    ax2.tick_params(axis="both",direction="in",bottom=True, top=True, left=False, right=True,labelsize=14)
    plt.subplots_adjust(bottom=0.4, top=0.8)
    
    ax.set_ylim(0.0,1.1)
    #ax2.set_ylim(0.0,1.1)
    ax.set_xlim(-7, -5)  # outliers only
    ax2.set_xlim(-4, -2)  # most of the data
    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)

#    axins1=ax.inset_axes([0.5, 0.5, 0.4, 0.4])
#    axins2=ax.inset_axes([0.5, 0.5, 0.4, 0.4])

    axins1 = inset_axes(ax,
                    width="50%", # width = 30% of parent_bbox
                    height=1., # height : 1 inch
                    loc=1)
    axins2 = inset_axes(ax2,
                    width="50%", # width = 30% of parent_bbox
                    height=1., # height : 1 inch
                    loc=1)


    axins1.plot(x[:,0],y_norm[:,0], label=c1)
    axins1.plot(x[:,1],y_norm[:,1], label=c2)
    axins1.plot(x[:,2],y_norm[:,2], label=c3)
    axins1.plot(x[:,3],y_norm[:,3],':', label=c4)
    axins2.plot(x[:,0],y_norm[:,0], label=c1)
    axins2.plot(x[:,1],y_norm[:,1], label=c2)
    axins2.plot(x[:,2],y_norm[:,2], label=c3)
    axins2.plot(x[:,3],y_norm[:,3],':', label=c4)
    x1, x2, y1, y2 = -6.5,-6.3,0.4,1.1
    axins1.set_xlim(x1, x2)
    axins1.set_ylim(y1, y2)
    x1, x2, y1, y2 = -3.6,-3.4,0.4,1.1
    axins2.set_xlim(x1, x2)
    axins2.set_ylim(y1, y2)
    mark_inset(ax, axins1, loc1=2, loc2=4, fc="none", ec="0.5")
    mark_inset(ax2, axins2, loc1=2, loc2=4, fc="none", ec="0.5")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('pe-atom_Cu50Zr50_'+str(siz)+'nm_'+tag+'.png')
    plt.clf()
    plt.close()
