#!/usr/bin/env python

# by Cameron Po-Hsuan Chen @ Princeton

import numpy as np, scipy, random, sys, math, os
import scipy.io
from scipy import stats

sys.path.append('/Users/ChimatChen/anaconda/python.app/Contents/lib/python2.7/site-packages/')

from libsvm.svmutil import *
from scikits.learn.svm import NuSVC

import numpy as np
import matplotlib.pyplot as plt
import sys

# load experiment parameters
para  = {'niter'     : int(sys.argv[1]),\
         'nvoxel'    : int(sys.argv[2]),\
         'nTR'       : int(sys.argv[3]),\
         'nsubjs'    : 10,\
         'niter_unit': 1 }

niter      = para['niter']
nvoxel     = para['nvoxel']
nTR        = para['nTR']
nsubjs     = para['nsubjs']
niter_unit = para['niter_unit']

# load experiment options
# rondo options
options = {'input_path'  : '/mnt/cd/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/mnt/cd/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/mnt/cd/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# local options
#options = {'input_path'  : '/Volumes/ramadge/pohsuan/pHA/data/input/', \
#           'working_path': '/Volumes/ramadge/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
#           'output_path' : '/Volumes/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}


movie_data_lh = scipy.io.loadmat(options['working_path']+'movie_data_lh_'+str(nvoxel)+'vx.mat')
movie_data_rh = scipy.io.loadmat(options['working_path']+'movie_data_rh_'+str(nvoxel)+'vx.mat')
movie_data_lh = movie_data_lh['movie_data_lh'] 
movie_data_rh = movie_data_rh['movie_data_rh']


bX_lh = np.zeros((nsubjs*nvoxel,nTR))
bX_rh = np.zeros((nsubjs*nvoxel,nTR))
for m in range(nsubjs):
  bX_lh[m*nvoxel:(m+1)*nvoxel,:] = stats.zscore(movie_data_lh[:,:,m].T ,axis=0, ddof=1).T
  bX_rh[m*nvoxel:(m+1)*nvoxel,:] = stats.zscore(movie_data_rh[:,:,m].T ,axis=0, ddof=1).T

bX_lh = bX_lh - bX_lh.mean(axis=1)[:,np.newaxis]
bX_rh = bX_rh - bX_rh.mean(axis=1)[:,np.newaxis]

loglike_lh = np.zeros(niter/niter_unit)
loglike_rh = np.zeros(niter/niter_unit)

for i in range(niter/niter_unit):
  print i
  sys.stdout.flush()
  ws_lh = np.load(options['working_path']+'pHA_EM_lh_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
  ws_rh = np.load(options['working_path']+'pHA_EM_rh_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')

  bSig_s_lh = ws_lh['bSig_s'] 
  bW_lh     = ws_lh['bW']
  bmu_lh    = ws_lh['bmu']
  sigma2_lh = ws_lh['sigma2']

  bSig_s_rh = ws_rh['bSig_s'] 
  bW_rh     = ws_rh['bW']
  bmu_rh    = ws_rh['bmu']
  sigma2_rh = ws_rh['sigma2']

  bSig_x_lh = np.zeros((nvoxel*nsubjs,nvoxel*nsubjs))
  bSig_x_lh = bW_lh.dot(bSig_s_lh).dot(bW_lh.T)

  bSig_x_rh = np.zeros((nvoxel*nsubjs,nvoxel*nsubjs))
  bSig_x_rh = bW_rh.dot(bSig_s_rh).dot(bW_rh.T)
 
  for m in range(nsubjs):
    bSig_x_lh[m*nvoxel:(m+1)*nvoxel,m*nvoxel:(m+1)*nvoxel] += sigma2_lh[m]*np.identity(nvoxel)
    bSig_x_rh[m*nvoxel:(m+1)*nvoxel,m*nvoxel:(m+1)*nvoxel] += sigma2_rh[m]*np.identity(nvoxel)

  inv_bSig_x_lh = scipy.linalg.inv(bSig_x_lh)
  inv_bSig_x_rh = scipy.linalg.inv(bSig_x_rh)

  sign_lh , logdet_lh = np.linalg.slogdet(bSig_x_lh)
  sign_rh , logdet_rh = np.linalg.slogdet(bSig_x_rh)
  if sign_lh == -1 or sign_rh == -1:
    print str(i)+'th iteration, log sign negative'

  loglike_lh[i] = -0.5*nTR*logdet_lh - 0.5*np.trace(bX_lh.T.dot(inv_bSig_x_lh).dot(bX_lh)) #-0.5*nTR*nvoxel*nsubjs*math.log(2*math.pi)   
  loglike_rh[i] = -0.5*nTR*logdet_rh - 0.5*np.trace(bX_rh.T.dot(inv_bSig_x_rh).dot(bX_rh)) #-0.5*nTR*nvoxel*nsubjs*math.log(2*math.pi) 

  np.savez_compressed(options['output_path']+'pHA_EM_loglikelihood_'+str(nvoxel)+'vx_'+str(i)+'.npz',\
                   loglike_lh=loglike_lh, loglike_rh=loglike_rh)

  print 'lh'+str(-0.5*nTR*logdet_lh)+','+str(-0.5*np.trace(bX_lh.T.dot(inv_bSig_x_lh).dot(bX_lh)))
  print 'rh'+str(-0.5*nTR*logdet_rh)+','+str(-0.5*np.trace(bX_rh.T.dot(inv_bSig_x_rh).dot(bX_rh))) 
  print str(i)+':' + str(loglike_lh[i]) +','+ str(loglike_rh[i]) 
