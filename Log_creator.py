import os
import scipy as sp
import pandas as pd
from astropy.io import fits

class log_creator(object):
    def __init__(self, paths, std_name_file):
        '''Initializes the class with the names of images in the
        paths given as input that matches the standard name for
        the images wanted'''

        self_paths = []

        image_names = []

        for path in paths:
            for name in os.listdir(path):
                if (std_name_file in name) and (name[-4:]=='fits'):
                    image_names.append(name)
                    self_paths.append(path)
        image_names = sp.array(image_names)

        self.paths = sp.array(self_paths)
        self.image_names = sp.sort(image_names)

    def head_reader(self, keys='Default', check_science='Default'):
        '''Reads the header of each science image, and extract information of
        interest to save in the log file.
        It extracts by default certain information from ESO header's
        standard format, but can be given a customized set of keywords
        on header.
        It needs a keyword to know if it is a science image or not'''

        if keys=='Default' and check_science=='Default':
            keys = sp.array(['ARCFILE', 'INSTRUME', 'DATE-OBS', 'EXPTIME',
                            'HIERARCH ESO DPR CATG',
                            'HIERARCH ESO INS SLIT1 NAME',  # Slit name
                            'HIERARCH ESO INS FILT1 NAME',   # Filter name
                            'HIERARCH ESO INS GRIS1 NAME'])  # Grism name
            check_science = 'HIERARCH ESO DPR CATG'
        # Create array with rows for each image info
        images_info = []
        for ind,name in enumerate(self.image_names):
            image = fits.open(self.paths[ind] + '/' + name)[0]
            header = image.header
            image = 0
            # Check if it is a science images
            try:
                if header[check_science]=='SCIENCE':
                    # Sub array with each image info
                    image_info = []
                    image_info.append(name)
                    for key in keys:
                        image_info.append(header[key])
                    image_info = sp.array(image_info)

                    images_info.append(image_info)
                else:
                    continue
            except:
                continue
        images_info = sp.array(images_info)

        # Create dictionary from the previous array with the images information
        images_info_dict = {}
        for ind,key in enumerate(keys):
            images_info_dict[key] = images_info[:,ind]

        self.image_info = images_info_dict

    def log_save(self, path):
        '''Saves to path, the images information obtained from the
        header to an csv log file'''
        df = pd.DataFrame(data=self.image_info)

        # Create path if doesn't exist
        try:
            os.system("mkdir " + path)
        except:
            pass

        df.to_csv(path + '/log_images_names.csv')


### MAIN ###

paths = []
while True:
	inp = input('>>>Path/s to search for images?:') # raw_input en python 2.7
	if inp=="exit":
		break
	paths.append(inp)
paths = sp.array(paths)

path_2sav = input('>>>Path to save log file?:')

log = log_creator(paths, 'EFOSC')
log.head_reader()
log.log_save(path_2sav)

# Test path ../../../../SN2016aiy/PHOT/EFOSC_OPT/2016_07/2016_07_26_bien_pbienr
