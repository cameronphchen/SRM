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

# load label for testing data
label = scipy.io.loadmat(options['input_path']+'subjall_picall_label.mat')
label = label['label']

for run in range(4,10):
  print 'run'+str(run)

  trn_label = label[0:504]
  tst_label = label[range(7*run, 7*(run+1))]
  trn_label = np.squeeze(np.asarray(trn_label))
  tst_label = np.squeeze(np.asarray(tst_label))

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
    mkdg_data_align_lh = np.delete(mkdg_data_lh, range(7*run, 7*(run+1)) ,1) 
    mkdg_data_align_rh = np.delete(mkdg_data_rh, range(7*run, 7*(run+1)) ,1)

    if para['align_algo'] in ['HA_img_align'] :
      new_niter_lh = HA(mkdg_data_align_lh, options, para, 'lh')
      new_niter_rh = HA(mkdg_data_align_rh, options, para, 'rh')
    elif para['align_algo'] in ['pHA_EM_img_align']:
      new_niter_lh = pHA_EM(mkdg_data_align_lh, options, para, 'lh')
      new_niter_rh = pHA_EM(mkdg_data_align_rh, options, para, 'rh')
    elif para['align_algo'] == 'None' :
      # without any alignment, set new_niter_lh and new_niter_rh=0, the corresponding transformation
      # matrices are identity matrices
      new_niter_lh = new_niter_rh = 0
    else :
      print 'alignment algo not recognize'

    #make sure right and left brain alignment are working at the same iterations
    assert new_niter_lh == new_niter_rh

    # load transformation matrices
    if not para['align_algo'] == 'None':
      workspace_lh = np.load(options['working_path']+para['align_algo']+'_lh_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz')
      workspace_rh = np.load(options['working_path']+para['align_algo']+'_rh_'+str(para['nvoxel'])+'vx_'+str(new_niter_rh)+'.npz')

    if para['align_algo'] in ['HA_img_align'] :
      transform_lh = workspace_lh['R']
      transform_rh = workspace_rh['R']
    elif para['align_algo'] in  ['pHA_EM_img_align'] :
      transform_lh = np.zeros((nvoxel,nvoxel,nsubjs))
      transform_rh = np.zeros((nvoxel,nvoxel,nsubjs))
      bW_lh = workspace_lh['bW']
      bW_rh = workspace_rh['bW']
      for m in range(nsubjs):
        transform_lh[:,:,m] = bW_lh[m*nvoxel:(m+1)*nvoxel,:]
        transform_rh[:,:,m] = bW_rh[m*nvoxel:(m+1)*nvoxel,:]
    elif para['align_algo'] == 'None' :
      transform_lh = np.zeros((nvoxel,nvoxel,nsubjs))
      transform_rh = np.zeros((nvoxel,nvoxel,nsubjs))
      for m in range(nsubjs):
        transform_lh[:,:,m] = np.identity(nvoxel)
        transform_rh[:,:,m] = np.identity(nvoxel)
      else :
        print 'alignment algo not recognize'

    # classification
    transformed_data = np.zeros((para['nvoxel']*2 ,56 ,para['nsubjs']))

    # transformed mkdg data with learned transformation matrices
    for m in range(para['nsubjs']):
      trfed_lh_tmp = transform_lh[:,:,m].T.dot(mkdg_data_lh[:,:,m])
      trfed_rh_tmp = transform_rh[:,:,m].T.dot(mkdg_data_rh[:,:,m])
      transformed_data[:,:,m] = stats.zscore( np.vstack((trfed_lh_tmp,trfed_rh_tmp)).T ,axis=0, ddof=1).T

    tst_data = np.zeros(shape = (para['nvoxel']*2,56))
    trn_data = np.zeros(shape = (para['nvoxel']*2,504))

    accu = np.zeros(shape=10)

    for loo in range(para['nsubjs']):
        tst_data = transformed_data[:,range(7*run,7*(run+1)),loo]

        loo_idx = range(para['nsubjs'])
        loo_idx.remove(loo)

        for m in range(para['nsubjs']-1):
          trn_data[:,m*56:(m+1)*56] = transformed_data[:,:,loo_idx[m]]

        # scikit-learn svm for classification
        clf = NuSVC(nu=0.5, kernel = 'linear')
        clf.fit(trn_data.T, trn_label)
        pred_label = clf.predict(tst_data.T)
      

        accu[loo] = sum(pred_label == tst_label)/float(len(pred_label))

    np.savez_compressed(options['working_path']+'acc_'+para['align_algo']+'_'+str(para['nvoxel'])+'vx_run'+str(run)+'_'+str(new_niter_lh)+'.npz',accu = accu)
    print np.mean(accu) 



