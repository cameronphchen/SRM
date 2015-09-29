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
         'nrand'     : int(sys.argv[4]),\
         'nsubjs'    : 10,\
         'niter_unit': 1 }

niter      = para['niter']
nvoxel     = para['nvoxel']
nTR        = para['nTR']
nsubjs     = para['nsubjs']
niter_unit = para['niter_unit']
nrand      = para['nrand']

# load experiment options
# rondo options
options = {'input_path'  : '/jukebox/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/jukebox/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# local options
#options = {'input_path'  : '/Volumes/ramadge/pohsuan/pHA/data/input/', \
#           'working_path': '/Volumes/ramadge/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
#           'output_path' : '/Volumes/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

nfeature = [10,20,30,40,50,100,500,1000,1300]

acc_pHA_EM_lowrank_all = np.zeros((nsubjs*nrand, niter/niter_unit, len(nfeature)))
acc_pHA_EM_all = np.zeros((nsubjs, niter/niter_unit))

for i in range(1,niter/niter_unit):
  ws_pha_em = np.load(options['working_path']+'acc_pHA_EM_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
  acc_pHA_EM_all[:,i] = ws_pha_em['accu']
  ws_pha_em.close()
  for k in range(len(nfeature)):
    for rand in range(nrand):
      ws_pha_em_lowrank = np.load(options['working_path']+ 'lowrank'+str(nfeature[k]) +'/rand'+str(rand)+'/acc_pHA_EM_lowrank_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
      acc_pHA_EM_lowrank_all[range(rand*nsubjs,(rand+1)*nsubjs),i,k] = ws_pha_em_lowrank['accu'] 
      ws_pha_em_lowrank.close()

ws_none = np.load(options['working_path']+'acc_None_'+str(para['nvoxel'])+'vx_0.npz')
acc_None_mean = ws_none['accu'].mean(axis = 0)
acc_None_se   = ws_none['accu'].std(axis = 0)/math.sqrt(nsubjs)

iter_range = range(niter/niter_unit)

acc_pHA_EM_mean = acc_pHA_EM_all.mean(axis = 0)
acc_pHA_EM_se   = acc_pHA_EM_all.std(axis = 0)/math.sqrt(nsubjs)
acc_pHA_EM_mean[0] = acc_None_mean
acc_pHA_EM_se[0]   = acc_None_se

# set font size
font = {#'family' : 'normal',
    'size'   : 10:conf q
    }

plt.rc('font', **font)

aspectratio=8

# plot accuracy
plt.figure()
#sys.exit()

color_code = 'cbgkmycbgkmy'
marker_code ='......******'

plt.errorbar(iter_range ,len(iter_range)*[0.639],\
                         len(iter_range)*[0.022]          , label="Neuron HA "      , markevery=2, linewidth=2, color='k',linestyle='--')
plt.errorbar(iter_range ,acc_pHA_EM_mean,acc_pHA_EM_se  , label='pHA EM identity' , linewidth=2, color='r')
for k in range(len(nfeature)):
  acc_pHA_EM_lowrank_mean = acc_pHA_EM_lowrank_all[:,:,k].mean(axis = 0)
  acc_pHA_EM_lowrank_se   = acc_pHA_EM_lowrank_all[:,:,k].std(axis = 0)/math.sqrt(nsubjs)
  acc_pHA_EM_lowrank_mean[0] = acc_None_mean
  acc_pHA_EM_lowrank_se[0]   = acc_None_se
  plt.errorbar(iter_range ,acc_pHA_EM_lowrank_mean,acc_pHA_EM_lowrank_se  , label='pHA EM '+str(nfeature[k]) , linewidth=1, color=color_code[k], marker=marker_code[k])
plt.xlabel('Iterations')
plt.ylabel('Accuracy')
plt.ylim([0,0.8])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
plt.text(.12, .05, 'Image Classification', horizontalalignment='left', verticalalignment='bottom')
plt.text(.12, .01, 'Skinny Random Matrices', horizontalalignment='left', verticalalignment='bottom')
plt.savefig(options['output_path']+'accuracy_lowrank_rand_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')

