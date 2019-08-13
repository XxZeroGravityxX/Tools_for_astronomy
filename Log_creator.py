import os
import scipy as sp
import pandas as pd
from astropy.io import fits

class log_creator(object):
    def __init__(self, path):
        '''Initializes the class with the names of all science images in the
        paths given as input'''
        image_names = []

        for path in paths:
            for name in os.listdir(path):
                if name[-4:]=='fits':
                    images.append(name)
        image_names = sp.array(image_names)

        self.image_names = sp.sort(image_names)

    def head_reader(self, keys='Default'):
        '''Reads the header of each image, and extract information of
        interest to save in the log file.
        It extracts by default certain information from ESO header's
        standard format, but can be given a customized set of keywords
        on header'''

        if keys=='Default':
            keys = sp.array(['OBJECT', 'INSTRUME', 'DATE-OBS', 'EXPTIME',
                            'HIERARCH ESO DPR TECH',
                            'HIERARCH ESO INST SLIT1 NAME',  # Slit name
                            'HIERARCH ESO INS FILT1 NAME',   # Filter name
                            'HIERARCH ESO INS GRIS1 NAME'])  # Grism name
        # Create array with rows for each image info
        images_info = []
        for name in self.image_names:
            image = fits.open(name)[0]
            header = image.header
            image = 0

            # Sub array with each image info
            image_info = []
            image_info.append(name)
            for key in keys:
                image_info.append(header[key])
            image_info = sp.array(image_info)

            images_info.append(image_info)
        images_info = sp.array(images_info)

        # Create dictionary from the previous array with the images information
        images_info_dict = {}
        for ind,key in enumerate(keys):
            images_info_dict[key] = images_info[:,ind]

        # Add names column
        images_info_dict['NAME'] = self.image_names

        self.image_info = images_info_dict

    def log_save(self, path):
        '''Saves to path, the images information obtained from the
        header to an csv log file'''
        df = pd.DataFrame(data=self.image_info)
        df.to_csv(path + '/' + 'log_images_names.csv')


### MAIN ###

paths = []
while True:
	inp = input('>>>Path/s to search for images?:') # raw_input en python 2.7
	if inp=="exit":
		break
	paths.append(inp)
paths = sp.array(paths)

path_2sav = input('>>>Path to save log file?:')

log = log_creator(paths)
log.head_reader()
log.log_save(path_2sav)
