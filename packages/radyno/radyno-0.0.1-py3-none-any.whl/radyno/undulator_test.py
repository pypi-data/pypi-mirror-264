# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 18:56:19 2024

@author: Andrea
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c,m_e,e,mu_0
from beam_utils import beam
from rad_utils import Ifunc2,Hz_to_keV
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
    c   = c         # [m/s]
    me  = m_e       # [kg]
    e   = e         # [C]
    mu0 = mu_0      # [N*A^-2]
    
    """init beam"""
    bm = beam(sigx=1e-7,
              sigy=1e-7,
              sigz=1e-9,
              aveg=20000,
              sigdg=0.0,
              epsx=0.000001,
              epsy=0.000001,
              npart=1)
    
    """add field"""
    bm.add_field("undulator",
                 l_U=0.01,
                 K=1)
                  
    
    """run BD simulation"""
    bm.run(ti=0,te=0.1*1/c,npt=1000)
    bm.plot("pos",2,0)
    # 
    """recalculate undulator strength 
    and calculate variables for spectral evaluation"""
    aveg = np.average(bm.gam)                                   # average beam Lorentz factor (should be approx aveg)
    l1 = bm.l_U/2/aveg**2*(1 + bm.K**2/2)                       # first harmonic wavelength [m]
    o1 = c*2*np.pi/l1                                           # first harmonic angular frequency [s^-1]
    f1 = o1/2/np.pi                                             # first harmonic frequency [s^-1]
    
    """run radiation calculation"""
    detpos = np.array([0.0001,0,10])                                 # detector position [m]
    freqs = np.linspace(0.1*f1, 5*f1, 1000)                    # frequencies [s^-1]
    U_numerical = bm.radiation(detpos,freqs,parall=False)
    
    """analytical radiation"""
    oms = 2*np.pi*freqs                                         # angular frequencies [s^-1]
    LU = np.average(bm.pos[-1,:,2])                             # undulator length [m] (final average beam position)
    U_analytical = Ifunc2(oms,0,0,LU*1e2,bm.K,bm.l_U*1e2,aveg)
    
    """plot spectrum"""
    plt.figure()
    plt.plot(Hz_to_keV(freqs),U_numerical,label="numerical")
    # if bm.npart>1:
    #     plt.plot(Hz_to_keV(freqs),U_analytical*bm.npart,"--",label="analytical incoherent",alpha=0.5)
    #     plt.plot(Hz_to_keV(freqs),U_analytical*bm.npart**2,"--",label="analytical coherent",alpha=0.5)
    # else:
    #     plt.plot(Hz_to_keV(freqs),U_analytical,"--",label="analytical",alpha=0.5)
    plt.axvline(Hz_to_keV(f1),linestyle="--",color="black",label="first harmonic")
    plt.xlabel(r"E [keV]")
    plt.ylabel(r"$\frac{d^2I}{d\Omega d\omega}\,[erg\,s]$")
    plt.legend()
    
    
    
    
    
    
