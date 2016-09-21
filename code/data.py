'''

Code for pre-processing data and ultimately creating a galaxy sample

'''
import h5py
import numpy as np 


# --- local ---
import util as Ut
from ChangTools import fitstables as Fits

class DRP(object): 
    def __init__(self):
        ''' Class object that describes the DRP data set 

        '''
        self.fits_file = Ut.Dir_dat()+'drp/drpall-v2_0_1.fits'              # fits file
        self.hdf5_file = (self.fits_file).split('.fits')[0]+'.hdf5'     # hdf5 file 

        self.nsa_grp = None 
        self.manga_grp = None
    
    def Write(self): 
        ''' Write into hdf5 file 
        '''
        # Read in .fits file 
        drpall = Fits.mrdfits(self.fits_file)
        # write to hdf5 file 
        f = h5py.File(self.hdf5_file, 'w') 
        nsa_grp = f.create_group('nsa_data') 
        manga_grp = f.create_group('manga_data') 

        for key in drpall.__dict__.keys(): 
            if 'nsa' in key: 
                nsa_grp.create_dataset(key.split('nsa_')[-1], data=getattr(drpall, key)) 
            else: 
                manga_grp.create_dataset(key, data=getattr(drpall, key)) 
        f.close() 
        return None 
    
    def Read(self):  
        ''' Read in hdf5 file into data dictionaries. 
        '''
        f = h5py.File(self.hdf5_file, 'r') 
        nsa_grp = f['nsa_data'] 
        manga_grp = f['manga_data'] 

        self.nsa_data = {} 
        for key in nsa_grp.iterkeys(): 
            self.nsa_data[key] = nsa_grp[key].value
    
        self.manga_data = {}
        for key in manga_grp.iterkeys(): 
            self.manga_data[key] = manga_grp[key].value
            
        return None

    def Preprocess(self): 
        ''' Preprocess out the z < 0 galaxies from the sample
        '''
        if not self.nsa_data: 
            raise ValueError
        if not self.manga_data: 
            raise ValueError

        has_z = np.where(self.nsa_data['z'] > 0) 
        for key in self.nsa_data.keys(): 
            self.nsa_data[key] = self.nsa_data[key][has_z]
        for key in self.manga_data.keys(): 
            self.manga_data[key] = self.manga_data[key][has_z]
        return None 


class NSA(object): 
    def __init__(self): 
        ''' Class object that describes the NSA data set. 
        '''
        self.fits_file = Ut.Dir_dat()+'nsa/nsa_v1_0_1.fits' # fits file 
        self.hdf5_file = (self.fits_file).split('.fits')[0]+'.hdf5'     # hdf5 file 

        self.nsa_data = None 

    def Write(self): 
        ''' Write into hdf5 file 
        '''
        # Read in .fits file 
        drpall = Fits.mrdfits(self.fits_file)
        # write to hdf5 file 
        f = h5py.File(self.hdf5_file, 'w') 
        nsa_grp = f.create_group('nsa_data') 

        for key in drpall.__dict__.keys(): 
            nsa_grp.create_dataset(key, data=getattr(drpall, key)) 
        f.close() 
        return None 
    
    def Read(self):  
        ''' Read in hdf5 file into data dictionaries. 
        '''
        f = h5py.File(self.hdf5_file, 'r') 
        nsa_grp = f['nsa_data'] 

        self.nsa_data = {} 
        for key in nsa_grp.iterkeys(): 
            self.nsa_data[key] = nsa_grp[key].value
        return None
    
    def Preprocess(self): 
        ''' Preprocess out the z < 0 galaxies from the sample
        '''
        if not self.nsa_data: 
            raise ValueError
        has_z = np.where(self.nsa_data['z'] > 0) 
        for key in self.nsa_data.keys(): 
            self.nsa_data[key] = self.nsa_data[key][has_z]
        return None 
