# -*- coding: utf-8 -*-
"""
Created on Mondat, Jan 22nd, 2024
@author: ben g
Python module for simulations with Lumerical
"""
import lumerical as lum
import numpy as np
from numpy import genfromtxt
from numpy import abs
from scipy import signal as si
# from scipy.integrate import simps
from scipy.optimize import minimize
from scipy.constants import pi, c
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as patches
import imp
import time
import csv

#default material values
# material_substrate = "SiO2_analytic"
# material_cladding = "SiO2_MDL_200nmTo1680nm_ONLY"
# material_thinfilm = "LN_Scripted"

def initializeMODE():
    global MODE
    lumapi = imp.load_source("lumapi", "C:/Program Files/Lumerical/v232/api/python/lumapi.py")
    MODE = lumapi.MODE("Template.lms")

#This annoying function enables us to use variables between the python script and this file.
# NEXT: MAKE SURE GLOBALS ARE USED.
def defineGlobals(wlt, h_LNt, h_etcht, h_substratet, h_claddingt, w_wgt, angle_swt, chip_width, 
                  m_sub = "SiO2_analytic", m_clad = "SiO2_analytic", m_TF = "LN_Scripted"):
    global wl, h_LN, h_etch, h_substrate, h_cladding, w_wg, angle_sw, wc, zt, zb, trim
    global offset_min, l_wg_margin, slab_margin, w_slab_min, mesh_margin
    global material_substrate, material_cladding, material_thinfilm

    wl = wlt
    h_LN = h_LNt
    h_etch = h_etcht
    h_substrate = h_substratet
    h_cladding = h_claddingt
    w_wg = w_wgt
    angle_sw = angle_swt
    
    material_substrate = m_sub
    material_cladding = m_clad
    material_thinfilm = m_TF
    
    print("material_cladding: "+material_cladding)
    print("material_thinfilm: "+material_thinfilm)
    print("material_substrate: "+material_substrate)
    
    #Derived Parameters
    ωc = 2*pi*c/wl

    #Defining top and bottom of MMI and waveguides (not including slab)
    zt = h_LN
    zb = zt-h_etch

    # Define the sidewall angle and hence the trim length
    trim = h_etch/np.tan(angle_sw)
    offset_min = w_wg/2+trim
    
    l_wg_margin = 0.1e-6
    slab_margin = chip_width
    w_slab_min = 2*(w_wg/2+trim+offset_min+slab_margin)
    mesh_margin = 7.5e-6

def switchtolayout():
    MODE.switchtolayout()

def drawWGMid(l_wg):
    #Bottom surface verticies
    x1 = 0
    y1 = -w_wg/2-trim

    x2 = l_wg
    y2 = -w_wg/2-trim

    x3 = l_wg
    y3 = w_wg/2+trim

    x4 = 0
    y4 = w_wg/2+trim

    #Top surface verticies
    x5 = 0
    y5 = -w_wg/2

    x6 = l_wg
    y6 = -w_wg/2

    x7 = l_wg
    y7 = w_wg/2

    x8 = 0
    y8 = w_wg/2
    
    # construct matrix for verticies
    vtx = np.array([[x1,y1,zb], #Vertex 1
                    [x2,y2,zb], #Vertex 2
                    [x3,y3,zb], #Vertex 3
                    [x4,y4,zb], #Vertex 4
                    [x5,y5,zt], #Vertex 5
                    [x6,y6,zt], #Vertex 6
                    [x7,y7,zt], #Vertex 7
                    [x8,y8,zt]]) #Vertex 8

    #construct matrix which groups verticies into facets.
    b = np.transpose(np.array([ [[1,2,6,5]], 
                                [[2,3,7,6]], 
                                [[3,4,8,7]], 
                                [[4,1,5,8]], 
                                [[5,6,7,8]], 
                                [[1,2,3,4]]]))
    
    # Draw tha darn thing
    MODE.switchtolayout()
    MODE.method_type = 2
    MODE.addplanarsolid()
    MODE.set('vertices',vtx)
    MODE.set('facets',b)
    MODE.set("name","wg_in")
    MODE.set("material", material_thinfilm)
    MODE.set("alpha", 0.5)
    MODE.set("override mesh order from material database", 1)
    MODE.set("mesh order", 1)
    time.sleep(0.1)    
    
def drawConformalCladding(l_wg, h_cladding):
    if(h_cladding != 0):

        w_wg_clad = w_wg +2*h_cladding/np.sqrt(3)
        zb_clad = zb + h_cladding
        zt_clad = zt + h_cladding
        
        #Bottom surface verticies
        x1 = 0
        y1 = -w_wg_clad/2-trim

        x2 = l_wg
        y2 = -w_wg_clad/2-trim

        x3 = l_wg
        y3 = w_wg_clad/2+trim

        x4 = 0
        y4 = w_wg_clad/2+trim

        #Top surface verticies
        x5 = 0
        y5 = -w_wg_clad/2

        x6 = l_wg
        y6 = -w_wg_clad/2

        x7 = l_wg
        y7 = w_wg_clad/2

        x8 = 0
        y8 = w_wg_clad/2

        # construct matrix for verticies
        vtx = np.array([[x1,y1,zb_clad], #Vertex 1
                        [x2,y2,zb_clad], #Vertex 2
                        [x3,y3,zb_clad], #Vertex 3
                        [x4,y4,zb_clad], #Vertex 4
                        [x5,y5,zt_clad], #Vertex 5
                        [x6,y6,zt_clad], #Vertex 6
                        [x7,y7,zt_clad], #Vertex 7
                        [x8,y8,zt_clad]]) #Vertex 8

        #construct matrix which groups verticies into facets.
        b = np.transpose(np.array([ [[1,2,6,5]], 
                                    [[2,3,7,6]], 
                                    [[3,4,8,7]], 
                                    [[4,1,5,8]], 
                                    [[5,6,7,8]], 
                                    [[1,2,3,4]]]))

        # Draw tha darn thing
        MODE.switchtolayout()
        MODE.method_type = 2
        MODE.addplanarsolid()
        MODE.set('vertices',vtx)
        MODE.set('facets',b)
        MODE.set("name","wg_cladding")
        MODE.set("material", material_cladding)
        MODE.set("alpha", 0.5)
        MODE.set("override mesh order from material database", 1)
        MODE.set("mesh order", 3)
        
        #Draw the brick
        x1 = -l_wg_margin
        x2 = l_wg+l_wg_margin

        y1 = -slab_margin/2
        y4 = slab_margin/2 

        x4 = x1
        x5 = x1
        x8 = x1

        x3 = x2
        x6 = x2
        x7 = x2

        y2 = y1
        y5 = y1
        y6 = y1

        y3 = y4
        y7 = y4
        y8 = y4

        # construct matrix for verticies
        vtx = np.array([[x1,y1,0], #Vertex 1
                        [x2,y2,0], #Vertex 2
                        [x3,y3,0], #Vertex 3
                        [x4,y4,0], #Vertex 4
                        [x5,y5,zb_clad], #Vertex 5
                        [x6,y6,zb_clad], #Vertex 6
                        [x7,y7,zb_clad], #Vertex 7
                        [x8,y8,zb_clad]]) #Vertex 8

        #construct matrix which groups verticies into facets.
        b = np.transpose(np.array([ [[1,2,6,5]], 
                                    [[2,3,7,6]], 
                                    [[3,4,8,7]], 
                                    [[4,1,5,8]], 
                                    [[5,6,7,8]], 
                                    [[1,2,3,4]]]))

        # Draw tha darn thing
        MODE.switchtolayout()
        MODE.method_type = 2
        MODE.addplanarsolid()
        MODE.set('vertices',vtx)
        MODE.set('facets',b)
        MODE.set("name","slab_cladding")
        MODE.set("material", material_cladding)
        MODE.set("alpha", 0.5)
        MODE.set("override mesh order from material database", 1)
        MODE.set("mesh order", 3)
        time.sleep(0.1)
    
    
def drawWGIn(l_wg, offset):
    #Bottom surface verticies
    x1 = -l_wg_margin
    y1 = offset-w_wg/2-trim

    x2 = l_wg
    y2 = offset-w_wg/2-trim

    x3 = l_wg
    y3 = offset+w_wg/2+trim

    x4 = -l_wg_margin
    y4 = offset+w_wg/2+trim

    #Top surface verticies
    x5 = -l_wg_margin
    y5 = -w_wg/2+offset

    x6 = l_wg
    y6 = -w_wg/2+offset

    x7 = l_wg
    y7 = w_wg/2+offset

    x8 = -l_wg_margin
    y8 = w_wg/2+offset
    
    # construct matrix for verticies
    vtx = np.array([[x1,y1,zb], #Vertex 1
                    [x2,y2,zb], #Vertex 2
                    [x3,y3,zb], #Vertex 3
                    [x4,y4,zb], #Vertex 4
                    [x5,y5,zt], #Vertex 5
                    [x6,y6,zt], #Vertex 6
                    [x7,y7,zt], #Vertex 7
                    [x8,y8,zt]]) #Vertex 8

    #construct matrix which groups verticies into facets.
    b = np.transpose(np.array([ [[1,2,6,5]], 
                                [[2,3,7,6]], 
                                [[3,4,8,7]], 
                                [[4,1,5,8]], 
                                [[5,6,7,8]], 
                                [[1,2,3,4]]]))
    
    # Draw tha darn thing
    MODE.switchtolayout()
    MODE.method_type = 2
    MODE.addplanarsolid()
    MODE.set('vertices',vtx)
    MODE.set('facets',b)
    MODE.set("name","wg_in")
    MODE.set("material", material_thinfilm)
    MODE.set("alpha", 0.5)
    MODE.set("override mesh order from material database", 1)
    MODE.set("mesh order", 1)
    time.sleep(0.1)
    
def drawWGOut(l_wg, offset):
    #Bottom surface verticies
    x1 = 0
    y1 = -w_wg/2-trim-offset

    x2 = l_wg+l_wg_margin
    y2 = -w_wg/2-trim-offset

    x3 = l_wg+l_wg_margin
    y3 = w_wg/2+trim-offset

    x4 = 0
    y4 = w_wg/2+trim-offset

    #Top surface verticies
    x5 = 0
    y5 = -w_wg/2-offset

    x6 = l_wg+l_wg_margin
    y6 = -w_wg/2-offset

    x7 = l_wg+l_wg_margin
    y7 = w_wg/2-offset

    x8 = 0
    y8 = w_wg/2-offset

    
    # construct matrix for verticies
    vtx = np.array([[x1,y1,zb], #Vertex 1
                    [x2,y2,zb], #Vertex 2
                    [x3,y3,zb], #Vertex 3
                    [x4,y4,zb], #Vertex 4
                    [x5,y5,zt], #Vertex 5
                    [x6,y6,zt], #Vertex 6
                    [x7,y7,zt], #Vertex 7
                    [x8,y8,zt]]) #Vertex 8

    #construct matrix which groups verticies into facets.
    b = np.transpose(np.array([ [[1,2,6,5]], 
                                [[2,3,7,6]], 
                                [[3,4,8,7]], 
                                [[4,1,5,8]], 
                                [[5,6,7,8]], 
                                [[1,2,3,4]]]))
    
    # Draw tha darn thing
    MODE.switchtolayout()
    MODE.method_type = 2
    MODE.addplanarsolid()
    MODE.set('vertices',vtx)
    MODE.set('facets',b)
    MODE.set("name","wg_out")
    MODE.set("material", material_thinfilm)
    MODE.set("alpha", 0.5)
    MODE.set("override mesh order from material database", 1)
    MODE.set("mesh order", 1)
    time.sleep(0.1)
    
def drawSlab(l_wg, offset):
    #Draw the brick
    x1 = -l_wg_margin
    x2 = l_wg+l_wg_margin
    
    y1 = -slab_margin/2
    y4 = slab_margin/2 
    
    x4 = x1
    x5 = x1
    x8 = x1
    
    x3 = x2
    x6 = x2
    x7 = x2
    
    y2 = y1
    y5 = y1
    y6 = y1
    
    y3 = y4
    y7 = y4
    y8 = y4
    
    # construct matrix for verticies
    vtx = np.array([[x1,y1,0], #Vertex 1
                    [x2,y2,0], #Vertex 2
                    [x3,y3,0], #Vertex 3
                    [x4,y4,0], #Vertex 4
                    [x5,y5,zb], #Vertex 5
                    [x6,y6,zb], #Vertex 6
                    [x7,y7,zb], #Vertex 7
                    [x8,y8,zb]]) #Vertex 8

    #construct matrix which groups verticies into facets.
    b = np.transpose(np.array([ [[1,2,6,5]], 
                                [[2,3,7,6]], 
                                [[3,4,8,7]], 
                                [[4,1,5,8]], 
                                [[5,6,7,8]], 
                                [[1,2,3,4]]]))
    
    # Draw tha darn thing
    MODE.switchtolayout()
    MODE.method_type = 2
    MODE.addplanarsolid()
    MODE.set('vertices',vtx)
    MODE.set('facets',b)
    MODE.set("name","slab")
    MODE.set("material", material_thinfilm)
    MODE.set("alpha", 0.5)
    MODE.set("override mesh order from material database", 1)
    MODE.set("mesh order", 1)
    time.sleep(0.1)
    
def drawCladding(l_wg, offset, h_cladding):
    if(h_cladding != 0):
        #Draw the brick
        x1 = -l_wg_margin
        x2 = l_wg+l_wg_margin

        y1 = -slab_margin/2
        y4 = slab_margin/2 

        x4 = x1
        x5 = x1
        x8 = x1

        x3 = x2
        x6 = x2
        x7 = x2

        y2 = y1
        y5 = y1
        y6 = y1

        y3 = y4
        y7 = y4
        y8 = y4

        # construct matrix for verticies
        vtx = np.array([[x1,y1,zb], #Vertex 1
                        [x2,y2,zb], #Vertex 2
                        [x3,y3,zb], #Vertex 3
                        [x4,y4,zb], #Vertex 4
                        [x5,y5,zt+h_cladding], #Vertex 5
                        [x6,y6,zt+h_cladding], #Vertex 6
                        [x7,y7,zt+h_cladding], #Vertex 7
                        [x8,y8,zt+h_cladding]]) #Vertex 8

        #construct matrix which groups verticies into facets.
        b = np.transpose(np.array([ [[1,2,6,5]], 
                                    [[2,3,7,6]], 
                                    [[3,4,8,7]], 
                                    [[4,1,5,8]], 
                                    [[5,6,7,8]], 
                                    [[1,2,3,4]]]))

        # Draw tha darn thing
        MODE.switchtolayout()
        MODE.method_type = 2
        MODE.addplanarsolid()
        MODE.set('vertices',vtx)
        MODE.set('facets',b)
        MODE.set("name","slab")
        MODE.set("material", material_cladding)
        MODE.set("alpha", 0.5)
        MODE.set("override mesh order from material database", 1)
        MODE.set("mesh order", 2)
        time.sleep(0.1)
        
def draw_conformal_cladding(material_cladding, h_LN, h_cladding, h_etch, w_slab, wg_length, w_ridge, x0=0):
    
    h_LN = float(h_LN)
    h_etch = float(h_etch)
    h_cladding = float(h_cladding)
    wg_length = float(wg_length)
    w_slab = float(w_slab)
    x0 = float(x0)
    
    #Calculate some extra geometric parameters
    h_slab = h_LN - h_etch
    Ymax = h_slab + h_cladding
    Zmin = -wg_length/2
    Zmax = wg_length/2
    
    w_cladding = w_ridge +2*h_cladding/np.sqrt(3)
    h_slab_clad = h_slab + h_cladding
    w_c_sidewall = h_etch/np.sqrt(3)
    
    #Draw cladding slab
    MODE.switchtolayout()
    MODE.addrect(override_mesh_order_from_material_database = True, mesh_order = 3)
    MODE.set("name","cladding_slab")
    MODE.set("material", material_cladding)
    MODE.set("x", x0)
    MODE.set("x span", w_slab)
    MODE.set("y min", h_slab)
    MODE.set("y max", Ymax)
    MODE.set("z min", Zmin)
    MODE.set("z max", Zmax)
    MODE.set("alpha", 0.5)
    
    #Main ridge
    MODE.switchtolayout()
    MODE.addrect(override_mesh_order_from_material_database = True, mesh_order = 3)
    MODE.set("name","cladding_ridge")
    MODE.set("material", material_cladding)
    MODE.set("x", x0)
    MODE.set("x span", w_cladding)
    MODE.set("y min", h_slab_clad)
    MODE.set("y max", h_LN + h_cladding)
    MODE.set("z min", Zmin)
    MODE.set("z max", Zmax)
    MODE.set("alpha", 0.5)
    
    #Draw left sidewall
    MODE.addtriangle(override_mesh_order_from_material_database = True, mesh_order = 3)
    MODE.set("name","cladding_left_sidewall")
    MODE.set("material", material_cladding)
    MODE.set("x", x0-w_cladding/2)
    MODE.set("y", h_slab_clad)
    MODE.set("z min", Zmin)
    MODE.set("z max", Zmax)
    V = np.array([[0, -w_c_sidewall, 0],[0, 0, h_etch]])
    MODE.set("vertices", V)
    MODE.set("alpha", 0.5)

    
    #Draw right sidewall
    MODE.addtriangle(override_mesh_order_from_material_database = True, mesh_order = 3)
    MODE.set("name","cladding_right_sidewall")
    MODE.set("material", material_cladding)
    MODE.set("x", x0+w_cladding/2)
    MODE.set("y", h_slab_clad)
    MODE.set("z min", Zmin)
    MODE.set("z max", Zmax)
    V = np.array([[0, w_c_sidewall, 0],[0, 0, h_etch]])
    MODE.set("vertices", V)
    MODE.set("alpha", 0.5)
    
def drawSubstrate(l_wg, offset):
    #Draw the brick
    x1 = -l_wg_margin
    x2 = l_wg+l_wg_margin
    
    y1 = -slab_margin/2
    y4 = slab_margin/2 
    
    x4 = x1
    x5 = x1
    x8 = x1
    
    x3 = x2
    x6 = x2
    x7 = x2
    
    y2 = y1
    y5 = y1
    y6 = y1
    
    y3 = y4
    y7 = y4
    y8 = y4
    
    # construct matrix for verticies
    vtx = np.array([[x1,y1,-h_substrate], #Vertex 1
                    [x2,y2,-h_substrate], #Vertex 2
                    [x3,y3,-h_substrate], #Vertex 3
                    [x4,y4,-h_substrate], #Vertex 4
                    [x5,y5,0], #Vertex 5
                    [x6,y6,0], #Vertex 6
                    [x7,y7,0], #Vertex 7
                    [x8,y8,0]]) #Vertex 8

    #construct matrix which groups verticies into facets.
    b = np.transpose(np.array([ [[1,2,6,5]], 
                                [[2,3,7,6]], 
                                [[3,4,8,7]], 
                                [[4,1,5,8]], 
                                [[5,6,7,8]], 
                                [[1,2,3,4]]]))
    
    # Draw tha darn thing
    MODE.switchtolayout()
    MODE.method_type = 2
    MODE.addplanarsolid()
    MODE.set('vertices',vtx)
    MODE.set('facets',b)
    MODE.set("name","substrate")
    MODE.set("material", material_substrate)
    MODE.set("alpha", 0.5)
    MODE.set("override mesh order from material database", 1)
    MODE.set("mesh order", 2)
    time.sleep(0.1)
    
def drawDC(l_wg, offset):
    MODE.switchtolayout()
    MODE.deleteall()
    MODE.addstructuregroup()
    MODE.set("name","DC")
    
    drawWGIn(l_wg, offset)
    MODE.addtogroup("DC")
    drawWGOut(l_wg, offset)
    MODE.addtogroup("DC")
    drawSlab(l_wg, offset)
    MODE.addtogroup("DC")
    drawSubstrate(l_wg, offset)
    MODE.addtogroup("DC")
    drawCladding(l_wg, offset, h_cladding)
    MODE.addtogroup("DC")
    
def drawWG(l_wg, offset):
    MODE.switchtolayout()
    MODE.deleteall()
    MODE.addstructuregroup()
    MODE.set("name","DC")
    drawWGMid(l_wg)
    MODE.addtogroup("DC")
    drawSlab(l_wg, offset)
    MODE.addtogroup("DC")
    drawSubstrate(l_wg, offset)
    MODE.addtogroup("DC")
    drawConformalCladding(l_wg, h_cladding)
    MODE.addtogroup("DC")
    
def drawDC_outer(l_wg, offset):
    MODE.switchtolayout()
    MODE.deleteall()
    MODE.addstructuregroup()
    MODE.set("name","DC")
    
    drawWGIn(l_wg, offset)
    MODE.addtogroup("DC")
    
    drawSlab(l_wg, offset)
    MODE.addtogroup("DC")
    drawSubstrate(l_wg, offset)
    MODE.addtogroup("DC")
    drawCladding(l_wg, offset, h_cladding)
    MODE.addtogroup("DC")
    
def drawDC_inner(l_wg, offset):
    MODE.switchtolayout()
    MODE.deleteall()
    MODE.addstructuregroup()
    MODE.set("name","DC")
    
    drawWGOut(l_wg, offset)
    MODE.addtogroup("DC")
    
    drawSlab(l_wg, offset)
    MODE.addtogroup("DC")
    drawSubstrate(l_wg, offset)
    MODE.addtogroup("DC")
    drawCladding(l_wg, offset, h_cladding)
    MODE.addtogroup("DC")   
    
def define_2D_FDE(width, mesh):
    l_wg = l_wg_margin
    h = h_LN + mesh_margin # Need to add substrate and cladding

    MODE.addfde()  
    MODE.set("solver type", "2D X normal")
    
    # set dimension
    MODE.set("x",l_wg_margin/2)
    MODE.set("y",0)
    MODE.set("y span", width)
    MODE.set("z",zb) #need to fix this once substrate is added
    MODE.set("z span",h) #need to fix this once cladding is added
    
    MODE.set("solver type","2D X normal") 
    MODE.set("define y mesh by","maximum mesh step")
    MODE.set("dy", mesh)
    MODE.set("define z mesh by","maximum mesh step")
    MODE.set("dz", mesh)
    
    MODE.set("y min bc", "PML")
    MODE.set("z min bc", "PML")
    MODE.set("y max bc", "PML")
    MODE.set("z max bc", "PML")
    MODE.set("mesh refinement", "conformal variant 0")
    
def addFineMesh2D(width, mesh):
    # add mesh
    MODE.switchtolayout()
    MODE.addmesh()
    MODE.set("override x mesh", 0)
    MODE.set("override y mesh", 1)
    MODE.set("dy", mesh)
    
    MODE.set("directly defined", 1)
    MODE.set("x",l_wg_margin/2)
    MODE.set("x span",l_wg_margin)
    MODE.set("y",0)
    MODE.set("y span", width)
    MODE.set("z min",-100e-9) #need to fix this once substrate is added
    MODE.set("z max", zt+100e-9) #need to fix this once cladding is added
    MODE.set("name", "Coupler Mesh")
    
def addWGMesh2D(width, mesh):
    mesh_margin = 1e-6
    h = h_LN + mesh_margin # Need to add substrate and cladding
    
    # add mesh
    MODE.switchtolayout()
    MODE.addmesh()
    MODE.set("override x mesh", 0)
    MODE.set("override y mesh", 1)
    MODE.set("override z mesh", 1)
    MODE.set("dz", mesh)
    MODE.set("dy", mesh)
    MODE.set("directly defined", 1)
    
    MODE.set("x",l_wg_margin/2)
    MODE.set("x span",l_wg_margin)
    MODE.set("y",0)
    MODE.set("y span", width)
    MODE.set("z min",-100e-9) #need to fix this once substrate is added
    MODE.set("z max", zt+100e-9) #need to fix this once cladding is added
    MODE.set("name", "WG Mesh")
    
def setupFDE(width_fde = 15e-6, size_fde_mesh = 100e-9, width_med = 5e-6, size_med_mesh = 10e-9, width_fine = 2.5e-6, size_fine_mesh = 2e-9):
    addWGMesh2D(width_med, size_med_mesh)
    addFineMesh2D(width_fine, size_fine_mesh)
    define_2D_FDE(width_fde, size_fde_mesh)
    
def plotFieldFull(xx,yy,intensity,yes):
    if yes:
        xx = xx*1e6 
        yy = yy*1e6 
        x, y = np.meshgrid(xx,yy)
        plt.rcParams["figure.figsize"] = (12,6) 
        plt.subplot() 
        plt.pcolormesh(x,y, intensity, cmap='jet') 
        plt.axis([x.min(), x.max(), y.min(), y.max()]) 
        plt.xlabel('Coupling Length [um]')
        plt.ylabel('Coupler Transverse Position [um]')
        plt.colorbar()  
        plt.show()
    return

def run():
    MODE.run()

def updateMaterial(c, T):
    MODE.switchtolayout()
    # T calculate the coefficients
    f = (T-24.5)*(T+570.82)

    #Determine coefficients for extraordinary and ordinary axesa

    ea1=5.7560E+00
    ea2=9.8300E-02
    ea3=2.0200E-01
    ea4=1.8932E+02
    ea5=1.2520E+01
    ea6=1.3200E-02
    eb1=2.8600E-06
    eb2=4.7000E-08
    eb3=6.1130E-08
    eb4=1.5160E-04

    e1 = ea1+eb1*f
    e2 = ea2+eb2*f 
    e3 = (ea3+eb3*f)**2
    e4 = ea4+eb4*f 
    e5 = ea5**2 
    e6 = ea6

    oa1=5.6530E+00
    oa2=1.1850E-01
    oa3=2.0910E-01
    oa4=8.9610E+01
    oa5=1.0850E+01
    oa6=1.9700E-02
    ob1=7.9410E-07
    ob2=3.1340E-08
    ob3=-4.6410E-09
    ob4=-2.1880E-06

    o1 = oa1+ob1*f
    o2 = oa2+ob2*f 
    o3 = (oa3+ob3*f)**2
    o4 = oa4+ob4*f 
    o5 = oa5**2 
    o6 = oa6

    estr = "sqrt("+str(e1)+" + "+str(e2)+"/(l0^2-"+str(e3)+") + "+str(e4)+"/(l0^2-"+str(e5)+") - "+str(e6)+"*l0^2)"
    ostr = "sqrt("+str(o1)+" + "+str(o2)+"/(l0^2-"+str(o3)+") + "+str(o4)+"/(l0^2-"+str(o5)+") - "+str(o6)+"*l0^2)"  
    
    if c == 'x':
        MODE.setmaterial("LN_Scripted", "Real", estr+";"+ostr+";"+ostr)
    elif c == 'y':
        MODE.setmaterial("LN_Scripted", "Real", ostr+";"+estr+";"+ostr)
    elif c == 'z':
        MODE.setmaterial("LN_Scripted", "Real", ostr+";"+ostr+";"+estr)
    else:
        print('Invalid axes selection: use x, y or z.')
    
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def solve_bent_modes(radius,nmodes=20, bent = True, sort_idx = 1, reverse = True):
    MODE.set("wavelength", wl)
    MODE.set("number of trial modes", nmodes)
    if bent == True:
        MODE.set("bent waveguide",1)
        MODE.set("bend radius",radius)
    n = int(MODE.findmodes())
    
    neff = np.zeros(n) #effective  index matrix
    ng = np.zeros(n) #group  index matrix
    loss = np.zeros(n) #group  index matrix
    TE = np.zeros(n) #TE polarization fraction
    aeff = np.zeros(n) # Effective area of mode
    
    for k in range(n):    
        neff[k] = float(np.real(MODE.getdata("FDE::data::mode"+str(k+1), "neff")))
        ng[k] = float(np.real(MODE.getdata('FDE::data::mode'+str(k+1), 'ng')))
        loss[k] = float(np.real(MODE.getdata('FDE::data::mode'+str(k+1), 'loss')))
        TE[k] = float(MODE.getdata("FDE::data::mode"+str(k+1), "TE polarization fraction"))
        aeff[k] = float(MODE.getdata("FDE::data::mode"+str(k+1), "mode effective area"))
        #print(MODE.getdata("FDE::data::mode"+str(k+1)))
        
    index = MODE.getdata("FDE::data::material", "index_y")
    
    modes = [0] * n
    for km in range(neff.size): #Look for first TE mode
        M = lum.modes()
        M.get_from_lumerical(MODE, km+1)
        modes[km] = M
        modes[km] = np.append(modes[km],TE[km])
        modes[km] = np.append(modes[km],neff[km])
        modes[km] = np.append(modes[km],loss[km])
        modes[km] = np.append(modes[km],aeff[km])
        modes[km] = np.append(modes[km],km+1)
    
    print(km+1)
    #Sort modes
    modes = sorted(modes,key=lambda x: x[sort_idx], reverse = reverse)
    return modes,index

def solve_bent_modes_at_n(radius, n1, nmodes=20, bent = True):
    MODE.set("wavelength", wl)
    MODE.set("number of trial modes", nmodes)
    MODE.set("use max index", 0)
    MODE.set("n",n1)
    
    if bent == True:
        MODE.set("bent waveguide",1)
        MODE.set("bend radius",radius)
    n = int(MODE.findmodes())
    
    neff = np.zeros(n) #effective  index matrix
    ng = np.zeros(n) #group  index matrix
    loss = np.zeros(n) #group  index matrix
    TE = np.zeros(n) #TE polarization fraction
    aeff = np.zeros(n) # Effective area of mode
    
    for k in range(n):    
        neff[k] = float(np.real(MODE.getdata("FDE::data::mode"+str(k+1), "neff")))
        ng[k] = float(np.real(MODE.getdata('FDE::data::mode'+str(k+1), 'ng')))
        loss[k] = float(np.real(MODE.getdata('FDE::data::mode'+str(k+1), 'loss')))
        TE[k] = float(MODE.getdata("FDE::data::mode"+str(k+1), "TE polarization fraction"))
        aeff[k] = float(MODE.getdata("FDE::data::mode"+str(k+1), "mode effective area"))
        #print(MODE.getdata("FDE::data::mode"+str(k+1)))
        
    index = MODE.getdata("FDE::data::material", "index_y")
    
    modes = [0] * n
    for km in range(neff.size): #Look for first TE mode
        M = lum.modes()
        M.get_from_lumerical(MODE, km+1)
        modes[km] = M
        modes[km] = np.append(modes[km],TE[km])
        modes[km] = np.append(modes[km],neff[km])
        modes[km] = np.append(modes[km],loss[km])
        modes[km] = np.append(modes[km],aeff[km])
    
    #Sort all the modes in order of TE fraction (highest in 0)
    modes = sorted(modes,key=lambda x: x[1], reverse = True)
    return modes,index

def solve_bent_modes_near(radius, n1, n2, nmodes=20, bent = True, sort_idx = 1):
    MODE.set("wavelength", wl)
    MODE.set("number of trial modes", nmodes)
    MODE.set("search", "in range")
    MODE.set("n1",n1)
    MODE.set("n2",n2)
    
    if bent == True:
        MODE.set("bent waveguide",1)
        MODE.set("bend radius",radius)
    n = int(MODE.findmodes())
    
    neff = np.zeros(n) #effective  index matrix
    ng = np.zeros(n) #group  index matrix
    loss = np.zeros(n) #group  index matrix
    TE = np.zeros(n) #TE polarization fraction
    aeff = np.zeros(n) # Effective area of mode
    
    for k in range(n):    
        neff[k] = float(np.real(MODE.getdata("FDE::data::mode"+str(k+1), "neff")))
        ng[k] = float(np.real(MODE.getdata('FDE::data::mode'+str(k+1), 'ng')))
        loss[k] = float(np.real(MODE.getdata('FDE::data::mode'+str(k+1), 'loss')))
        TE[k] = float(MODE.getdata("FDE::data::mode"+str(k+1), "TE polarization fraction"))
        aeff[k] = float(MODE.getdata("FDE::data::mode"+str(k+1), "mode effective area"))
        #print(MODE.getdata("FDE::data::mode"+str(k+1)))
        
    index = MODE.getdata("FDE::data::material", "index_y")
    
    modes = [0] * n
    for km in range(neff.size): #Look for first TE mode
        M = lum.modes()
        M.get_from_lumerical(MODE, km+1)
        modes[km] = M
        modes[km] = np.append(modes[km],TE[km])
        modes[km] = np.append(modes[km],neff[km])
        modes[km] = np.append(modes[km],loss[km])
        modes[km] = np.append(modes[km],aeff[km])
    
    #Sort all the modes in order of TE fraction (highest in 0)
    modes = sorted(modes,key=lambda x: x[sort_idx], reverse = True)
    return modes,index

def dispersion_analysis(wavelength, mode_number):
    MODE.selectmode(mode_number+1)
    MODE.setanalysis("track selected mode",1)
    MODE.setanalysis("stop wavelength", wavelength)
    MODE.setanalysis("detailed dispersion calculation",1)
    MODE.setanalysis("number of points", 1)
    MODE.setanalysis("number of test modes", 20)
    MODE.frequencysweep()
    vg = MODE.getdata("frequencysweep","vg")
    D = MODE.getdata("frequencysweep","D")
    GVD = -D*(wavelength)**2/(2*pi*c)
    return vg, GVD

def neff_analysis(wl_max,modenum):
    MODE.selectmode(modenum)
    MODE.setanalysis("track selected mode",1)
    MODE.setanalysis("stop wavelength", wl_max)
    MODE.setanalysis("number of points", 10)
    MODE.setanalysis("number of test modes", 20)
    MODE.frequencysweep()
    neff = np.real(MODE.getdata("frequencysweep","neff"))
    return neff

def wg_modes(radius, nmodes=20, bent = True):
    MODE.set("wavelength", wl)
    MODE.set("number of trial modes", nmodes)
    if bent == True:
        MODE.set("bent waveguide",1)
        MODE.set("bend radius",radius)
    n = int(MODE.findmodes())
    
    neff = np.zeros(n) #effective  index matrix
    ng = np.zeros(n) #group  index matrix
    loss = np.zeros(n) #group  index matrix
    TE = np.zeros(n) #TE polarization fraction
    aeff = np.zeros(n) # Effective area of mode
    vg = np.zeros(n) # group velocity
    GVD = np.zeros(n) # group velocity dispersion
    
    for k in range(n):    
        neff[k] = float(np.real(MODE.getdata("FDE::data::mode"+str(k+1), "neff")))
        ng[k] = float(np.real(MODE.getdata('FDE::data::mode'+str(k+1), 'ng')))
        loss[k] = float(np.real(MODE.getdata('FDE::data::mode'+str(k+1), 'loss')))
        TE[k] = float(MODE.getdata("FDE::data::mode"+str(k+1), "TE polarization fraction"))
        aeff[k] = float(MODE.getdata("FDE::data::mode"+str(k+1), "mode effective area"))
        vg[k], GVD[k] = dispersion_analysis(wl,k)
    
    index = MODE.getdata("FDE::data::material", "index_y")
    
    modes = [0] * n
    for km in range(neff.size): #Look for first TE mode
        M = lum.modes()
        M.get_from_lumerical(MODE, km+1)
        modes[km] = M
        modes[km] = np.append(modes[km],TE[km])
        modes[km] = np.append(modes[km],neff[km])
        modes[km] = np.append(modes[km],loss[km])
        modes[km] = np.append(modes[km],aeff[km])
        modes[km] = np.append(modes[km],vg[km])
        modes[km] = np.append(modes[km],GVD[km])
        
    #Sort all the modes in order of TE fraction (highest in 0)
    modes = sorted(modes,key=lambda x: x[1], reverse = True)
    return modes,index

def wg_TEmodes(radius, nmodes=20, bent = True):
    MODE.set("wavelength", wl)
    MODE.set("number of trial modes", nmodes)
    if bent == True:
        MODE.set("bent waveguide",1)
        MODE.set("bend radius",radius)
    n = int(MODE.findmodes())
    
    neff = np.zeros(n) #effective  index matrix
    ng = np.zeros(n) #group  index matrix
    loss = np.zeros(n) #group  index matrix
    TE = np.zeros(n) #TE polarization fraction
    aeff = np.zeros(n) # Effective area of mode
    vg = np.zeros(n) # group velocity
    GVD = np.zeros(n) # group velocity dispersion
    
    for k in range(n):    
        neff[k] = float(np.real(MODE.getdata("FDE::data::mode"+str(k+1), "neff")))
        ng[k] = float(np.real(MODE.getdata('FDE::data::mode'+str(k+1), 'ng')))
        loss[k] = float(np.real(MODE.getdata('FDE::data::mode'+str(k+1), 'loss')))
        TE[k] = float(MODE.getdata("FDE::data::mode"+str(k+1), "TE polarization fraction"))
        aeff[k] = float(MODE.getdata("FDE::data::mode"+str(k+1), "mode effective area"))
#         vg[k], GVD[k] = dispersion_analysis(wl,k)
    
    index = MODE.getdata("FDE::data::material", "index_y")
    
    TEmin = 0.95
    count = len([i for i in TE if i > TEmin])
    if count == 0:
        print("No TE modes with TEPF higher than " +str(TEmin))
        return
    modes = [0] * count
    for km in range(neff.size): #Look for first TE mode
        if TE[km]>90:
            M = lum.modes()
            M.get_from_lumerical(MODE, km+1)
            modes[km] = M
            modes[km] = np.append(modes[km],TE[km])
            modes[km] = np.append(modes[km],neff[km])
            modes[km] = np.append(modes[km],loss[km])
            modes[km] = np.append(modes[km],aeff[km])
            vg[k], GVD[k] = dispersion_analysis(wl,k)
            modes[km] = np.append(modes[km],vg[km])
            modes[km] = np.append(modes[km],GVD[km])
        
    #Sort all the modes in order of TE fraction (highest in 0)
    if count>1:
        modes = sorted(modes,key=lambda x: x[1], reverse = True)
        
    return modes,index






















