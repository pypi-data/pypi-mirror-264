# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:45:47 2024

@author: Andrea
"""
import numpy as np
from num_traj_rad import beam
from scipy.constants import c,m_e,e,mu_0
import matplotlib.pyplot as plt

def drift(z,s0,epsrms):
    bw = s0**2/epsrms
    return s0*np.sqrt(1 + (z/bw)**2)
    

"""beam parameters"""
sx = 1e-5
sy = 1e-5
sz = 0
gamma = 100
relspread = 0
epsx = 0.1
epsy = 0.1
npart = 10000

"""init beam"""
bm = beam(sigx=sx,
          sigy=sy,
          sigz=sz,
          aveg=gamma,
          sigdg=relspread,
          epsx=epsx,
          epsy=epsy,
          npart=npart)

"""add drift: no field"""
bm.add_field("drift",
             B0=1,
             l_U=0.03)

"""run simulation"""
bm.run(0,1/c,npt=1000)

"""plot rms size"""
bm.plot("sigpos",2,0)

"""plot analytical check"""
epsrms = bm.epsxr*1e-6
s0 = bm.sigpos[0,0]
z = bm.mupos[:,2]
s = drift(z, s0, epsrms)
plt.plot(z,s,"--")




