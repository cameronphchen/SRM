
import scipy.io
import os,sys
sys.path.append('/jukebox/ramadge/pohsuan/PyMVPA-hyper/')
import numpy as np
import mvpa2
from mvpa2.datasets.mri import fmri_dataset

template_path = '/jukebox/fastscratch/pohsuan/pHA/data/raw/studyforrest/templates/grpbold7Tp1/from_mni/'
roi = 'ac'
mask_fname = os.path.join(template_path, roi+'_mask.nii.gz')
nsubj = 20

data_tmp   = fmri_dataset(mask_fname, mask = mask_fname)
LR_mask = data_tmp.samples.T
for i in range(len(LR_mask)):
  if LR_mask[i,0] in [241,243,245]:
    LR_mask[i,0] = 1 #Left Hemisphere, pt:2383 voxels, ac:overall 2108 voxels
  elif LR_mask[i,0] in [242,244,246]:
    LR_mask[i,0] = 2 #Right Hemisphere, pt:1879 voxels, ac:overall 2131 voxels
  else:
    sys.exit('incorrect LR_mask data')

pandora_LRmask_all = np.empty((nsubj,1), dtype=object)
for subj in range(nsubj):
    pandora_LRmask_all[subj,0] = LR_mask
scipy.io.savemat('/jukebox/ramadge/pohsuan/pHA/data/raw/pandora_'+roi+'/pandora_LRmask_all.mat', {'pandora_LRmask_all': pandora_LRmask_all})
