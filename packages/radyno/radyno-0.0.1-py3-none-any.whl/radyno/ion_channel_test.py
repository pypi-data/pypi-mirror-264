# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:25:44 2024

@author: Andrea
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c,m_e,e,mu_0,epsilon_0
from beam_utils import beam
from rad_utils import Hz_to_keV
plt.rcParams['figure.autolayout'] = True
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['font.size'] = 15
plt.rcParams['lines.linewidth'] = 3

if __name__ == '__main__':    
    np.random.seed(0)

    """constants and utils"""
    npn = np.newaxis
    
    """init beam"""
    bm = beam(sigx=1e-7,
              sigy=1e-7,
              sigz=1e-9,
              aveg=70,
              sigdg=0.0,
              epsx=0.000001,
              epsy=0.000001,
              npart=10)
    
    """add field"""
    bm.add_field("ion channel",
                  n_p=2e14*1e6,
                  K=0.01)
    
    """run BD simulation"""
    bm.run(ti=0,te=0.1*1/c,npt=1000)
    bm.plot("pos",2,0)
    
    """calculate variables for spectral evaluation"""
    aveg = np.average(bm.gam)                               # average beam Lorentz factor (should be approx aveg)     
    lb = 2*np.pi/bm.k_b
    if bm.K<1:
        o = 4*np.pi*aveg**2*c/lb/(1 + bm.K**2/2)
        lab = "first harmonic"
    else:
        o = 3*np.pi*bm.K*aveg**2*c/lb              
        lab = "critical frequency"
    f1 = o/2/np.pi                                             
    
    """run radiation calculation"""
    detpos = np.array([0,0,10])                                 # detector position [m]
    freqs = np.linspace(0.1*f1, 30*f1, 1000)                    # frequencies [s^-1]
    U_numerical = bm.radiation(detpos,freqs,parall=False)
    
    # """analytical radiation"""
    # oms = 2*np.pi*freqs                                         # angular frequencies [s^-1]
    # LU = np.average(bm.pos[-1,:,2])                             # undulator length [m] (final average beam position)
    # U_analytical = Ifunc2(oms,0,0,LU*1e2,bm.K,bm.l_U*1e2,aveg)
    
    """plot spectrum"""
    plt.figure()
    plt.plot(freqs,U_numerical,label="numerical")
    # if bm.npart>1:
    #     plt.plot(freqs,U_analytical*bm.npart,"--",label="analytical incoherent",alpha=0.5)
    #     plt.plot(freqs,U_analytical*bm.npart**2,"--",label="analytical coherent",alpha=0.5)
    # else:
    #     plt.plot(freqs,U_analytical,"--",label="analytical",alpha=0.5)
    plt.axvline(f1,linestyle="--",color="black",label=lab)
    plt.xlabel(r"$\nu\,[Hz]$")
    plt.ylabel(r"$\frac{d^2I}{d\Omega d\omega}\,[erg\,s]$")
    plt.legend()
    
    
    
    
    
    
