import os
import scipy as sp
import pandas as pd
from astropy.io import fits

class log_creator(object):
    def __init__(self, paths, std_name_file='ALL'):
        '''Initializes the class with the names of images in the
        paths given as input that matches the standard name for
        the images wanted'''

        self_paths = []

        image_names = []

        if std_name_file=='ALL':
            for name in os.listdir(paths):
                image_names.append(name)
                self_paths.append(paths)
        else:
            for path in paths:
                for name in os.listdir(path):
                    if (name[0:2] in std_name_file) and (name[-4:]=='fits'):
                        image_names.append(name)
                        self_paths.append(path)

        self.paths = sp.array(self_paths)
        self.image_names = sp.array(image_names)

    def head_reader(self, obs_type, keys='Default', check_science='Default',
                    check_slit='Default'):
        '''Reads the header of each science image, and extract information of
        interest to save in the log file.
        It extracts by default certain information from ESO header's
        standard format, but can be given a customized set of keywords
        on header.
        It needs a keyword to know if it is a science image or not'''

        if (keys=='Default' and check_science=='Default' and
        check_slit=='Default'):
            keys = sp.array(['ARCFILE', 'INSTRUME', 'DATE-OBS', 'EXPTIME',
                            'HIERARCH ESO DPR CATG',
                            'HIERARCH ESO INS SLIT1 NAME',  # Slit name
                            'HIERARCH ESO INS FILT1 NAME',   # Filter name
                            'HIERARCH ESO INS GRIS1 NAME'])  # Grism name
            check_science = 'HIERARCH ESO DPR CATG'
            check_slit = 'HIERARCH ESO INS SLIT1 NAME'

        # Create array with rows for each image info
        images_info = []
        for ind,name in enumerate(self.image_names):
            image = fits.open(self.paths[ind] + '/' + name)[0]
            header = image.header
            image = 0
            # Check if it is a science images
            try:
                if obs_type=='phot':
                    if (header[check_science]=='SCIENCE' and
                    header[check_slit]=='Free'):
                        # Sub array with each image info
                        image_info = []
                        for key in keys:
                            image_info.append(header[key])
                        image_info = sp.array(image_info)

                        images_info.append(image_info)
                    else:
                        continue
                elif obs_type=='spec':
                    if (header[check_science]=='SCIENCE' and
                    header[check_slit]!='Free'):
                        # Sub array with each image info
                        image_info = []
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
        try:
            for ind,key in enumerate(keys):
                images_info_dict[key] = images_info[:,ind]
        except:
            print('Default keyword not found')

        self.image_info = images_info_dict

    def log_save(self, path, sort_by='ARCFILE'):
        '''Saves to path, the images information obtained from the
        header to an csv log file'''
        df = pd.DataFrame(data=self.image_info).sort_values(by='ARCFILE').reset_index(drop=True)

        # Create path if doesn't exist
        try:
            os.system("mkdir " + path)
        except:
            pass

        df.to_csv(path + '/log_images_names.csv')


### MAIN ###

### Get instrument from user

ins = input('>>>Instrument ([EFOSC]/LCOGT) ?:')

if ins=='':
    ins = 'EFOSC'

### Get paths of images from user

if ins=='EFOSC':
    main = input('>>>Root path to search for images?:')

    specphot = input('>>>Spectroscopy or photometry?:')

    paths = []
    while True:
        date = input('>>>Dates (yyyymmdd)?:') # raw_input en python 2.7
        if date=="exit":
            break
        if specphot=='phot':
            suf = "_bien_pbienr"
        else:
            suf = "_bien_sbienr"
        path = main + "/" + date[:4] + "_" + date[4:6] + "/" + date[:4] + "_" + date[4:6] +\
               "_" + date[6:] + suf

        paths.append(path)
    paths = sp.array(paths)

    path_2sav = input('>>>Path to save log file?:')

    log = log_creator(paths, std_name_file='EFOSC')
    log.head_reader(specphot)
    log.log_save(path_2sav)

elif ins=='LCOGT':
    main = input('>>>Root path to search for images?:')

    specphot = input('>>>Spectroscopy or photometry?:')

    paths = []
    while True:
        date = input('>>>Dates (yyyymmdd)?:') # raw_input en python 2.7
        if date=="exit":
            break
        path = main + "/" + date[:4] + "_" + date[4:6] + "/" + date[:4] + "_" + date[4:6] +\
               "_" + date[6:]

        paths.append(path)
    paths = sp.array(paths)

    path_2sav = input('>>>Path to save log file?:')

    log = log_creator(main, std_name_file='ALL')
    log.head_reader(specphot)
    log.log_save(path_2sav)
