#!/usr/bin/env python

# this is the code that runs the whole type 1 experiment
# using movie data to learn alignment parameter and conduct classification on 
# image data
#
# for type 2 (leave-one-out) experiment, please refer to run_exp_loo.py
# 
# this code run a specific alignment algorithm (align_algo) for (niter) rounds
# with voxel selection algorithm selecting (nvoxel) amount of voxels
# and (nTR) TR of movie data for alignment 
# using both right and left VT data
#
# before running the experiment, please make sure to execute data_preprocessing.m and  transform_matdata2pydata.py to transformt the mat format data into python .npz
#
# align_algo = 'HA', 'HA_shuffle', 'pHA_EM', 'pHA_EM_shuffle', 'None'
# 
# example: run_exp.py (align_algo) (n_iter) (n_voxel) (n_TR)
#          run_exp.p  HA  100  1300  2201
#
# by Cameron Po-Hsuan Chen @ Princeton


import numpy as np, scipy, random, sys, math, os
import scipy.io
from scipy import stats
import random
#from libsvm.svmutil import *
from scikits.learn.svm import NuSVC
from alignment_algo import *
import sys
sys.path.append('/usr/local/epd-7.1-2-rh5-x86_64/lib/python2.7/site-packages/libsvm')


# load experiment parameters
para  = {'dataset'   : sys.argv[1],\
         'exptype'   : sys.argv[2],\
         'align_algo': sys.argv[3],\
         'niter'     : int(sys.argv[4]),\
         'nvoxel'    : int(sys.argv[5]),\
         'nTR'       : int(sys.argv[6]),\
         'nsubjs'    : 10,\
         'niter_unit': 1 }

print para
align_algo = para['align_algo']
niter      = para['niter']
nvoxel     = para['nvoxel']
nTR        = para['nTR']
nsubjs     = para['nsubjs']
niter_unit = para['niter_unit']

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
movie_data_lh = scipy.io.loadmat(options['working_path']+'movie_data_lh_'+str(para['nvoxel'])+'vx.mat')
movie_data_rh = scipy.io.loadmat(options['working_path']+'movie_data_rh_'+str(para['nvoxel'])+'vx.mat')
movie_data_lh = movie_data_lh['movie_data_lh'] 
movie_data_rh = movie_data_rh['movie_data_rh'] 

# load mkdg data after voxel selection by matdata_preprocess.m
mkdg_data_lh = scipy.io.loadmat(options['working_path']+'mkdg_data_lh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_rh = scipy.io.loadmat(options['working_path']+'mkdg_data_rh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_lh = mkdg_data_lh['mkdg_data_lh'] 
mkdg_data_rh = mkdg_data_rh['mkdg_data_rh']

if 'shuffle' in para['align_algo'] :
  print 'shuffle'
  time_idx = range(0,nTR)
  random.seed(0)
  time_idx = random.sample(time_idx,nTR)
  movie_data_lh = movie_data_lh[:,time_idx]
  movie_data_rh = movie_data_rh[:,time_idx]

# load label for testing data
label = scipy.io.loadmat(options['input_path']+'subjall_picall_label.mat')
label = label['label']
trn_label = label[0:504]
tst_label = label[504:560]
trn_label = np.squeeze(np.asarray(trn_label))
tst_label = np.squeeze(np.asarray(tst_label))

#if para['align_algo'] in ['pHA_EM_lowrank', 'spHA_VI']:
#  para['ranNum']=int(sys.argv[5])
#  para['nfeature'] = int(sys.argv[6])
#  nfeature = para['nfeature']
#  options['working_path'] = options['working_path'] + 'lowrank' + str(nfeature) +'/' + 'rand' + str(para['ranNum']) +'/'
#elif para['align_algo'] in ['pHA_EM_shift_lowrank']:
#  para['nfeature'] = int(sys.argv[5])
#  nfeature = para['nfeature']
#  options['working_path'] = options['working_path'] + 'lowrank' + str(nfeature) +'/'
nfeature = nvoxel
if 'spHA_VI' in para['align_algo']:
  para['ranNum']=int(sys.argv[5])
  para['nfeature'] = int(sys.argv[6])
  para['kernel']   = sys.argv[7]
  nfeature = para['nfeature']
  options['working_path'] = options['working_path'] + para['kernel'] + '/' +'lowrank' + str(nfeature) +'/' + 'rand' + str(para['ranNum']) +'/'
elif 'pHA_EM_lowrank' in para['align_algo'] or 'HA_SM_Newton' in para['align_algo'] or 'HA_SM_Retraction' in para['align_algo']:
  para['ranNum']=int(sys.argv[5])
  para['nfeature'] = int(sys.argv[6])
  nfeature = para['nfeature']
  options['working_path'] = options['working_path'] + 'lowrank' + str(nfeature) +'/' + 'rand' + str(para['ranNum']) +'/'
elif 'pHA_EM_shift_lowrank' in para['align_algo'] :
  para['nfeature'] = int(sys.argv[5])
  nfeature = para['nfeature']
  options['working_path'] = options['working_path'] + 'lowrank' + str(nfeature) +'/'
elif 'HA_rand' in para['align_algo'] or 'pHA_EM_rand' in para['align_algo']:
  para['ranNum'] = int(sys.argv[5])
  options['working_path'] = options['working_path'] + '/rand'+str(para['ranNum'])+'/'
elif 'HAreg' in para['align_algo'] :
  para['alpha']=float(sys.argv[5])
elif 'pPCA'  in para['align_algo'] or 'pICA' in para['align_algo'] :
  para['nfeature'] = int(sys.argv[5])
  nfeature = para['nfeature']
  options['working_path'] = options['working_path'] + 'lowrank' + str(nfeature) +'/'

if not os.path.exists(options['working_path']):
  os.makedirs(options['working_path'])

# for niter/niter_unit round, each round the alignment algorithm will run niter_unit iterations
for i in range(para['niter']/para['niter_unit']):
  
  # alignment phase
  # fit the model to movie data with number of iterations
  if para['align_algo'] in ['HA', 'HA_shuffle'] :
    new_niter_lh = HA(movie_data_lh, options, para, 'lh')
    new_niter_rh = HA(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['HA_rand'] :
    new_niter_lh = HA_rand(movie_data_lh, options, para, 'lh')
    new_niter_rh = HA_rand(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['HA_swaroop','HA_swaroop_shuffle'] :
    new_niter_lh = HA_swaroop(movie_data_lh, options, para, 'lh')
    new_niter_rh = HA_swaroop(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['HA_SM_Newton'] :
    new_niter_lh = HA_SM_Newton(movie_data_lh, options, para, 'lh')
    new_niter_rh = HA_SM_Newton(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['HA_SM_Retraction'] :
    new_niter_lh = HA_SM_Retraction(movie_data_lh, options, para, 'lh')
    new_niter_rh = HA_SM_Retraction(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['pHA_EM', 'pHA_EM_shuffle']:
    new_niter_lh = pHA_EM(movie_data_lh, options, para, 'lh')
    new_niter_rh = pHA_EM(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['pHA_EM_rand']:
    new_niter_lh = pHA_EM_rand(movie_data_lh, options, para, 'lh')
    new_niter_rh = pHA_EM_rand(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['pHA_EM_lowrank']:
    new_niter_lh = pHA_EM_lowrank(movie_data_lh, options, para, 'lh')
    new_niter_rh = pHA_EM_lowrank(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['pHA_EM_shift_lowrank']:
    new_niter_lh = pHA_EM_shift_lowrank(movie_data_lh, options, para, 'lh')
    new_niter_rh = pHA_EM_shift_lowrank(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['spHA_VI'] :
    new_niter_lh = spHA_VI(movie_data_lh, options, para, 'lh')
    new_niter_rh = spHA_VI(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['pPCA']:
    new_niter_lh = pPCA(movie_data_lh, options, para, 'lh')
    new_niter_rh = pPCA(movie_data_rh, options, para, 'rh')
  elif para['align_algo'] in ['pICA']:
    new_niter_lh = pICA(movie_data_lh, options, para, 'lh')
    new_niter_rh = pICA(movie_data_rh, options, para, 'rh')
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

  if para['align_algo'] in ['HA', 'HA_shuffle','HA_swaroop','HA_swaroop_shuffle','HA_rand'] :
    transformed_data = np.zeros((para['nvoxel']*2 ,56 ,para['nsubjs']))
    tst_data = np.zeros(shape = (para['nvoxel']*2,56))
    trn_data = np.zeros(shape = (para['nvoxel']*2,504))

    transform_lh = workspace_lh['R']
    transform_rh = workspace_rh['R']
  #elif 'pHA_EM' in para['align_algo'] or 'pHA_EM_rand' in para['align_algo'] or 'spHA_VI' in para['align_algo']:
  elif para['align_algo'] in ['pHA_EM', 'pHA_EM_rand']:
    transformed_data = np.zeros((para['nvoxel']*2 ,56 ,para['nsubjs']))
    tst_data = np.zeros(shape = (para['nvoxel']*2,56))
    trn_data = np.zeros(shape = (para['nvoxel']*2,504))
 
    transform_lh = np.zeros((nvoxel,nvoxel,nsubjs))
    transform_rh = np.zeros((nvoxel,nvoxel,nsubjs))
    bW_lh = workspace_lh['bW']
    bW_rh = workspace_rh['bW']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh[m*nvoxel:(m+1)*nvoxel,:]
      transform_rh[:,:,m] = bW_rh[m*nvoxel:(m+1)*nvoxel,:]
  elif para['align_algo'] in [ 'pHA_EM_lowrank', 'pHA_EM_shift_lowrank','spHA_VI']:
    transformed_data = np.zeros((nfeature*2 ,56 ,para['nsubjs']))
    tst_data = np.zeros(shape = (nfeature*2,56))
    trn_data = np.zeros(shape = (nfeature*2,504))

    transform_lh = np.zeros((nvoxel,nfeature,nsubjs))
    transform_rh = np.zeros((nvoxel,nfeature,nsubjs))
    bW_lh = workspace_lh['bW']
    bW_rh = workspace_rh['bW']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh[m*nvoxel:(m+1)*nvoxel,:]
      transform_rh[:,:,m] = bW_rh[m*nvoxel:(m+1)*nvoxel,:]
  elif 'pPCA' in  para['align_algo'] or 'pICA' in para['align_algo']:
    transformed_data = np.zeros((nfeature*2 ,56 ,para['nsubjs']))
    tst_data = np.zeros(shape = (nfeature*2,56))
    trn_data = np.zeros(shape = (nfeature*2,504))
    transform_lh = np.zeros((nvoxel,nfeature,nsubjs))
    transform_rh = np.zeros((nvoxel,nfeature,nsubjs))
    bW_lh = workspace_lh['R']
    bW_rh = workspace_rh['R']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh
      transform_rh[:,:,m] = bW_rh
  elif 'HA_SM_Newton' in  para['align_algo'] or 'HA_SM_Retraction' in para['align_algo']:
    transformed_data = np.zeros((nfeature*2 ,56 ,para['nsubjs']))
    tst_data = np.zeros(shape = (nfeature*2,56))
    trn_data = np.zeros(shape = (nfeature*2,504))
    transform_lh = np.zeros((nvoxel,nfeature,nsubjs))
    transform_rh = np.zeros((nvoxel,nfeature,nsubjs))
    bW_lh = workspace_lh['W']
    bW_rh = workspace_rh['W']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh[:,:,m]
      transform_rh[:,:,m] = bW_rh[:,:,m]
  elif para['align_algo'] == 'None' :
    transform_lh = np.zeros((nvoxel,nvoxel,nsubjs))
    transform_rh = np.zeros((nvoxel,nvoxel,nsubjs))
    for m in range(nsubjs):
      transform_lh[:,:,m] = np.identity(nvoxel)
      transform_rh[:,:,m] = np.identity(nvoxel)
  else :
    print 'alignment algo not recognize'

  # classification
  #transformed_data = np.zeros((para['nvoxel']*2 ,56 ,para['nsubjs']))

  # transformed mkdg data with learned transformation matrices
  for m in range(para['nsubjs']):
    trfed_lh_tmp = transform_lh[:,:,m].T.dot(mkdg_data_lh[:,:,m])
    trfed_rh_tmp = transform_rh[:,:,m].T.dot(mkdg_data_rh[:,:,m])
    transformed_data[:,:,m] = stats.zscore( np.vstack((trfed_lh_tmp,trfed_rh_tmp)).T ,axis=0, ddof=1).T

  #tst_data = np.zeros(shape = (para['nvoxel']*2,56))
  #trn_data = np.zeros(shape = (para['nvoxel']*2,504))
  accu = np.zeros(shape=10)

  for loo in range(para['nsubjs']):
      tst_data = transformed_data[:,:,loo]

      loo_idx = range(para['nsubjs'])
      loo_idx.remove(loo)

      for m in range(para['nsubjs']-1):
        trn_data[:,m*56:(m+1)*56] = transformed_data[:,:,loo_idx[m]]

      # scikit-learn svm for classification
      clf = NuSVC(nu=0.5, kernel = 'linear')
      clf.fit(trn_data.T, trn_label)
      pred_label = clf.predict(tst_data.T)
      
      # libsvm
      #trn_label_list = trn_label.tolist()
      #tst_label_list = tst_label.tolist()
      #trn_data_T_tolist = trn_data.T.tolist()
      #tst_data_T_tolist = tst_data.T.tolist()
      #prob = svm_problem(trn_label_list,trn_data_T_tolist)
      #param = svm_parameter('-s 1 -t 0 -n 0.5 -p 0.001')
      #m = svm_train(prob, param)
      #pred_label = svm_predict(tst_label_list,tst_data_T_tolist,m)    

      accu[loo] = sum(pred_label == tst_label)/float(len(pred_label))

  np.savez_compressed(options['working_path']+'acc_'+para['align_algo']+'_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz',accu = accu)

  print np.mean(accu) 



