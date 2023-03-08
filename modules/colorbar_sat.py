# -*- coding: utf-8 -*-
"""
Created on 2022/06/14
@author: ccl
"""
import matplotlib.colors as mcolors 

def clist_IR(): 
    clist = [(0,    mcolors.cnames['darkgreen']),
             (1/11, mcolors.cnames['cyan']),
             (2/11, mcolors.cnames['black']),
             (3/11, mcolors.cnames['red']),
             (4/11, mcolors.cnames['black']),
             (5/11, mcolors.cnames['yellow']),
             (6/11, mcolors.cnames['lightgrey']),
             (1, mcolors.cnames['black'])]
    return clist

def clist_WV():
    clist = [(0,   mcolors.cnames['saddlebrown']),
             (1/2, '#ffffff'),
             (1,   '#4F3FAE') ]
    return clist

def clist_PMW(): 
    clist = [(0,   mcolors.cnames['cyan']),
             (1/8, mcolors.cnames['blue']),
             (2/8, mcolors.cnames['lawngreen']),
             (3/8, mcolors.cnames['green']),
             (4/8, mcolors.cnames['yellow']),
             (5/8, mcolors.cnames['orange']),
             (6/8, mcolors.cnames['red']),
             (7/8, mcolors.cnames['firebrick']),
             (1,   mcolors.cnames['mediumvioletred'])]
    return clist


def make_cmap(clist_name):
    clist = globals()[clist_name]()
    cmap = mcolors.LinearSegmentedColormap.from_list('my_cmap', clist)
    return cmap
