'''

SFR code

Author : Nitya Mandyam

'''
import numpy as np
import pyfits
import math
import astropy as ap
from astropy.cosmology import WMAP7

def jansky(flux,kcorrect):
    '''Getting fluxes in Janskies from Nanomaggies:
    Inputs: Choose Petrosian/Sersic Nmgy and the relevant Kcorrection
    '''
    flux_in_Jy = flux*3631*(10.0**(-9.0))*(10**(kcorrect/(-2.5)))
    return flux_in_Jy


def jansky_err(flux,kcorrect):
    '''Inverse Variance in Fluxes: (Input Flux inverse variance in Nmgy^-2)
    '''
    Jy_err = (flux**(-0.5))*3631*(10.0**(-9.0))*(10**(kcorrect/(-2.5)))
    return Jy_err


def UVsfr(z,fmag,nmag,rmag,f_flux):
    ''' Calculate UV star formation rates. 
    Inputs: NSAID,z,F-band magnitude, N-band magnitude, r-band magnitude, F-band flux in Janskies
    '''
    fn = fmag - nmag
    opt = nmag - rmag   # N-r
    
    #Luminosity Distance
    dist = WMAP7.comoving_distance(z)
    ldist = (1+z)*dist
    
    #calculating Attenuation 'atten'
    atten = np.repeat(-999., len(fmag)) 

    case1 = np.where((opt > 4.) & (fn < 0.95))
    atten[case1] = 3.32*fn[case1] + 0.22
    case2 = np.where((opt > 4.) & (fn >= 0.95))
    atten[case2] = 3.37
    case3 = np.where((opt <= 4.) & (fn < 0.9))
    atten[case3] = 2.99*fn[case3] + 0.27
    case4 = np.where((opt <= 4.) & (fn >= 0.9))
    atten[case4] = 2.96

    #if opt >= 4.0:
    #    if fn < 0.95:
    #        atten = 3.32*fn + 0.22
    #    else:
    #        atten = 3.37
    #else:
    #    if fn < 0.90:
    #        atten = 2.99*fn +0.27
    #    else:
    #        atten = 2.96

    lum = 4.*np.pi*(ldist**2.0)*(3.087**2.0)*(10**(25.0 +(atten/2.5)))*f_flux  #Luminosity
    sfr = 1.08*(10**(-28.0))*np.abs(lum)
    return sfr


def DRP_UVsfr(nsa_data, flux_choice): 
    ''' Given NSA data dictionary calculate the UV sfrs 
    '''
    if flux_choice not in ['elpetro', 'sersic']: 
        raise ValueError

    fuv_nanomags = nsa_data[flux_choice+'_flux'][:,0]
    not_nans = (fuv_nanomags > 0.) 
    print len(fuv_nanomags) - np.sum(not_nans), " galaxies don't have UV"

    fuv_jansky = np.repeat(-999., len(fuv_nanomags))
    fuv_jansky[np.where(not_nans)] = jansky(fuv_nanomags[np.where(not_nans)], 0.) 

    absmags = nsa_data[flux_choice+'_absmag']
    f_notnans = (absmags[:,0] != -9999.)
    n_notnans = (absmags[:,1] != -9999.)
    r_notnans = (absmags[:,4] != -9999.)
    
    has_everything = np.where(not_nans & f_notnans & n_notnans & r_notnans)
    uvsfrs = np.repeat(-999., len(fuv_nanomags))
    uvsfrs[has_everything] = UVsfr(
            nsa_data['z'][has_everything], 
            absmags[:,0][has_everything], 
            absmags[:,1][has_everything], 
            absmags[:,4][has_everything], 
            fuv_jansky[has_everything])

    return uvsfrs 


def DRP_Nr(nsa_data, flux_choice): 
    ''' Given NSA data dictionary calculate the UV sfrs 
    '''
    if flux_choice not in ['elpetro', 'sersic']: 
        raise ValueError
    
    absmags = nsa_data[flux_choice+'_absmag']
    f_notnans = (absmags[:,0] != -9999.)
    n_notnans = (absmags[:,1] != -9999.)
    r_notnans = (absmags[:,4] != -9999.)
    
    has_everything = np.where(f_notnans & n_notnans & r_notnans)
    Nr = np.repeat(-999., len(absmags)) 

    Nr[has_everything] = absmags[:,1][has_everything] - absmags[:,4][has_everything]
    return Nr 
