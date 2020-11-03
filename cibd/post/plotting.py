#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

def plot_one(filnam,name,x1col,y1col,xlab,ylab,title,leg1):
    x1, x2, y1, y2 = [], []
    for line in open(filnam, 'r'):
        values = [float(s) for s in line.split()]
        x1.append(values[x1col])
        y1.append(values[y1col])

    fig = plt.figure()
    ax = plt.gca()
    plt.plot(x1, y1,'^', label = leg1)
    fig.suptitle(title, fontsize=14)
    plt.xlabel(xlab,fontsize=12)
    plt.ylabel(ylab,fontsize=12)
    ax.tick_params(axis="both",direction="in",bottom=True, top=True, left=True, right=True)
#    ax.tick_params(axis="y",direction="in")
    plt.legend()
    #plt.legend(bbox_to_anchor=(1.01, 0.8, 0.3, 0.2), loc='upper left')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(name+'.png')
    plt.clf()
    plt.close()

def plot_two(filnam,name,x1col,y1col,x2col,y2col,xlab,ylab,title,leg1,leg2):
    x1, x2, y1, y2 = [], [], [], []
    for line in open(filnam, 'r'):
        values = [float(s) for s in line.split()]
        x1.append(values[x1col])
        y1.append(values[y1col])
        x2.append(values[x2col])
        y2.append(values[y2col])

    fig = plt.figure()
    ax = plt.gca()
    plt.plot(x1, y1,'^-', label = leg1)
    plt.plot(x2, y2,'s-', label = leg2)
#    plt.hlines(0.5,0,1,'dashed')
#    plt.text(0.5, 0, 'Metallic glass composition', fontsize=12)
    fig.suptitle(title, fontsize=14)
    plt.xlabel(xlab,fontsize=12)
    plt.ylabel(ylab,fontsize=12)
    ax.tick_params(axis="both",direction="in",bottom=True, top=True, left=True, right=True)
#    ax.tick_params(axis="y",direction="in")
    plt.legend()
    #plt.legend(bbox_to_anchor=(1.01, 0.8, 0.3, 0.2), loc='upper left')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(name+'.png')
    plt.clf()
    plt.close()

def plot_three(f1,f2,n,x1c,y1c,x2c,y2c,x3c,y3c,xlab,ylab,ylab2,title,leg1,leg2,leg3):
    x1, x2, x3, y1, y2, y3 = [], [], [], [], [], []
    for line in open(f1, 'r'):
        values = [float(s) for s in line.split()]
        x1.append(values[x1c])
        y1.append(values[y1c])
        x2.append(values[x2c])
        y2.append(values[y2c])
    for line in open(f2, 'r'):
        values = [float(s) for s in line.split()]
        x3.append(values[x3c])
        y3.append(values[y3c])

    fig,ax = plt.subplots()
#    ax = plt.gca()
    ax2=ax.twinx()
    p1=ax.plot(x1, y1,'^-', label = leg1)
    p2=ax.plot(x2, y2,'s-', label = leg2)
    p3,=ax2.plot(x3,y3,'b:',label = leg3)
#    plt.hlines(0.5,0,1,'dashed')
#    plt.text(0.5, 0, 'Metallic glass composition', fontsize=12)
    fig.suptitle(title, fontsize=14)
    ax.set_yticks(np.round(np.linspace(ax.get_ybound()[0], ax.get_ybound()[1]),3),5)
    ax2.set_yticks(np.round(np.linspace(ax2.get_ybound()[0], ax2.get_ybound()[1]),3),5)
    ax.set_xlabel(xlab,fontsize=12)
    ax.set_ylabel(ylab,fontsize=12)
    ax2.set_ylabel(ylab2,fontsize=12)
    ax.tick_params(axis="both",which="both",direction="in",bottom=True, top=True, left=True, right=False)
    ax2.tick_params(axis="both",which="both",direction="in",bottom=True, top=True, left=False, right=True,colors=p3.get_color())
    ax2.yaxis.label.set_color(p3.get_color())
    ax2.spines["right"].set_color(p3.get_color())
    fig.legend(bbox_to_anchor=(0.12, 0.1, 0.2, 0.2),loc=3)
    fig.savefig(n+'.png')
    plt.clf()
    plt.close()

def plot_four(f1,f2,f3,f4,n,x1c,y1c,x2c,y2c,x3c,y3c,x4c,y4c,xlab,ylab,title,leg1,leg2,leg3,leg4):
    x1, x2, x3, x4, y1, y2, y3, y4 = [], [], [], [], [], [], [], []
    for line in open(f1, 'r'):
        values = [float(s) for s in line.split()]
        x1.append(values[x1c])
        y1.append(values[y1c])
    for line in open(f2, 'r'):
        values = [float(s) for s in line.split()]
        x2.append(values[x2c])
        y2.append(values[y2c])
    for line in open(f3, 'r'):
        values = [float(s) for s in line.split()]
        x3.append(values[x3c])
        y3.append(values[y3c])
    for line in open(f4, 'r'):
        values = [float(s) for s in line.split()]
        x4.append(values[x4c])
        y4.append(values[y4c])

    fig,ax = plt.subplots()
#    ax = plt.gca()
#    ax2=ax.twinx()
    p1=ax.plot(x1, y1,'^-', label = leg1)
    p2=ax.plot(x2, y2,'s-', label = leg2)
    p3=ax.plot(x3, y3,'o-', label = leg3)
    p4=ax.plot(x4, y4,'*-', label = leg4)
#    plt.hlines(0.5,0,1,'dashed')
#    plt.text(0.5, 0, 'Metallic glass composition', fontsize=12)
    fig.suptitle(title, fontsize=14)
    ax.set_yticks(np.round(np.linspace(ax.get_ybound()[0], ax.get_ybound()[1]),3),5)
#    ax2.set_yticks(np.round(np.linspace(ax2.get_ybound()[0], ax2.get_ybound()[1]),3),5)
    ax.set_xlabel(xlab,fontsize=12)
    ax.set_ylabel(ylab,fontsize=12)
#   ax2.set_ylabel(ylab2,fontsize=12)
    ax.tick_params(axis="both",which="both",direction="in",bottom=True, top=True, left=True, right=False)
#    ax2.tick_params(axis="both",which="both",direction="in",bottom=True, top=True, left=False, right=True,colors=p3.get_color())
#    ax2.yaxis.label.set_color(p3.get_color())
#    ax2.spines["right"].set_color(p3.get_color())
#    fig.legend(bbox_to_anchor=(0.12, 0.1, 0.2, 0.2),loc=1)
    plt.legend(loc=1)
    fig.savefig(n+'.png')
    plt.clf()
    plt.close()
