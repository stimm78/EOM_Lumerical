# import lumerical as lum
import numpy as np
from numpy import genfromtxt
from numpy import abs
from scipy import signal as si
from scipy.integrate import simpson
from scipy.optimize import minimize
from scipy.constants import pi, c
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as patches
import imp
import time
import csv

def initializeDEVICE():
    global DEVICE
    lumapi = imp.load_source("lumapi", "C:\\Program Files\\Lumerical\\v232\\api\\python")
    DEVICE = lumapi.DEVICE("Template.ldev")
