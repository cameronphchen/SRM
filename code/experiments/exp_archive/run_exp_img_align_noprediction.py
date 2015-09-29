#!/usr/bin/env python

# this is the code that runs the whole type 1 experiment
# using image data to learn alignment parameter and conduct classification on 
# image data
#
# this code run a specific alignment algorithm (align_algo) for (niter) rounds
# with voxel selection algorithm selecting (nvoxel) amount of voxels
# and (nTR) TR of movie data for alignment 
# using both right and left VT data
#
# before running the experiment, please make sure to execute 
# data_preprocessing.m and  transform_matdata2pydata.py to transformt the 
# mat format data into python .npz
#
# align_algo = 'HA_img_align', 'pHA_EM_img_align', 'None'
# 
# example: run_exp.py (align_algo) (n_iter) (n_voxel) (n_TR)
#          run_exp.p  HA_img_align  100  1300  2201
#
# by Cameron Po-Hsuan Chen @ Princeton


import numpy as np, scipy, random, sys, math, os
import scipy.io
from scipy import stats
import random
from libsvm.svmutil import *
from scikits.learn.svm import NuSVC
from ha import HA
from ha_swaroop import HA_swaroop
from pha_em import pHA_EM
import sys
sys.path.append('/Users/ChimatChen/anaconda/python.app/Contents/lib/python2.7/site-packages/')


# load experiment parameters
para  = {'align_algo': sys.argv[1],\
         'niter'     : int(sys.argv[2]),\
         'nvoxel'    : int(sys.argv[3]),\
         'nTR'       : int(sys.argv[4]),\
         'nsubjs'    : 10,\
         'niter_unit': 1 }

print para

niter      = para['niter']
nvoxel     = para['nvoxel']
nTR        = para['nTR']
nsubjs     = para['nsubjs']
niter_unit = para['niter_unit']
align_algo = para['align_algo']

# load experiment options
# rondo options
options = {'input_path'  : '/jukebox/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/jukebox/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# load mkdg data after voxel selection by matdata_preprocess.m
mkdg_data_lh = scipy.io.loadmat(options['working_path']+'mkdg_data_lh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_rh = scipy.io.loadmat(options['working_path']+'mkdg_data_rh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_lh = mkdg_data_lh['mkdg_data_lh'] 
mkdg_data_rh = mkdg_data_rh['mkdg_data_rh']

# load label for testing data
label = scipy.io.loadmat(options['input_path']+'subjall_picall_label.mat')
label = label['label']

current_file_lh = options['working_path']+align_algo+'_lh_'+str(nvoxel)+'vx_current.npz'
current_file_rh = options['working_path']+align_algo+'_rh_'+str(nvoxel)+'vx_current.npz'
if os.path.exists(current_file_lh):
  os.remove(current_file_lh)
if os.path.exists(current_file_rh):
  os.remove(current_file_rh)  

# for niter/niter_unit round, each round the alignment algorithm will run niter_unit iterations
for i in range(para['niter']/para['niter_unit']):
  # alignment phase
  # fit the model to movie data with number of iterations
  if para['align_algo'] in ['HA_img_align_noprediction'] :
    new_niter_lh = HA(mkdg_data_lh, options, para, 'lh')
    new_niter_rh = HA(mkdg_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['pHA_EM_img_align_noprediction']:
    new_niter_lh = pHA_EM(mkdg_data_lh, options, para, 'lh')
    new_niter_rh = pHA_EM(mkdg_data_rh, options, para, 'rh')
  elif para['align_algo'] == 'None' :
    # without any alignment, set new_niter_lh and new_niter_rh=0, the corresponding transformation
    # matrices are identity matrices
    new_niter_lh = new_niter_rh = 0
  else :
    print 'alignment algo not recognize'



