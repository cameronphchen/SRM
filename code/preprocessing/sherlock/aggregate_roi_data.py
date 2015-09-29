#!/usr/bin/env python

import scipy.io
import os,sys
import numpy as np
sys.path.append('/jukebox/ramadge/pohsuan/PyMVPA-hyper/')
import mvpa2
from mvpa2.datasets.mri import fmri_dataset
from scipy.signal import butter, lfilter
import nibabel as nib
import random, copy

roi = 'pmc'
smooth = 6


template_path = '/jukebox/fastscratch/janice/sherlock_movie/'
#if smooth != 0 :
data_path = '/jukebox/fastscratch/pohsuan/sherlock_movie/smooth{}/'.format(smooth)
data_name = 'smooth_sherlock_movie_s{}.nii.gz'
output_path = '/jukebox/ramadge/pohsuan/pHA/data/raw/sherlock_pmc_smooth{}'.format(smooth)
#else:
#    data_path = '/jukebox/fastscratch/janice/sherlock_movie/nosmooth/'
#    data_name = 'nosmooth_sherlock_movie_s{}.nii.gz'
#    output_path = '/jukebox/ramadge/pohsuan/pHA/data/raw/sherlock_nosmooth_'+roi


mask_fname = os.path.join(template_path, 'PMC_3mm.nii')

subj_idx_all = range(1,18)
subj_idx_all.remove(5)

movie_all = np.empty((len(subj_idx_all),1), dtype=object)


mask = nib.load(mask_fname)
maskdata = mask.get_data()
(i,j,k) = np.where(maskdata>0)

for idx,subj_idx in enumerate(subj_idx_all):
    bold_fname = os.path.join(data_path, data_name.format(subj_idx))
    print bold_fname
    img = nib.load(bold_fname)
    imgdata = img.get_data()
    assert imgdata.shape[0:3] == maskdata.shape
    movie_all[idx,0] = imgdata[i,j,k]

#if not os.path.exists(output_path):
#    os.mkdir(output_path)
#scipy.io.savemat(output_path+   '/sherlock_'+roi+'.mat', {'movie_all': movie_all})


for rseed in range(5):
    random.seed(rseed)
    tmp = range(len(movie_all))
    random.shuffle(tmp)
    g1_idx = tmp[:len(tmp)/2]
    g2_idx = tmp[len(tmp)/2 :]
    g1_idx = np.sort(g1_idx)
    g2_idx = np.sort(g2_idx)    
    movie_g1 = movie_all[g1_idx]
    movie_g2 = movie_all[g2_idx]

    if not os.path.exists(output_path+'_rnd{}_g1/'.format(rseed)):
        os.mkdir(output_path+'_rnd{}_g1/'.format(rseed))
    if not os.path.exists(output_path+'_rnd{}_g2/'.format(rseed)):
        os.mkdir(output_path+'_rnd{}_g2/'.format(rseed))
    scipy.io.savemat(output_path+'_rnd{}_g1/'.format(rseed)+'sherlock_'+roi+'.mat', {'movie_all' : movie_g1})
    print output_path+'_rnd{}_g1/'.format(rseed)+'sherlock_'+roi+'.mat'
    scipy.io.savemat(output_path+'_rnd{}_g2/'.format(rseed)+'sherlock_'+roi+'.mat', {'movie_all' : movie_g2})
    print output_path+'_rnd{}_g2/'.format(rseed)+'sherlock_'+roi+'.mat'

