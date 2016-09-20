'''

Test the SFR routines 

'''
import numpy as np
import matplotlib.pyplot as plt

# --- Local ---
import util as Ut
import data as Data
import sfr as SFR 
from ChangTools.plotting import prettyplot
from ChangTools.plotting import prettycolors


def DRP_SFRs(flux_choice): 
    ''' Calculate the SFRs for DRP in order to test the SFR 
    functions. 
    '''
    derp = Data.DRP() 
    derp.Read() 
    nsa_data = derp.nsa_data

    if flux_choice not in ['elpetro', 'sersic']: 
        raise ValueError

    fuv_nanomags = nsa_data[flux_choice+'_flux'][:,0]
    not_nans = (fuv_nanomags > 0.) 
    #print len(not_nans[0])
    #print fuv[not_nans]

    fuv_jansky = np.repeat(-999., len(fuv_nanomags))
    fuv_jansky[np.where(not_nans)] = SFR.jansky(fuv_nanomags[np.where(not_nans)], 0.) 

    absmags = nsa_data[flux_choice+'_absmag']
    f_notnans = (absmags[:,0] != -9999.)
    n_notnans = (absmags[:,1] != -9999.)
    r_notnans = (absmags[:,4] != -9999.)
    
    has_everything = np.where(not_nans & f_notnans & n_notnans & r_notnans)
    uvsfrs = np.repeat(-999., len(fuv_nanomags))
    uvsfrs[has_everything] = SFR.uvsfr(
            nsa_data['z'][has_everything], 
            absmags[:,0][has_everything], 
            absmags[:,1][has_everything], 
            absmags[:,4][has_everything], 
            fuv_jansky[has_everything])

    print uvsfrs[has_everything]
    return None


if __name__=="__main__":
    DRP_SFRs('elpetro')

