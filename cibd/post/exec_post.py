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
import matplotlib.pyplot as plt

from pe_atom import ovito_pote
from pe_atom import pe_plot_species
from rdf import ovito_rdf
from rdf import plot_rdf
from rdf import plot_rdf2
from voronoi import voro_data_bulk
from voronoi import voro_data_film
from voronoi import voro_plot_species
from voronoi import voro_plot_case

#pe/atom AS_PREPARED
ovito_pote('lammpstrj.dep.cibd_pe-atom_3nm_60meV',60,1)
ovito_pote('lammpstrj.dep.cibd_pe-atom_3nm_300meV',300,1)
ovito_pote('lammpstrj.dep.cibd_pe-atom_3nm_600meV',600,1)
ovito_pote('lammpstrj.dep.msr_pe-atom','mg',0)
pe_plot_species('60meV','300meV','600meV','MG',3,1)

#pe/atom AS_ANNEALED
ovito_pote('lammpstrj.dep.cibd_pe-atom_anneal_3nm_60meV',60,1)
ovito_pote('lammpstrj.dep.cibd_pe-atom_anneal_3nm_300meV',300,1)
ovito_pote('lammpstrj.dep.cibd_pe-atom_anneal_3nm_600meV',600,1)
ovito_pote('lammpstrj.dep.msr_anneal_pe-atom','mg',0)
pe_plot_species('60meV','300meV','600meV','MG',3,2)


#rdf AS_PREPARED
ovito_rdf('lammpstrj.dep.cibd_pe-atom_3nm_60meV',60,1)
ovito_rdf('lammpstrj.dep.cibd_pe-atom_3nm_300meV',300,1)
ovito_rdf('lammpstrj.dep.cibd_pe-atom_3nm_600meV',600,1)
ovito_rdf('lammpstrj.dep.msr_pe-atom','mg',0)

plot_rdf2(60,3,1,1)
plot_rdf2(300,3,1,1)
plot_rdf2(600,3,1,1)
plot_rdf2('MG',3,0,1)

#voronoi AS_PREPARED
h1a,b1a,h1b,b1b,h1c,b1c = voro_data_bulk('data.msr')
h2a,b2a,h2b,b2b,h2c,b2c = voro_data_film('data.cibd_Cu50Zr50_3nm_60meV-lay5')
h3a,b3a,h3b,b3b,h3c,b3c = voro_data_film('data.cibd_Cu50Zr50_3nm_300meV-lay5')
h4a,b4a,h4b,b4b,h4c,b4c = voro_data_film('data.cibd_Cu50Zr50_3nm_600meV-lay5')

#voro_plot_species(h1,b1,h2,b2,h3,b3,e1,e2,e3,siz,species,typ)
voro_plot_species(h1a,b1a,h2a,b2a,h3a,b3a,h4a,b4a,60,300,600,3,0,1)
voro_plot_species(h1b,b1b,h2b,b2b,h3b,b3b,h4b,b4b,60,300,600,3,1,1)
voro_plot_species(h1c,b1c,h2c,b2c,h3c,b3c,h4c,b4c,60,300,600,3,2,1)

voro_plot_case(h1a,b1a,h1b,b1b,h1c,b1c,3,'mg',1)
voro_plot_case(h2a,b2a,h2b,b2b,h2c,b2c,3,60,1)
voro_plot_case(h3a,b3a,h3b,b3b,h3c,b3c,3,300,1)
voro_plot_case(h4a,b4a,h4b,b4b,h4c,b4c,3,600,1)

#h2a1,b2a1,h2b1,b2b1,h2c1,b2c1 = voro_data_film('data.cibd_Cu50Zr50_3nm_50eV-lay1')
#h2a2,b2a2,h2b2,b2b2,h2c2,b2c2 = voro_data_film('data.cibd_Cu50Zr50_3nm_50eV-lay2')
#h2a3,b2a3,h2b3,b2b3,h2c3,b2c3 = voro_data_film('data.cibd_Cu50Zr50_3nm_50eV-lay3')
#voro_plot_layer(h2a1,b2a1,h2a2,b2a2,h2a3,b2a3,0,1)
#voro_plot_layer(h2b1,b2b1,h2b2,b2b2,h2b3,b2b3,3,1)
#voro_plot_layer(h2c1,b2c1,h2c2,b2c2,h2c3,b2c3,4,1)


#voronoi ANNEALED
h1a,b1a,h1b,b1b,h1c,b1c = voro_data_bulk('data.msr_anneal')
h2a,b2a,h2b,b2b,h2c,b2c = voro_data_film('data.cibd_anneal_3nm_60meV')
h3a,b3a,h3b,b3b,h3c,b3c = voro_data_film('data.cibd_anneal_3nm_300meV')
h4a,b4a,h4b,b4b,h4c,b4c = voro_data_film('data.cibd_anneal_3nm_600meV')

#voro_plot_species(h1,b1,h2,b2,h3,b3,e1,e2,e3,siz,species,typ)
voro_plot_species(h1a,b1a,h2a,b2a,h3a,b3a,h4a,b4a,60,300,600,3,0,2)
voro_plot_species(h1b,b1b,h2b,b2b,h3b,b3b,h4b,b4b,60,300,600,3,1,2)
voro_plot_species(h1c,b1c,h2c,b2c,h3c,b3c,h4c,b4c,60,300,600,3,2,2)

voro_plot_case(h1a,b1a,h1b,b1b,h1c,b1c,3,'mg',2)
voro_plot_case(h2a,b2a,h2b,b2b,h2c,b2c,3,60,2)
voro_plot_case(h3a,b3a,h3b,b3b,h3c,b3c,3,300,2)
voro_plot_case(h4a,b4a,h4b,b4b,h4c,b4c,3,600,2)

