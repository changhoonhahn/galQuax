import numpy as np
import pyfits
import math
import astropy as ap
from astropy.cosmology import WMAP7


#Getting fluxes in Janskies from Nanomaggies:
# Inputs: Choose Petrosian/Sersic Nmgy and the relevant Kcorrection

def jansky(flux,kcorrect):
    flux_in_Jy = flux*3631*(10.0**(-9.0))*(10**(kcorrect/(-2.5)))
    return flux_in_Jy


#Inverse Variance in Fluxes: (Input Flux inverse variance in Nmgy^-2)
def jansky_err(flux,kcorrect):
    Jy_err = (flux**(-0.5))*3631*(10.0**(-9.0))*(10**(kcorrect/(-2.5)))
    return Jy_err



#Inputs: NSAID,z,F-band magnitude, N-band magnitude, r-band magnitude, F-band flux in Janskies

def uvsfr(id,z,fmag,nmag,rmag,f_flux):
    fn = fmag - nmag
    opt = nmag - rmag   # N-r
    
    #Luminosity Distance
    dist = WMAP7.comoving_distance(z)
    ldist = (1+z)*dist
    
    #calculating Attenuation 'a'
    if opt>=4.0:
        if fn < 0.95:
            a = 3.32*float(fn) + 0.22
        else:
            a = 3.37
    else:
        if fn < 0.90:
            a = 2.99*float(fn) +0.27
        else:
            a = 2.96

    lum = 4*3.14159*(ldist**2.0)*(3.087**2.0)*(10**(25.0 +(a/2.5)))*f_flux  #Luminosity
    sfr = 1.08*(10**(-28.0))*abs(lum)
    return sfr



