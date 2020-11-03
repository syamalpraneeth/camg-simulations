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

def ovito_rdf(fil,val,delsub):
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

        surfmod=ConstructSurfaceModifier(radius = 2.8, select_surface_particles=True)
        pipeline.modifiers.append(surfmod)
        surfmod.vis.enabled=False
        data = pipeline.compute()
        pipeline.modifiers.append(DeleteSelectedModifier()) #Delete all substrate atoms
        data = pipeline.compute()

    at_typ_ind =  data.particles['Particle Type']
    print('Total number after deleting surface atoms',fil," is :",len(at_typ_ind))


    typ='All'
    rdf1=CoordinationAnalysisModifier(cutoff = 10.0, number_of_bins = 200,partial=True)
    pipeline.modifiers.append(rdf1)
    data = pipeline.compute()
    rdffil='tmp.rdf_'+case #+'_'+str(typ)
    numpy.savetxt(rdffil, data.tables['coordination-rdf'].xy())
    rdf1.enabled = False

#   typ='Cu'
#    elemod1=ExpressionSelectionModifier(expression = 'ParticleType==2 || ParticleType ==4')
#    pipeline.modifiers.append(elemod1)
#    pipeline.modifiers.append(DeleteSelectedModifier())
#    data = pipeline.compute()

#    at_typ_ind =  data.particles['Particle Type']
#    print('Cu atoms',fil," is :",len(at_typ_ind))
#    rdf2=CoordinationAnalysisModifier(cutoff = 10.0, number_of_bins = 200)
#    pipeline.modifiers.append(rdf2)
#    data = pipeline.compute()
#    rdffil='tmp.rdf_'+case+'_'+str(typ)
#    numpy.savetxt(rdffil, data.tables['coordination-rdf'].xy())
#    rdf2.enabled = False
#    elemod1.enabled = False

#    typ='Zr'
#    elemod2=ExpressionSelectionModifier(expression = 'ParticleType==1 || ParticleType ==3')
#    pipeline.modifiers.append(elemod2)
#    pipeline.modifiers.append(DeleteSelectedModifier())
#    data = pipeline.compute()

#    at_typ_ind =  data.particles['Particle Type']
#    print('Zr atoms',fil," is :",len(at_typ_ind))
#    rdf3=CoordinationAnalysisModifier(cutoff = 10.0, number_of_bins = 200)
#    pipeline.modifiers.append(rdf3)
#    data = pipeline.compute()
#    rdffil='tmp.rdf_'+case+'_'+str(typ)
#    numpy.savetxt(rdffil, data.tables['coordination-rdf'].xy())

    return []

def plot_rdf(c,typ):
    i=0
    x1, y1 = [], []
    fil= open('tmp.rdf_'+c+'_All', 'r')
    next(fil)
    next(fil)
    for line in fil:
        values = [float(s) for s in line.split()]
        x1.append(values[0])
        y1.append(values[1])
    fil.close()
    x2, y2 = [], []
    fil= open('tmp.rdf_'+c+'_Cu', 'r')
    next(fil)
    next(fil)
    for line in fil:
        values = [float(s) for s in line.split()]
        x2.append(values[0])
        y2.append(values[1])
    fil.close()
    x3, y3 = [], []
    fil= open('tmp.rdf_'+c+'_Zr', 'r')
    next(fil)
    next(fil)
    for line in fil:
        values = [float(s) for s in line.split()]
        x3.append(values[0])
        y3.append(values[1])
    fil.close()

    if typ==1:
        comm='As Prepared'
        tag='asp'
    elif typ==2:
        comm='Annealed'
        tag='ann'
    else:
        raise ValueError('typ value only 1 or 2!')


    fig, ax= plt.subplots(1,1) #,figsize=(10,5),sharey=True)

    fig.suptitle(r'RDF'+str(siz)+'nm $Cu_{50}Zr_{50}$ '+c, fontsize=20)
    p1=ax.plot(x1,y1, label='All')
    p2=ax.plot(x2,y2, label='Cu')
    p3=ax.plot(x3,y3, label='Zr')


    ax.set_xlabel(r'Pair Separation Distance ($\AA$)', fontsize=18)
    ax.set_ylabel('g(r)',fontsize=18)
#    ax.yaxis.set_label_position('left')
    ax.tick_params(axis="both",direction="in",bottom=True, top=True, left=True, right=True,labelsize=14)
    plt.legend()
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('rdf_Cu50Zr50_'+c+'.png')

def plot_rdf2(c,siz,delsub,typ):
    i=0
    x, y1, y2, y3 = [], [], [], []
    if delsub==1:    fil= open('tmp.rdf_'+str(c)+'meV', 'r')
    else: fil= open('tmp.rdf_'+c, 'r')
#    next(fil)
#    next(fil)
    for line in fil:
        values = [float(s) for s in line.split()]
        x.append(values[0])
#        y1.append(values[1])
        if delsub==1:
            y1.append(values[8])
            y2.append(values[9])
            y3.append(values[10])
        else:
            y1.append(values[1])
            y2.append(values[2])
            y3.append(values[3])

    fil.close()

    if typ==1:
        comm='As Prepared'
        tag='asp'
    elif typ==2:
        comm='Annealed'
        tag='ann'
    else:
        raise ValueError('typ value only 1 or 2!')


    fig, ax= plt.subplots(1,1) #,figsize=(10,5),sharey=True)
    if delsub==1:    fig.suptitle(r'RDF'+str(siz)+'$Cu_{50}Zr_{50}$ '+str(c)+'meV', fontsize=20)
    else: fig.suptitle(r'RDF $Cu_{50}Zr_{50}$ '+c, fontsize=20)
    p1=ax.plot(x,y1, label='Cu-Zr')
    p2=ax.plot(x,y2, label='Cu-Cu')
    p3=ax.plot(x,y3, label='Zr-Zr')


    ax.set_xlabel(r'Pair Separation Distance ($\AA$)', fontsize=18)
    ax.set_ylabel('g(r)',fontsize=18)
#    ax.yaxis.set_label_position('left')
    ax.tick_params(axis="both",direction="in",bottom=True, top=True, left=True, right=True,labelsize=14)
    plt.legend()
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    if delsub==1:
        plt.savefig('rdf_Cu50Zr50_'+str(siz)+'nm_'+str(c)+'meV'+'.png')
    else:
        plt.savefig('rdf_Cu50Zr50_'+c+'.png')

