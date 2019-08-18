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
        for ind,key in enumerate(keys):
            images_info_dict[key] = images_info[:,ind]

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

log = log_creator(paths, 'EFOSC')
log.head_reader(specphot)
log.log_save(path_2sav)

# Test paths phot
'''
['../../../../SN2016aiy/PHOT/EFOSC_OPT/2016_07/2016_07_26_bien_pbienr',
'../../../../SN2016aiy/PHOT/EFOSC_OPT/2016_09/2016_09_08_bien_pbienr',
'../../../../SN2016aiy/PHOT/EFOSC_OPT/2016_09/2016_09_18_bien_pbienr',
'../../../../SN2016aiy/PHOT/EFOSC_OPT/2016_09/2016_09_19_bien_pbienr',
'../../../../SN2016aiy/PHOT/EFOSC_OPT/2017_01/2017_01_27_bien_pbienr',
'../../../../SN2016aiy/PHOT/EFOSC_OPT/2017_02/2017_02_06_bien_pbienr',
'../../../../SN2016aiy/PHOT/EFOSC_OPT/2018_01/2018_01_14_bien_pbienr']
'''
#Test path spec
'''
['../../../../SN2016aiy/SPEC/EFOSC_OPT/Espectros_reducidos_wo_wl_fix/2016_02',
'../../../../SN2016aiy/SPEC/EFOSC_OPT/Espectros_reducidos_wo_wl_fix/2016_03/2016_03_09_bien_sbienr',
'../../../../SN2016aiy/SPEC/EFOSC_OPT/Espectros_reducidos_wo_wl_fix/2016_04/2016_04_13_bien_sbienr',
'../../../../SN2016aiy/SPEC/EFOSC_OPT/Espectros_reducidos_wo_wl_fix/2016_07/2016_07_25_bien_sbienr',
'../../../../SN2016aiy/SPEC/EFOSC_OPT/Espectros_reducidos_wo_wl_fix/2016_07/2016_07_26_bien_sbienr',
'../../../../SN2016aiy/SPEC/EFOSC_OPT/Espectros_reducidos_wo_wl_fix/2016_09/2016_09_07_bien_sbienr']
'''
