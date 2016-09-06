'''



'''
import numpy as np
import matplotlib.pyplot as plt

# --- Local ---
import util as Ut
import data as Data
from ChangTools.plotting import prettyplot
from ChangTools.plotting import prettycolors


def DRP_NSA(prop, prop_spec=None): 
    '''
    '''
    prettyplot()    # plotting pretty
    pretty_color = prettycolors() 
    fig_file = Ut.Dir_fig() 
    # import DRP object
    derp = Data.DRP() 
    derp.Read() 
    if prop == 'zdist':  # check out the z distribution of the DRP galaxies
        nsa_data = derp.nsa_data
        print np.float(np.sum(nsa_data['z'] == nsa_data['z'].min()))/np.float(len(nsa_data['z'])), \
                ' of the galaxies have z = ', nsa_data['z'].min()
        # calculate p(z)
        p_z, z_bins = np.histogram(nsa_data['z'], bins=15, range=[0., 0.15], normed=True) 
    
        fig = plt.figure() 
        sub = fig.add_subplot(111) 
        sub.plot(0.5*(z_bins[:-1] + z_bins[1:]), p_z, linewidth=3, c='k') 
        sub.text(0.1, 0.8*p_z.max(), r'$\mathtt{N_{gal} = '+str(np.sum(nsa_data['z'] > 0.))+'}$', fontsize=20) 
    
        # x-axis
        sub.set_xlim([0.0, 0.15]) 
        sub.set_xlabel(r'Redshift ($\mathtt{z}$)', fontsize=25) 
        # y-axis
        sub.set_ylabel(r'$\mathtt{p(z)}$', fontsize=25) 
    
        fig_file += 'NSA_zdist.png'
        fig.savefig(fig_file, bbox_inches='tight') 
        plt.close() 

    elif prop == 'mass_comparison': # compare M*_petro to M*_sersic for z > 0 galaxies
        derp.Preprocess() 
        nsa_data = derp.nsa_data

        fig = plt.figure() 
        sub = fig.add_subplot(111)
        
        sub.scatter(np.log10(nsa_data['elpetro_mass'][has_z]), np.log10(nsa_data['sersic_mass'][has_z]), s=10, c='k')

        # x-axis
        sub.set_xlim([8.0, 12.0]) 
        sub.set_xlabel(r'$\mathtt{M_{*}^{elpetro}}$', fontsize=25) 
        # y-axis
        sub.set_ylim([8.0, 12.0]) 
        sub.set_ylabel(r'$\mathtt{M_{*}^{sersic}}$', fontsize=25) 
        fig_file += 'NSA_mass_comparison.png'
        fig.savefig(fig_file, bbox_inches='tight') 

    elif prop == 'mass(z)': # M*(z) for z > 0 galaxies
        derp.Preprocess() 
        nsa_data = derp.nsa_data
            
        if prop_spec == 'petro': 
            mass = np.log10(nsa_data['elpetro_mass'])
        elif prop_spec == 'sersic': 
            mass = np.log10(nsa_data['sersic_mass'])
        else: 
            raise ValueError
        fig = plt.figure() 
        sub = fig.add_subplot(111)
        sub.scatter(nsa_data['z'], mass, c='k', s=10) 
        # x-axis
        sub.set_xlim([0.0, 0.15]) 
        sub.set_xlabel(r'Redshift $\mathtt{(z)}$', fontsize=25) 
        # y-axis
        sub.set_ylim([8.0, 12.0]) 
        sub.set_ylabel(r'$\mathtt{M_{*}^{'+prop_spec+'}}$', fontsize=25) 
        fig_file += 'NSA_'+prop_spec.upper()+'mass_of_z.png'
        fig.savefig(fig_file, bbox_inches='tight') 
    
    return None



if __name__=='__main__': 
    DRP_NSA('mass(z)', prop_spec='petro')
    DRP_NSA('mass(z)', prop_spec='sersic')
