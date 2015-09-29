#!/usr/bin/env python

# this is the code that runs the whole type 2 (leave-one-out) experiment
# using movie data for learning alignment parameter and conduct classification
# on image viewing data
#
# this code run a specific alignment algorithm (align_algo) for (niter) rounds
# with voxel selection algorithm selecting (nvoxel) amount of voxels
# and (nTR) TR of movie data for alignment 
# using both right and left VT data
#
# before running the experiment, please make sure to execute 
# data_preprocessing.m and  transform_matdata2pydata.py to 
# transform the mat format data into python .npz
#
# align_algo = 'HA', 'HA_shuffle', 'pHA_EM', 'pHA_EM_shuffle', 'None'
# 
# example: run_exp_loo.py (align_algo) (n_iter) (n_voxel) (n_TR)
#          run_exp_loo.py  HA_img_align_loo0  100  1300  2201
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
         'nsubjs'    : 9,\
         'niter_unit': 1 }

print para

align_algo = para['align_algo']
niter      = para['niter']
nvoxel     = para['nvoxel']
nTR        = para['nTR']
loo        = align_algo[-1]
nsubjs     = para['nsubjs']
niter_unit = para['niter_unit']

print 'loo:'+loo
# load experiment options
# rondo options
options = {'input_path'  : '/jukebox/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/jukebox/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# local options
#options = {'input_path'  : '/Volumes/ramadge/pohsuan/pHA/data/input/', \
#           'working_path': '/Volumes/ramadge/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
#           'output_path' : '/Volumes/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# load movie data after voxel selection by matdata_preprocess.m 
#movie_data_lh = scipy.io.loadmat(options['working_path']+'movie_data_lh_'+str(para['nvoxel'])+'vx.mat')
#movie_data_rh = scipy.io.loadmat(options['working_path']+'movie_data_rh_'+str(para['nvoxel'])+'vx.mat')
#movie_data_lh = movie_data_lh['movie_data_lh'] 
#movie_data_rh = movie_data_rh['movie_data_rh'] 

# load mkdg data after voxel selection by matdata_preprocess.m
mkdg_data_lh = scipy.io.loadmat(options['working_path']+'mkdg_data_lh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_rh = scipy.io.loadmat(options['working_path']+'mkdg_data_rh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_lh = mkdg_data_lh['mkdg_data_lh'] 
mkdg_data_rh = mkdg_data_rh['mkdg_data_rh']

mkdg_data_lh_loo = np.delete(mkdg_data_lh, loo,2) 
mkdg_data_rh_loo = np.delete(mkdg_data_rh, loo,2)

# load label for testing data
label = scipy.io.loadmat(options['input_path']+'subjall_picall_label.mat')
label = label['label']
trn_label = label[0:504]
tst_label = label[504:560]
trn_label = np.squeeze(np.asarray(trn_label))
tst_label = np.squeeze(np.asarray(tst_label))

loo_idx = range(10)
loo_idx = np.delete(loo_idx, loo)

# for niter/niter_unit round, each round the alignment algorithm will run niter_unit iterations
for i in range(para['niter']/para['niter_unit']):
  
  # alignment phase
  # fit the model to movie data with number of iterations
  if align_algo[0:-1] in ['HA_img_align_loo'] :
    new_niter_lh = HA(mkdg_data_lh_loo, options, para, 'lh')
    new_niter_rh = HA(mkdg_data_rh_loo, options, para, 'rh')
  elif align_algo[0:-1] in ['HA_swaroop_img_align_loo'] :
    new_niter_lh = HA_swaroop(mkdg_data_lh_loo, options, para, 'lh')
    new_niter_rh = HA_swaroop(mkdg_data_rh_loo, options, para, 'rh')
  elif align_algo[0:-1] in ['pHA_EM_img_align_loo']:
    new_niter_lh = pHA_EM(mkdg_data_lh_loo, options, para, 'lh')
    new_niter_rh = pHA_EM(mkdg_data_rh_loo, options, para, 'rh')
  elif align_algo[0:-1] in ['None_loo'] :
    # without any alignment, set new_niter_lh and new_niter_rh=0, the corresponding transformation
    # matrices are identity matrices
    new_niter_lh = new_niter_rh = 0
  else :
    print 'alignment algo not recognize'

  #make sure right and left brain alignment are working at the same iterations
  assert new_niter_lh == new_niter_rh

  # load transformation matrices
  if not align_algo[0:-1] in ['None_loo']:
    workspace_lh = np.load(options['working_path']+para['align_algo']+'_lh_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz')
    workspace_rh = np.load(options['working_path']+para['align_algo']+'_rh_'+str(para['nvoxel'])+'vx_'+str(new_niter_rh)+'.npz')

  transform_lh = np.zeros((nvoxel,nvoxel,nsubjs+1))
  transform_rh = np.zeros((nvoxel,nvoxel,nsubjs+1))
  if align_algo[0:-1] in ['HA_img_align_loo','HA_swaroop_img_align_loo'] :
    transform_lh_tmp = workspace_lh['R']
    transform_rh_tmp = workspace_rh['R']
    for m in range(nsubjs):
      transform_lh[:,:,loo_idx[m]] = transform_lh_tmp[:,:,m]
      transform_rh[:,:,loo_idx[m]] = transform_rh_tmp[:,:,m]
    # find transform_lh[:,:,loo], transform_rh[:,:,loo]
    mkdg_data_lh_zscore = stats.zscore(mkdg_data_lh[:,:,loo].T ,axis=0, ddof=1).T 
    mkdg_data_rh_zscore = stats.zscore(mkdg_data_rh[:,:,loo].T ,axis=0, ddof=1).T
    U_lh, s_lh, V_lh = np.linalg.svd(mkdg_data_lh_zscore.dot(workspace_lh['G']), full_matrices=False)
    U_rh, s_rh, V_rh = np.linalg.svd(mkdg_data_rh_zscore.dot(workspace_rh['G']), full_matrices=False)
    transform_lh[:,:,loo] = U_lh.dot(V_lh)
    transform_rh[:,:,loo] = U_rh.dot(V_rh)
  elif align_algo[0:-1] in  ['pHA_EM_img_align_loo'] :
    bW_lh = workspace_lh['bW']
    bW_rh = workspace_rh['bW']
    for m in range(nsubjs):
      transform_lh[:,:,loo_idx[m]] = bW_lh[m*nvoxel:(m+1)*nvoxel,:]
      transform_rh[:,:,loo_idx[m]] = bW_rh[m*nvoxel:(m+1)*nvoxel,:]
    # find transform_lh[:,:,loo], transform_rh[:,:,loo]
    mkdg_data_lh_zscore = stats.zscore(mkdg_data_lh[:,:,loo].T ,axis=0, ddof=1).T 
    mkdg_data_rh_zscore = stats.zscore(mkdg_data_rh[:,:,loo].T ,axis=0, ddof=1).T
    U_lh, s_lh, V_lh = np.linalg.svd(mkdg_data_lh_zscore.dot(workspace_lh['ES'].T), full_matrices=False)
    U_rh, s_rh, V_rh = np.linalg.svd(mkdg_data_rh_zscore.dot(workspace_rh['ES'].T), full_matrices=False)
    transform_lh[:,:,loo] = U_lh.dot(V_lh)
    transform_rh[:,:,loo] = U_rh.dot(V_rh)
  elif align_algo[0:-1] in ['None_loo'] :
   for m in range(nsubjs+1):
      transform_lh[:,:,m] = np.identity(nvoxel)
      transform_rh[:,:,m] = np.identity(nvoxel)
  else :
    print 'alignment algo not recognize'

  # classification
  transformed_data = np.zeros((para['nvoxel']*2 ,56 ,nsubjs+1))

  # transformed mkdg data with learned transformation matrices
  for m in range(nsubjs+1):
    trfed_lh_tmp = transform_lh[:,:,m].T.dot(mkdg_data_lh[:,:,m])
    trfed_rh_tmp = transform_rh[:,:,m].T.dot(mkdg_data_rh[:,:,m])
    transformed_data[:,:,m] = stats.zscore( np.vstack((trfed_lh_tmp,trfed_rh_tmp)).T ,axis=0, ddof=1).T

  tst_data = np.zeros(shape = (para['nvoxel']*2,56))
  trn_data = np.zeros(shape = (para['nvoxel']*2,504))

  tst_data = transformed_data[:,:,loo]

  for m in range(nsubjs):
    trn_data[:,m*56:(m+1)*56] = transformed_data[:,:,loo_idx[m]]

  # scikit-learn svm for classification
  clf = NuSVC(nu=0.5, kernel = 'linear')
  clf.fit(trn_data.T, trn_label)
  pred_label = clf.predict(tst_data.T)
      
  accu = sum(pred_label == tst_label)/float(len(pred_label))

  np.savez_compressed(options['working_path']+'acc_'+para['align_algo']+'_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz',accu = accu)

  print np.mean(accu) 



