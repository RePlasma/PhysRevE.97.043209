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
from matplotlib import cm

# progress bar
from tqdm.notebook import tqdm
from tqdm import trange
from time import sleep
from tqdm import tqdm

# pickle
import pickle

# warnings
import warnings
warnings.simplefilter('ignore')


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
    res = 2/3 * Kalpha * chi**2 * g25(chi);
    return res

def R40(chi,gm,Kalpha):
    """Niel2018 equation 40"""
    res = 2/3 * Kalpha * gm * h41(chi);
    return res
    

"""
# Niel2018: figure 1a
chilst=np.linspace(-5,1)
logg25lst = np.log10( np.array([g25(10**chi) for chi in chilst]) )
plt.plot(chilst,logg25lst)
plt.show()
"""