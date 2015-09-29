#!/usr/bin/env python
import scipy.io
import os,sys
import numpy as np
import sys
sys.path.append('/jukebox/ramadge/pohsuan/PyMVPA-hyper/')
import mvpa2
from mvpa2.datasets.mri import fmri_dataset
from scipy.signal import butter, lfilter


roi = 'vt'

nsubj = 20
nrun  = 8
nTR_remove = 4

forrest_movie_all = np.empty((nsubj,1), dtype=object)

for i in range(nsubj):
  filename = '/jukebox/ramadge/pohsuan/pHA/data/raw/forrest_'+roi+'/forrest_movie_'+roi+str(i)+'.npz' 
  ws = np.load(filename)
  subj_data = ws['arr_0']
  forrest_movie_all[i,0] = subj_data[()]['subj_data']
scipy.io.savemat('/jukebox/ramadge/pohsuan/pHA/data/raw/forrest_'+roi+'/forrest_movie_'+roi+'_distributed.mat', {'forrest_movie_all': forrest_movie_all})



