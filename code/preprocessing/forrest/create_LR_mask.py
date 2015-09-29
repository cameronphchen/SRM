
import scipy.io
import os,sys
import numpy as np
import mvpa2
from mvpa2.datasets.mri import fmri_dataset

template_path = '/jukebox/fastscratch/pohsuan/pHA/data/raw/forest/'+\
                'psydata.ovgu.de/forrest_gump/templates/grpbold7Tad/from_mni/'
roi = 'pt'
mask_fname = os.path.join(template_path, roi+'_mask.nii.gz')
nsubj = 20

data_tmp   = fmri_dataset(mask_fname,mask = mask_fname)
LR_mask = data_tmp.samples.T
for i in range(len(LR_mask)):
  if LR_mask[i,0] in [91]: #[241,243,245]:
    LR_mask[i,0] = 1 #Left Hemisphere, pt:2383 voxels, ac:overall 2108 voxels
  elif LR_mask[i,0] in [92]:  #[242,244,246]:
    LR_mask[i,0] = 2 #Right Hemisphere, pt:1879 voxels, ac:overall 2131 voxels
  else:
    sys.exit('incorrect LR_mask data')

forrest_LRmask_all = np.empty((nsubj,1), dtype=object)
for subj in range(nsubj):
    forrest_LRmask_all[subj,0] = LR_mask
scipy.io.savemat('/jukebox/ramadge/pohsuan/pHA/data/raw/forrest_'+roi+'/forrest_LRmask_all.mat', {'forrest_LRmask_all': forrest_LRmask_all})
