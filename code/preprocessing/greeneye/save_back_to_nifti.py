#!/usr/bin/env python

import scipy.io
import os,sys
import numpy as np
sys.path.append('/jukebox/ramadge/pohsuan/PyMVPA-hyper/')
import mvpa2
from mvpa2.datasets.mri import fmri_dataset
from mvpa2.datasets.mri import map2nifti
from scipy.signal import butter, lfilter

roi = 'pccprecun'

template_path = '/jukebox/ramadge/RAW_DATA/green_eye/masks/'
mask_fname = os.path.join(template_path, 'pccprecun.nii.gz')


start = [21, 20, 19, 20, 20, 16, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 19, 20, 20,
          20, 20, 20, 20, 19, 20, 20, 20, 20, 20, 20, 20, 20, 15, 20, 19, 20, 20, 20, 20]
end = [470, 469, 468, 469, 469, 465, 469, 469, 469, 469, 469, 469, 469, 469, 469, 469, 469, 468, 469, 469,
       469, 469, 469, 469, 468, 469, 469, 469, 469, 469, 469, 469, 469, 464, 469, 468, 469, 469, 469, 469]

group1 = range(1,15)+range(29,35)
group2 = range(15,29)+range(35,41)
group_all = group1+group2
gp11 = [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,15,16,17,18,19,20,21,22,23,24]
gp12 = [11,12,13,14,29,30,31,32,33,34,25,26,27,28,35,36,37,38,39,40]
gp21 = [11,12,13,14,29,30,31,32,33,34,15,16,17,18,19,20,21,22,23,24]
gp22 = [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,25,26,27,28,35,36,37,38,39,40]


gptest = range(1,2)
# modify this line to choose the data to output
output_gp_name = 'gptest'
output_gp = gptest


greeneye_movie_all = np.empty((len(output_gp),1), dtype=object)
for i,subj in enumerate(output_gp):

    datapath = '/jukebox/ramadge/RAW_DATA/green_eye/niftis/'
    # getting first run data
    bold_fname = os.path.join(datapath, 'subj{}_trans_filtered_func_data.nii'.format(subj))
    data_tmp = fmri_dataset(bold_fname,mask = mask_fname)
    nifti = map2nifti(data_tmp)    

    subj_data = data_tmp.samples.T
    subj_data = subj_data[:,start[subj-1]:end[subj-1]]
    greeneye_movie_all[i,0] = subj_data


