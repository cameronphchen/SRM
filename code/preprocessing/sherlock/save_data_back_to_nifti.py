#!/usr/bin/env python

import scipy.io
import os,sys
import numpy as np
sys.path.append('/jukebox/ramadge/pohsuan/PyMVPA-hyper/')
import mvpa2
from mvpa2.datasets.mri import fmri_dataset
from mvpa2.datasets.mri import map2nifti
from scipy.signal import butter, lfilter
import nibabel as nib

roi = 'pmc'
smooth = True


template_path = '/jukebox/fastscratch/janice/sherlock_movie/'
if smooth:
    input_path = '/jukebox/fastscratch/pohsuan/pHA/data/working/sherlock_smooth_pmc_noLR/813vx/1976TR/'
    output_path = '/jukebox/ramadge/pohsuan/pHA/data/output/synthesized/sherlock_smooth_'+roi+'/'
else:
    input_path = '/jukebox/fastscratch/pohsuan/pHA/data/working/sherlock_nosmooth_pmc_noLR/813vx/1976TR/'
    output_path = '/jukebox/ramadge/pohsuan/pHA/data/output/synthesized/sherlock_nosmooth_'+roi+'/'

in_fname = 'mysseg_1st_winsize9/ha_syn/50feat/rand0/all/ha_syn__10.npz'

if not os.path.exists(output_path):
    os.makedirs(output_path)

mask_fname = os.path.join(template_path, 'PMC_3mm.nii')

subj_idx_all = range(1,18)
#subj_idx_all = range(1,2)
subj_idx_all.remove(5)
movie_all = np.empty((len(subj_idx_all),1), dtype=object)

# load mask
mask = nib.load(mask_fname)
maskdata = mask.get_data()
(i,j,k) = np.where(maskdata>0)

# load alignment results
ws = np.load(input_path+in_fname)
W = ws['R']
S = ws['G'].T

datadim = maskdata.shape +(S.shape[1],)

sele_feat = 0

for idx,subj_idx in enumerate(subj_idx_all):
    syn_data = np.zeros(datadim, dtype=np.float32)
    syn_data[i,j,k,:] = np.outer(W[:,sele_feat,idx],S[sele_feat,:])

    #data = np.ones((32, 32, 15, 100), dtype=np.int16)

    out_fname = 'sherlock_synthesized_s{}'.format(subj_idx) #os.path.join(output_path, data_name.format(subj_idx))
    img_out = nib.Nifti1Image(syn_data,None)#, np.eye(4))

    nib.save(img_out,  output_path+out_fname+'.nii.gz')
    print output_path+out_fname+'.nii.gz'
