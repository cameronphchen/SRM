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
options = {'input_path'  : '/jukebox/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/jukebox/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# local options
#options = {'input_path'  : '/Volumes/ramadge/pohsuan/pHA/data/input/', \
#           'working_path': '/Volumes/ramadge/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
#           'output_path' : '/Volumes/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

loglike = np.zeros(niter/niter_unit)

for i in range(1,niter):
  ws_lh = np.load(options['output_path']+'pHA_EM_lowrank_mysseg_1st_loglikelihood_lh_'+str(nvoxel)+'vx_'+str(i)+'.npz')
  ws_rh = np.load(options['output_path']+'pHA_EM_lowrank_mysseg_1st_loglikelihood_rh_'+str(nvoxel)+'vx_'+str(i)+'.npz')
  
  loglike[i] = ws_lh['loglike'] + ws_rh['loglike'] 

iter_range = range(niter/niter_unit)

# plot accuracy
plt.figure()
plt.plot    (iter_range[1:] ,loglike[1:] )
plt.xlabel('Iteration')
plt.ylabel('Log Likelihood')
plt.xlim([1,50])
plt.savefig(options['output_path']+'loglike_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000)


