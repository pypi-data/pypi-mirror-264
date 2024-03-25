# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 10:27:04 2024

@author: Andrea
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c,m_e,e,mu_0,epsilon_0
from scipy.integrate import solve_ivp
from rad_utils import rad_parall,rad_no_parall

class beam():
    """default: gaussian beam"""
    def __init__(self,sigx,sigy,sigz,aveg,sigdg,epsx,epsy,npart):
        self.sigx = sigx        # x rms size [m]
        self.sigy = sigy        # y rms size [m]
        self.sigz = sigz        # z rms size [m]
        self.aveg = aveg        # average Lorentz factor
        self.sigdg = sigdg      # rms relative energy spread dgamma/gamma
        self.epsx = epsx        # x normalized emittance [mm mrad]
        self.epsy = epsy        # y normalized emittance [mm mrad] 
        self.npart = npart      # number of beam particles
        
        self.mupos = np.array([0, 0, 0])                                    # gaussian position means

        """calculated variables"""
        # self.aveb = np.sqrt(1-1/aveg**2)                                    # average beta [v/c]
        self.sigg = aveg*sigdg                                              # rms energy spread dgamma
        self.epsxr = np.sqrt(epsx**2/aveg**2/(1 + self.sigg**2/aveg**2))    # x rms emittance [mm mrad]
        self.epsyr = np.sqrt(epsy**2/aveg**2/(1 + self.sigg**2/aveg**2))    # y rms emittance [mm mrad]
    
        """gammas and positions"""
        self.gamma = np.random.normal(aveg,self.sigg,(npart))
        sigp = np.array([sigx, sigy, sigz])
        self.pos0 = np.random.normal(self.mupos, sigp, (npart, 3))          # particle initial positions [m]
        
        """angles"""
        # calculated throug normalized emittance expression with gamma spread WITHOUT trace space correlation
        try:
            self.sigthx = epsx*1e-6/sigx/aveg/np.sqrt(self.sigg**2/aveg**2+1)
        except:
            self.sigthx = 0
        try:
            self.sigthy = epsy*1e-6/sigy/aveg/np.sqrt(self.sigg**2/aveg**2+1)
        except:
            self.sigthy = 0
        self.thx = np.random.normal(0, self.sigthx, (npart))
        self.thy = np.random.normal(0, self.sigthy, (npart))
        self.th = np.sqrt(self.thx**2 + self.thy**2)
        self.ph = np.arctan2(self.thy, self.thx)
        
        """normalized velocities"""
        beta = np.sqrt(1-1/self.gamma**2)
        bx0 = beta*np.sin(self.th)*np.cos(self.ph)
        by0 = beta*np.sin(self.th)*np.sin(self.ph)
        bz0 = beta*np.cos(self.th)
        self.bet0 = np.zeros_like(self.pos0)
        self.bet0[:,0] = bx0
        self.bet0[:,1] = by0
        self.bet0[:,2] = bz0
        
    def add_field(self,device,**kwargs):
        if device=="ABP":
            assert "r_c" in kwargs and "rho_c" in kwargs and "J" in kwargs and "lr" in kwargs
            self.field = self.ABP_field
            self.kw = kwargs
        if device=="undulator":
            assert "K" in kwargs and "l_U" in kwargs 
            self.field = self.undulator_field
            self.kw = kwargs
            # self.K = e*kwargs['B0']*kwargs['l_U']/2/np.pi/m_e/c         # undulator strength [T*m]
            self.K = kwargs['K']
            self.B0 = kwargs['K']*2*np.pi*m_e*c/e/kwargs['l_U']
            self.l_U = kwargs['l_U']
            self.l_1 = self.l_U/2/self.aveg**2*(1 + self.K**2/2)
        if device=="ion channel":
            assert "n_p" in kwargs and "K" in kwargs
            self.field = self.plasma_field
            self.kw = kwargs
            self.n_p = kwargs['n_p']
            self.omega_p = np.sqrt(self.n_p*e**2/m_e/epsilon_0)
            self.k_b = np.sqrt(self.n_p*e**2/2/epsilon_0/m_e/c**2/self.aveg)
            self.K = kwargs['K']
            self.r_off = self.K/self.aveg/self.k_b

        if device=="CBM":
            assert "B0" in kwargs
            self.field = self.CBM_field
            self.kw = kwargs
        if device=="drift":
            self.field = self.no_field

    def ABP_field(self,x,y,z):
        kwargs = self.kw
        r_c = kwargs["r_c"]                     # capillary section radius [m]
        rho_c = kwargs["rho_c"]                 # capillary bending radius [m]
        J = kwargs["J"]                         # current density [A/m^2]
        lr = kwargs["lr"]                       # left/right bending label

        B1 = mu_0*J/2                            # field slope [T/m]
        r = np.sqrt(x**2 + z**2)
        dr = r-rho_c
        drax = np.sqrt(dr**2 + y**2)              # distance from design trajectory [m]
        the = np.arctan2(y, dr)                 # azimuthal angle around capillary axis[rad]
        phi = np.arctan2(z, x)                  # angle around capillary bending axis[rad]
        cff = -1
        if lr == "l":
            cff = 1
        Bmod = B1*drax
        By = Bmod*np.cos(the)*cff 
        Br = Bmod*np.sin(the)*(-cff)
        Bx = Br*np.cos(phi)
        Bz = Br*np.sin(phi)
        Ex = np.zeros_like(x)
        Ey = np.zeros_like(x)
        Ez = np.zeros_like(x)
        # sigcurr = r_c/2                         # current spatial standard deviation (for gaussian density) [m]
        # d = 0.1*r_c
        # cut1 = 1/(1+np.exp((drax-r_c)/d))
        # cut2 = 1/(1+np.exp((drax-r_c)/d/0.001))
        # Brgauss = mu0*J/4/np.pi**2/sigcurr**2/dr*(1-np.exp(-drax**2/2/sigcurr**2))
        # return B0*drax*cut1     
        return Ex,Ey,Ez,Bx,By,Bz
    
    def undulator_field(self,x,y,z):
        kwargs = self.kw
        B0 = self.B0                            # undulator field amplitude [T]
        l_U = self.l_U                          # undulator wavelength [m]
        k_U = 2*np.pi/l_U                       # undulator wavevector [m^-1]
        Ex = np.zeros_like(x)
        Ey = np.zeros_like(x)
        Ez = np.zeros_like(x)
        Bx = np.zeros_like(x)
        By = B0*np.cos(k_U*z)
        Bz = np.zeros_like(x)
        return Ex,Ey,Ez,Bx,By,Bz
    
    def plasma_field(self,x,y,z):
        kwargs = self.kw
        r = np.sqrt((x - self.r_off)**2 + y**2)
        theta = np.arctan2(y,(x - self.r_off))
        Er = self.n_p*e*(r)/2/epsilon_0
        Ex = Er*np.cos(theta)
        Ey = Er*np.sin(theta)
        Ez = np.zeros_like(x)
        Bx = np.zeros_like(x)
        By = np.zeros_like(x)
        Bz = np.zeros_like(x)
        return Ex,Ey,Ez,Bx,By,Bz    

    def CBM_field(self,x,y,z):
        kwargs = self.kw
        B0 = kwargs["B0"]                       # undulator field amplitude [T]
        Ex = np.zeros_like(x)
        Ey = np.zeros_like(x)
        Ez = np.zeros_like(x)
        Bx = np.zeros_like(x)
        By = -B0*np.ones_like(x)
        Bz = np.zeros_like(x)
        return Ex,Ey,Ez,Bx,By,Bz
    
    def no_field(self,x,y,z):
        zero = np.zeros_like(x)
        return zero,zero,zero,zero,zero,zero

    def match(self):
        """overwrites original transverse rms sizes and matches the beam over given emittances"""

    def wtstd(self,values,weights):
        average = np.average(values, weights=weights)
        variance = np.average((values-average)**2, weights=weights)
        return (average, np.sqrt(variance))
    
    def IVP(self, t, y, npart):    
        U = y.reshape(npart, 6)    
        x = U[:, 0]
        y = U[:, 1]
        z = U[:, 2]
        bx = U[:, 3]
        by = U[:, 4]
        bz = U[:, 5]    
    
        Ex,Ey,Ez,Bx,By,Bz = self.field(x,y,z)
    
        g = 1/np.sqrt(1-(bx**2 + by**2 + bz**2))
        Fx = -e*(Ex + c*(by*Bz - bz*By))
        Fy = -e*(Ey + c*(bz*Bx - bx*Bz))
        Fz = -e*(Ez + c*(bx*By - by*Bx))
    
        bdF = bx*Fx + by*Fy + bz*Fz
    
        ax = 1/m_e/g * (Fx - bdF*bx)
        ay = 1/m_e/g * (Fy - bdF*by)
        az = 1/m_e/g * (Fz - bdF*bz)
    
        dxdt = bx*c
        dydt = by*c
        dzdt = bz*c
        dbxdt = ax/c
        dbydt = ay/c
        dbzdt = az/c
    
        out = np.stack([dxdt, dydt, dzdt, dbxdt, dbydt, dbzdt]).transpose().flatten()
    
        return out
    
    def run(self,ti,te,npt):
        self.teval = np.linspace(ti, te, npt, endpoint=False)

        """IVP"""
        x0 = self.pos0[:,0]
        y0 = self.pos0[:,1]
        z0 = self.pos0[:,2]
        bx0 = self.bet0[:,0]
        by0 = self.bet0[:,1]
        bz0 = self.bet0[:,2]
        u0 = np.stack((x0, y0, z0, bx0, by0, bz0)).transpose()
        u0 = u0.flatten()
        u = solve_ivp(self.IVP, 
                      [ti, te], 
                      u0, 
                      method='RK45',
                      t_eval=self.teval, 
                      max_step=te*1e-4, 
                      args=(self.npart,))
        x = u.y[slice(0, 0+6*self.npart, 6)].transpose()
        y = u.y[slice(1, 0+6*self.npart, 6)].transpose()
        z = u.y[slice(2, 0+6*self.npart, 6)].transpose()
        bx = u.y[slice(3, 0+6*self.npart, 6)].transpose()
        by = u.y[slice(4, 0+6*self.npart, 6)].transpose()
        bz = u.y[slice(5, 0+6*self.npart, 6)].transpose()
        sx = np.std(x,axis=1)
        sy = np.std(y,axis=1)
        sz = np.std(z,axis=1)
        mx = np.average(x,axis=1)
        my = np.average(y,axis=1)
        mz = np.average(z,axis=1)
        self.pos = np.zeros((npt,self.npart,3))
        self.pos[:,:,0] = x
        self.pos[:,:,1] = y
        self.pos[:,:,2] = z
        self.sigpos = np.zeros((npt,3))
        self.sigpos[:,0] = sx
        self.sigpos[:,1] = sy
        self.sigpos[:,2] = sz
        self.mupos = np.zeros((npt,3))
        self.mupos[:,0] = mx
        self.mupos[:,1] = my
        self.mupos[:,2] = mz
        self.bet = np.zeros((npt,self.npart,3))
        self.bet[:,:,0] = bx
        self.bet[:,:,1] = by
        self.bet[:,:,2] = bz
        self.gam = 1/np.sqrt(1-np.linalg.norm(self.bet,axis=2)**2)
        """fields felt during evolution"""
        fields = self.field(x,y,z)
        self.E_field = np.zeros((npt,self.npart,3))
        self.E_field[:,:,0] = fields[0]
        self.E_field[:,:,1] = fields[1]
        self.E_field[:,:,2] = fields[2]
        self.B_field = np.zeros((npt,self.npart,3))
        self.B_field[:,:,0] = fields[3]
        self.B_field[:,:,1] = fields[4]
        self.B_field[:,:,2] = fields[5]
        
    def SI_CGS(self):
        pos_CGS = self.pos*1e2
        E_CGS = self.E_field*1e-4/2.9979
        B_CGS = self.B_field*1e4
        return pos_CGS,E_CGS,B_CGS
    
    def radiation(self,detpos,freqs,parall):
        pos_CGS,E_CGS,B_CGS = self.SI_CGS()
        wt = 1
        t = self.teval
        detpos *= 100 #CGS
        ft_array = np.zeros((len(freqs),6))
        if parall==False:
            for i in range(self.npart):
                xint = pos_CGS[:,i,:]
                bint = self.bet[:,i,:]
                gint = self.gam[:,i]
                Eint = E_CGS[:,i,:]
                Bint = B_CGS[:,i,:]
                ft_array = rad_no_parall(xint,bint,gint,Eint,Bint,wt,detpos,freqs,t,ft_array)
                print(i)
            ft_out = ft_array[:,0:3] + 1j*ft_array[:,3:6]        
            Aampl = abs(np.linalg.norm(ft_out,axis=1))
            U = 2*Aampl**2                            #d^I/domedOme (jackson IIedition pg669)
        elif parall==True:
            xint = pos_CGS
            bint = self.bet
            gint = self.gam
            Eint = E_CGS
            Bint = B_CGS
            ft_out = rad_parall(xint,bint,gint,Eint,Bint,wt,detpos,freqs,t,ft_array)
            Aampl = abs(np.linalg.norm(ft_out,axis=1))
            U = 2*Aampl**2                            #d^I/domedOme (jackson IIedition pg669)
        return U
            
    def plot(self,var,c0,c1):
        plt.figure()
        if var=="pos":
            xp = self.pos[:,:,c0]
            yp = self.pos[:,:,c1]
        if var=="sigpos":
            xp = self.mupos[:,c0]
            yp = self.sigpos[:,c1]
        if var=="bet":
            xp = self.bet[:,:,c0]
            yp = self.bet[:,:,c1]
        plt.plot(xp,yp,alpha=0.5)
        plt.scatter(xp[0],yp[0])