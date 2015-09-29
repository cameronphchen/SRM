#!/usr/bin/env python

# this is the code that runs the whole type 1 experiment
# for type 2 experiment, please refer to run_exp_loo.py
# 
# this code run a specific alignment algorithm (align_algo) for (niter) rounds
# with voxel selection algorithm selecting (nvoxel) amount of voxels
# and (nTR) TR of movie data for alignment 
# using both right and left VT data
#
# before running the experiment, please make sure to execute data_preprocessing.m and  transform_matdata2pydata.py to transformt the mat format data into python .npz
#
# align_algo = 'HA_mysseg_1st_loo0', 'pHA_EM_mysseg_1st_loo0' , 'None_mysseg_1st'
# 
# example: run_exp.py (align_algo) (n_iter) (n_voxel) (n_TR)
#          run_exp.p  HA  100  1300  2201
#
# by Cameron Po-Hsuan Chen @ Princeton


import numpy as np, scipy, random, sys, math, os
import scipy.io
from scipy import stats
import random
from libsvm.svmutil import *
from scikits.learn.svm import NuSVC
from ha import HA
from ha_rand import HA_rand
from ha_swaroop import HA_swaroop
from pha_em import pHA_EM
from pha_em_rand import pHA_EM_rand
import sys
sys.path.append('/Users/ChimatChen/anaconda/python.app/Contents/lib/python2.7/site-packages/')


# load experiment parameters
para  = {'align_algo': sys.argv[1],\
         'niter'     : int(sys.argv[2]),\
         'nvoxel'    : int(sys.argv[3]),\
         'nTR'       : int(sys.argv[4]),\
         'ranNum'       : int(sys.argv[5]),\
         'nsubjs'    : 9,\
         'niter_unit': 1 }

print para

align_algo = para['align_algo']
niter      = para['niter']
nvoxel     = para['nvoxel']
nTR        = para['nTR']
nsubjs     = para['nsubjs']
niter_unit = para['niter_unit']
loo        = align_algo[-1]
win_size   = 9 #TR
nseg       = nTR/2 - win_size

# load experiment options
# rondo options
options = {'input_path'  : '/jukebox/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/rand'+str(para['ranNum'])+'/',\
           'data_path'   : '/jukebox/ramadge/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/jukebox/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# local options
#options = {'input_path'  : '/Volumes/ramadge/pohsuan/pHA/data/input/', \
#           'working_path': '/Volumes/ramadge/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
#           'output_path' : '/Volumes/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

if not os.path.exists(options['working_path']):
  os.makedirs(options['working_path'])

if os.path.exists(options['working_path']+align_algo+'_lh_'+str(nvoxel)+'vx_current.npz'):
  os.remove(options['working_path']+align_algo+'_lh_'+str(nvoxel)+'vx_current.npz')
if os.path.exists(options['working_path']+align_algo+'_rh_'+str(nvoxel)+'vx_current.npz'):
  os.remove(options['working_path']+align_algo+'_rh_'+str(nvoxel)+'vx_current.npz')



##################loo classification###########################

# load mkdg data after voxel selection by matdata_preprocess.m
mkdg_data_lh = scipy.io.loadmat(options['data_path']+'mkdg_data_lh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_rh = scipy.io.loadmat(options['data_path']+'mkdg_data_rh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_lh = mkdg_data_lh['mkdg_data_lh'] 
mkdg_data_rh = mkdg_data_rh['mkdg_data_rh']

# load label for testing data
label = scipy.io.loadmat(options['input_path']+'subjall_picall_label.mat')
label = label['label']
trn_label = label[0:504]
tst_label = label[504:560]
trn_label = np.squeeze(np.asarray(trn_label))
tst_label = np.squeeze(np.asarray(tst_label))

###############################################################


# load movie data after voxel selection by matdata_preprocess.m 
movie_data_lh = scipy.io.loadmat(options['data_path']+'movie_data_lh_'+str(para['nvoxel'])+'vx.mat')
movie_data_rh = scipy.io.loadmat(options['data_path']+'movie_data_rh_'+str(para['nvoxel'])+'vx.mat')
movie_data_lh = movie_data_lh['movie_data_lh'] 
movie_data_rh = movie_data_rh['movie_data_rh'] 

movie_data_lh_1st = movie_data_lh[:,0:nTR/2,:]
movie_data_lh_2nd = movie_data_lh[:,(nTR/2+1):nTR,:]
movie_data_rh_1st = movie_data_rh[:,0:nTR/2,:]
movie_data_rh_2nd = movie_data_rh[:,(nTR/2+1):nTR,:]

if 'shuffle' in para['align_algo'] :
  print 'shuffle'
  time_idx = range(0,nTR/2)
  random.seed(0)
  time_idx = random.sample(time_idx,nTR/2)
  if '1st' in para['align_algo']: 
    movie_data_lh_1st = movie_data_lh_1st[:,time_idx,:]
    movie_data_rh_1st = movie_data_rh_1st[:,time_idx,:]
  elif '2nd' in para['align_algo']: 
    movie_data_lh_2nd = movie_data_lh_2nd[:,time_idx,:]
    movie_data_rh_2nd = movie_data_rh_2nd[:,time_idx,:]

movie_data_lh_trn = np.zeros((movie_data_lh_1st.shape))
movie_data_rh_trn = np.zeros((movie_data_rh_1st.shape))
movie_data_lh_tst = np.zeros((movie_data_lh_2nd.shape))
movie_data_rh_tst = np.zeros((movie_data_rh_2nd.shape))

if '1st' in para['align_algo']:
  for m in range(nsubjs+1):
    movie_data_lh_trn[:,:,m] = stats.zscore(movie_data_lh_1st[:,:,m].T ,axis=0, ddof=1).T
    movie_data_lh_tst[:,:,m] = stats.zscore(movie_data_lh_2nd[:,:,m].T ,axis=0, ddof=1).T 
    movie_data_rh_trn[:,:,m] = stats.zscore(movie_data_rh_1st[:,:,m].T ,axis=0, ddof=1).T 
    movie_data_rh_tst[:,:,m] = stats.zscore(movie_data_rh_2nd[:,:,m].T ,axis=0, ddof=1).T 
elif '2nd' in para['align_algo']:
  for m in range(nsubjs+1):
    movie_data_lh_trn[:,:,m] = stats.zscore(movie_data_lh_2nd[:,:,m].T ,axis=0, ddof=1).T 
    movie_data_lh_tst[:,:,m] = stats.zscore(movie_data_lh_1st[:,:,m].T ,axis=0, ddof=1).T 
    movie_data_rh_trn[:,:,m] = stats.zscore(movie_data_rh_2nd[:,:,m].T ,axis=0, ddof=1).T 
    movie_data_rh_tst[:,:,m] = stats.zscore(movie_data_rh_1st[:,:,m].T ,axis=0, ddof=1).T 

movie_data_lh_trn_loo = np.delete(movie_data_lh_trn, loo,2) 
movie_data_rh_trn_loo = np.delete(movie_data_rh_trn, loo,2)

loo_idx = range(10)
loo_idx = np.delete(loo_idx, loo)

# for niter/niter_unit round, each round the alignment algorithm will run niter_unit iterations
for i in range(para['niter']/para['niter_unit']):
  # alignment phase
  # fit the model to movie data with number of iterations
  if 'HA_mysseg' in para['align_algo'] or 'HA_shuffle_mysseg' in  para['align_algo'] :
    new_niter_lh = HA(movie_data_lh_trn_loo, options, para, 'lh')
    new_niter_rh = HA(movie_data_rh_trn_loo, options, para, 'rh')
  elif 'HA_rand_mysseg' in para['align_algo'] :
    new_niter_lh = HA_rand(movie_data_lh_trn_loo, options, para, 'lh')
    new_niter_rh = HA_rand(movie_data_rh_trn_loo, options, para, 'rh')
  elif 'pHA_EM_mysseg' in para['align_algo'] or 'pHA_EM_shuffle_mysseg' in  para['align_algo'] :
    new_niter_lh = pHA_EM(movie_data_lh_trn_loo, options, para, 'lh')
    new_niter_rh = pHA_EM(movie_data_rh_trn_loo, options, para, 'rh')
  elif 'pHA_EM_rand_mysseg' in para['align_algo'] :
    new_niter_lh = pHA_EM_rand(movie_data_lh_trn_loo, options, para, 'lh')
    new_niter_rh = pHA_EM_rand(movie_data_rh_trn_loo, options, para, 'rh')
  elif 'None' in para['align_algo']  :
    # without any alignment, set new_niter_lh and new_niter_rh=0, the corresponding transformation
    # matrices are identity matrices
    new_niter_lh = new_niter_rh = 0
  else :
    print 'alignment algo not recognize'

  #make sure right and left brain alignment are working at the same iterations
  assert new_niter_lh == new_niter_rh

  # load transformation matrices
  if not 'None' in para['align_algo'] :
    workspace_lh = np.load(options['working_path']+para['align_algo']+'_lh_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz')
    workspace_rh = np.load(options['working_path']+para['align_algo']+'_rh_'+str(para['nvoxel'])+'vx_'+str(new_niter_rh)+'.npz')

  transform_lh = np.zeros((nvoxel,nvoxel,nsubjs+1))
  transform_rh = np.zeros((nvoxel,nvoxel,nsubjs+1))
  if 'HA_mysseg' in para['align_algo'] or 'HA_shuffle_mysseg' in  para['align_algo'] or 'HA_rand_mysseg' in  para['align_algo']:
    transform_lh_tmp = workspace_lh['R']
    transform_rh_tmp = workspace_rh['R']
    for m in range(nsubjs):
      transform_lh[:,:,loo_idx[m]] = transform_lh_tmp[:,:,m]
      transform_rh[:,:,loo_idx[m]] = transform_rh_tmp[:,:,m]
    # find transform_lh[:,:,loo], transform_rh[:,:,loo]
    movie_data_lh_zscore = stats.zscore(movie_data_lh_trn[:,:,loo].T ,axis=0, ddof=1).T 
    movie_data_rh_zscore = stats.zscore(movie_data_rh_trn[:,:,loo].T ,axis=0, ddof=1).T
    U_lh, s_lh, V_lh = np.linalg.svd(movie_data_lh_zscore.dot(workspace_lh['G']), full_matrices=False)
    U_rh, s_rh, V_rh = np.linalg.svd(movie_data_rh_zscore.dot(workspace_rh['G']), full_matrices=False)
    transform_lh[:,:,loo] = U_lh.dot(V_lh)
    transform_rh[:,:,loo] = U_rh.dot(V_rh)

  elif 'pHA_EM_mysseg' in para['align_algo'] or 'pHA_EM_shuffle_mysseg' in  para['align_algo'] or 'pHA_EM_rand_mysseg' in  para['align_algo']:
    bW_lh = workspace_lh['bW']
    bW_rh = workspace_rh['bW']
    for m in range(nsubjs):
      transform_lh[:,:,loo_idx[m]] = bW_lh[m*nvoxel:(m+1)*nvoxel,:]
      transform_rh[:,:,loo_idx[m]] = bW_rh[m*nvoxel:(m+1)*nvoxel,:]
    # find transform_lh[:,:,loo], transform_rh[:,:,loo]
    movie_data_lh_zscore = stats.zscore(movie_data_lh_trn[:,:,loo].T ,axis=0, ddof=1).T 
    movie_data_rh_zscore = stats.zscore(movie_data_rh_trn[:,:,loo].T ,axis=0, ddof=1).T
    U_lh, s_lh, V_lh = np.linalg.svd(movie_data_lh_zscore.dot(workspace_lh['ES'].T), full_matrices=False)
    U_rh, s_rh, V_rh = np.linalg.svd(movie_data_rh_zscore.dot(workspace_rh['ES'].T), full_matrices=False)
    transform_lh[:,:,loo] = U_lh.dot(V_lh)
    transform_rh[:,:,loo] = U_rh.dot(V_rh)

  elif 'None' in para['align_algo'] :
    for m in range(nsubjs):
      transform_lh[:,:,m] = np.identity(nvoxel)
      transform_rh[:,:,m] = np.identity(nvoxel)
  else :
    print 'alignment algo not recognize'

################################ hao's implementation
  movie_data_tst_tmp = np.zeros((nvoxel*2,nTR/2,nsubjs+1))
  for t in range(nTR/2):
    if (t % 100) == 0:
      print '.',
      sys.stdout.flush()
    for m in range(nsubjs+1):
      movie_data_tst_tmp[0:nvoxel,t,m]        = transform_lh[:,:,m].T.dot(movie_data_lh_tst[:,t,m])
      movie_data_tst_tmp[nvoxel:2*nvoxel,t,m] = transform_rh[:,:,m].T.dot(movie_data_rh_tst[:,t,m])
  
  movie_data_tst = np.zeros((nvoxel*2,nTR/2,nsubjs+1))
  for m in range(nsubjs+1): 
    movie_data_tst[:,:,m] = stats.zscore(movie_data_tst_tmp[:,:,m].T ,axis=0, ddof=1).T 

  movie_data_sum = np.zeros((nvoxel*2*win_size, nseg))
  for m in range(nsubjs+1):
    for w in range(win_size):
      movie_data_sum[w*2*nvoxel:(w+1)*2*nvoxel,:] += movie_data_tst[:,w:(w+nseg),m]

  movie_data_loo = np.zeros((nvoxel*2*win_size, nseg))
  for w in range(win_size):
    movie_data_loo[w*2*nvoxel:(w+1)*2*nvoxel,:] = movie_data_tst[:,w:(w+nseg),loo]
    
  A =  stats.zscore((movie_data_sum - movie_data_loo),axis=0, ddof=1)
  B =  stats.zscore(movie_data_loo,axis=0, ddof=1)
  corr_mtx = B.T.dot(A)

  for i in range(nseg):
    for j in range(nseg):
      if abs(i-j)<win_size and i != j :
        corr_mtx[i,j] = -np.inf

  rank = np.argmax(corr_mtx, axis=1)

  accu = sum(rank == range(nseg)) / float(nseg)

  print accu

  if not os.path.exists(options['working_path']+align_algo[0:-1]):
    os.makedirs(options['working_path']+align_algo[0:-1])

  np.savez_compressed(options['working_path']+align_algo[0:-1]+'/acc_'+para['align_algo']+'_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz',accu = accu)



