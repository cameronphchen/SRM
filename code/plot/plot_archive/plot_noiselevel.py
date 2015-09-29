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

noise_lh = np.zeros((nsubjs, niter/niter_unit))
noise_rh = np.zeros((nsubjs, niter/niter_unit))


for i in range(niter/niter_unit):
  ws_lh = np.load(options['working_path']+'pHA_EM_lh_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
  ws_rh = np.load(options['working_path']+'pHA_EM_rh_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')

  noise_lh[:,i] = ws_lh['sigma2']
  noise_rh[:,i] = ws_rh['sigma2'] 

iter_range = range(niter/niter_unit)
 

# plot subject specific prediciton accuracy
plt.figure()
plt.plot(iter_range ,(noise_lh[7,:]+noise_rh[0,:])/2, marker = 'x', markevery=2, label = str(0))
plt.plot(iter_range ,(noise_lh[7,:]+noise_rh[1,:])/2, marker = 'x', markevery=3, label = str(1))
plt.plot(iter_range ,(noise_lh[7,:]+noise_rh[2,:])/2, marker = 'x', markevery=2, label = str(2))
plt.plot(iter_range ,(noise_lh[7,:]+noise_rh[3,:])/2, marker = 'x', markevery=2, label = str(3))
plt.plot(iter_range ,(noise_lh[7,:]+noise_rh[4,:])/2, marker = 'x', markevery=2, label = str(4))
plt.plot(iter_range ,(noise_lh[7,:]+noise_rh[5,:])/2, marker = 'x', markevery=2, label = str(5))
plt.plot(iter_range ,(noise_lh[7,:]+noise_rh[6,:])/2, marker = 'x', markevery=3, label = str(6))
plt.plot(iter_range ,(noise_lh[7,:]+noise_rh[7,:])/2, marker = 'o', markevery=4, label = str(7))
plt.plot(iter_range ,(noise_lh[8,:]+noise_rh[8,:])/2, marker = 'o', markevery=3, label = str(8))
plt.plot(iter_range ,(noise_lh[9,:]+noise_rh[9,:])/2, marker = 'o', markevery=3, label = str(9))

plt.xlabel('Iteartions')
plt.ylabel('Accuracy')
plt.ylim([0.45,10])
#plt.legend(loc=4)
plt.savefig(options['output_path']+'pHAEM_allsubj_noise_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000)

