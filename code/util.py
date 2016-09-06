'''

All utility code for project 

'''
import os 


def Dir_dat():
    ''' Data directory symlink. This directory *should* be symlinked to a local directory 
    on a machine. No data, aside from the bare minimum, should be on the git repo.
    '''
    return os.path.dirname(os.path.realpath(__file__)).split('code')[0]+'dat/'


def Dir_code():
    ''' code directory. This is to avoid relative paths in general 
    '''
    return os.path.dirname(os.path.realpath(__file__))+'/'


def Dir_fig():
    ''' figure directory
    '''
    return os.path.dirname(os.path.realpath(__file__)).split('code')[0]+'fig/'

