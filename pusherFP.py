# numpy
import numpy as np
np.random.seed(19680801)
from numpy.random import default_rng
rng = default_rng()

# import functions
from scipy.special import kv, iv, erf
from scipy.integrate import quad
from numpy import log, log10, sin, cos, exp, sqrt, pi

# interpolate
from scipy import interpolate

# physical constants
from scipy.constants import speed_of_light, fine_structure, hbar, elementary_charge, electron_mass

# root finding
from scipy.optimize import fsolve
from scipy import optimize

# plotting
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# progress bar
from tqdm.notebook import tqdm
from tqdm import trange
from time import sleep
from tqdm import tqdm

# warnings
import warnings
warnings.simplefilter('ignore')

import pandas as pd

def arraycenter(x):
    """
    returns centered array for histograms
    """
    return [(x[i]+x[i+1])/2 for i in range(len(x)-1)]



"""
%-------------------------------------------------------------------------------
%  FP pusher
%-------------------------------------------------------------------------------
"""

def g25(chi):
    """Niel2018 equation 25"""
    res = 9*sqrt(3)/(8*pi) * quad(lambda v: 2*v**2 * kv(5/3,v)/(2+3*v*chi)**2 + 4*v* (3*v*chi)**2 *kv(2/3,v)/(2+3*v*chi)**4, 0, np.inf)[0]
    return res

def h41(chi):
    """Niel2018 equation 41"""
    res = 9*sqrt(3)/(4*pi) * quad(lambda v: 2*chi**3 * v**3 * kv(5/3,v)/(2+3*v*chi)**3 + 54* chi**5 * v**4 *kv(2/3,v)/(2+3*v*chi)**5, 0, np.inf)[0]
    return res

def S39(chi,Kalpha):
    """Niel2018 equation 39"""
    res = 2/3 * Kalpha * chi**2 * g25(chi); #fine_structure**2/taue
    return res

def R40(chi,gm,Kalpha):
    """Niel2018 equation 40"""
    res = 2/3 * Kalpha * gm * h41(chi);
    return res

def pushFP(chi0, Nsmpl, tdim, nbins, g0, s0):

    gmdist = g0 + s0*rng.standard_normal(Nsmpl)
    gmdist[gmdist<1]=1 # make sure no particle has a physically inconsistent gamma
    gmdist_dump1 = np.copy(gmdist) #[] dump1
    gmdist_dump2 = np.copy(gmdist) * 0 #[] dump2
    gmdist_dump3 = np.copy(gmdist) * 0 #[] dump3

    # reference chi0
    print("chi0 =",chi0)
    #chi0 = 1e-1; #[] {1e-3,1e-2,1e-1,1e0}
    
    if chi0==1e-3:
        tmax = 20
    elif chi0==1e-2:
        tmax = 20
    elif chi0==1e-1:
        tmax = 5
    elif chi0==1e0:
        tmax = 3
    else:
        tmax = 5
    #tmax = 5 #[1/omega_p] simulation duration {20,20,5,3}

    # reference omega_p
    omega_p = elementary_charge/electron_mass/1800 * 2.5e3 * (chi0/(1e-3))
    #print("omega_p =",omega_p)

    # dimensionless but physically relevant constant
    Kalpha = fine_structure * electron_mass * speed_of_light**2 / (hbar * omega_p)
    #print("Kalpha = alpha^2/tau_e/omega_p =",Kalpha)

    # simulation parameters
    dt = tmax/tdim #[1/omega_p]
    print("dt =", dt)

    # interpolation
    gmlst = np.linspace(1,2*g0+3*s0,300); #[]
    S_lst = np.array([S39(gm/1800*chi0,Kalpha) for gm in gmlst])
    S_intrp = interpolate.interp1d(gmlst, S_lst) #interp1d / CubicSpline
    R_lst = np.array([R40(gm/1800*chi0,gm,Kalpha) for gm in gmlst])
    R_intrp = interpolate.interp1d(gmlst, R_lst)
    """
    def S_intrp(x):
        if x > 2*g0+5*s0:
            return S_intrpi(2*g0+5*s0)
        else:
            return S_intrpi(x)
        
    def R_intrp(x):
        if x > 2*g0+5*s0:
            return R_intrpi(2*g0+5*s0)
        else:
            return R_intrpi(x)
    
    S_intrp = np.vectorize(S_intrp)
    R_intrp = np.vectorize(R_intrp)
    """
    
    # for each time step
    for t in tqdm(range(tdim)):

        # interpolate S and R
        S = S_intrp(gmdist);
        R = R_intrp(gmdist);

        # Gaussian random number
        dW = sqrt(dt) * np.random.randn(Nsmpl)

        # Niel2018 eq 42
        dgamma = -S * dt + sqrt(R) * dW

        gmdist = gmdist + dgamma

        gmdist[gmdist < 1] = 1
        gmdist[gmdist > 2*g0+3*s0] = g0+3*s0

        # save distribution
        if t == int(tdim/2):
            gmdist_dump2 = np.copy(gmdist)

    # save distribution
    gmdist_dump3 = np.copy(gmdist)

    # get histograms
    # dump 1
    gmdist_y,gmdist_x = np.histogram(gmdist_dump1,np.linspace(1,g0+4*s0,nbins))
    gmdist1_y, gmdist1_x = gmdist_y, np.array(arraycenter(gmdist_x))
    # dump 2
    gmdist_y,gmdist_x = np.histogram(gmdist_dump2,np.linspace(1,g0+4*s0,nbins))
    gmdist2_y, gmdist2_x = gmdist_y, np.array(arraycenter(gmdist_x))
    # dump 3
    gmdist_y,gmdist_x = np.histogram(gmdist_dump3,np.linspace(1,g0+4*s0,nbins))
    gmdist3_y, gmdist3_x = gmdist_y, np.array(arraycenter(gmdist_x))

    return gmdist1_y, gmdist1_x, gmdist2_y, gmdist2_x, gmdist3_y, gmdist3_x