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

acc_HA_all = np.zeros((nsubjs, niter/niter_unit))
acc_HA_shuffle_all = np.zeros((nsubjs, niter/niter_unit))
acc_pHA_EM_all = np.zeros((nsubjs, niter/niter_unit))
acc_pHA_EM_shuffle_all = np.zeros((nsubjs, niter/niter_unit))


for i in range(1,niter/niter_unit):
  for m in range(nsubjs):
    ws_ha             = np.load(options['working_path']+'acc_HA_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_ha_shuffle     = np.load(options['working_path']+'acc_HA_shuffle_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_pha_em         = np.load(options['working_path']+'acc_pHA_EM_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_pha_em_shuffle = np.load(options['working_path']+'acc_pHA_EM_shuffle_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')

    acc_HA_all[m,i]             = ws_ha['accu']
    acc_HA_shuffle_all[m,i]     = ws_ha_shuffle['accu']
    acc_pHA_EM_all[m,i]         = ws_pha_em['accu'] 
    acc_pHA_EM_shuffle_all[m,i] = ws_pha_em_shuffle['accu'] 
    ws_ha.close()
    ws_ha_shuffle.close()
    ws_pha_em.close()
    ws_pha_em_shuffle.close()
iter_range = range(niter/niter_unit)
acc_HA_mean = acc_HA_all.mean(axis = 0).tolist()
acc_HA_se   = acc_HA_all.std(axis = 0)/math.sqrt(nsubjs)
acc_HA_shuffle_mean = acc_HA_shuffle_all.mean(axis = 0).tolist()
acc_HA_shuffle_se   = acc_HA_shuffle_all.std(axis = 0)/math.sqrt(nsubjs)

acc_pHA_EM_mean = acc_pHA_EM_all.mean(axis = 0)
acc_pHA_EM_se   = acc_pHA_EM_all.std(axis = 0)/math.sqrt(nsubjs)
acc_pHA_EM_shuffle_mean = acc_pHA_EM_shuffle_all.mean(axis = 0)
acc_pHA_EM_shuffle_se   = acc_pHA_EM_shuffle_all.std(axis = 0)/math.sqrt(nsubjs)

ws_none = np.load(options['working_path']+'acc_None_'+str(para['nvoxel'])+'vx_0.npz')
acc_None_mean = ws_none['accu'].mean(axis = 0)
acc_None_se   = ws_none['accu'].std(axis = 0)/math.sqrt(nsubjs)
 
acc_HA_mean[0] = acc_None_mean
acc_HA_se[0]   = acc_None_se
acc_pHA_EM_mean[0] = acc_None_mean
acc_pHA_EM_se[0]   = acc_None_se
acc_HA_shuffle_mean[0] = acc_None_mean
acc_HA_shuffle_se [0]  = acc_None_se
acc_pHA_EM_shuffle_mean[0] = acc_None_mean 
acc_pHA_EM_shuffle_se[0] = acc_None_se 

# set font size
font = {'family' : 'normal',
        'size'   : 18}

plt.rc('font', **font)

aspectratio = 25

# plot accuracy
plt.figure()
plt.errorbar(iter_range ,acc_HA_mean    ,acc_HA_se      , label="HA"    , markevery=2,linewidth=2, color='b', marker = 'o')
plt.errorbar(iter_range ,acc_pHA_EM_mean,acc_pHA_EM_se  , label="pHA EM", markevery=2, linewidth=2, color='r', marker = 'D',linestyle='--', markersize=7)
plt.errorbar(iter_range ,len(iter_range)*[acc_None_mean],\
                         len(iter_range)*[acc_None_se]  , label="no align"  , markevery=2, linewidth=2, color='g', marker = '.')
plt.plot    (iter_range ,len(iter_range)*[0.1428]       , label="chance", markevery=2, linewidth=2, color='k',linestyle='--')
plt.xlabel('Iterations')
plt.ylabel('Accuracy')
plt.ylim([0,0.8])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
plt.savefig(options['output_path']+'accuracy_loo_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000 ,bbox_inches='tight')

plt.figure()
plt.errorbar(iter_range ,acc_HA_shuffle_mean    ,acc_HA_shuffle_se    , label="HA shuffle", markevery=2,linewidth=2, color='b', marker = 'o')
plt.errorbar(iter_range ,acc_pHA_EM_shuffle_mean,acc_pHA_EM_shuffle_se, label="pHA EM shuffle",markevery=2, linewidth=2, color='r', marker = 'D',linestyle='--', markersize=7)
plt.errorbar(iter_range ,len(iter_range)*[acc_None_mean],\
                         len(iter_range)*[acc_None_se], label="no align"  , markevery=2, linewidth=2, color='g', marker = '.')
plt.plot    (iter_range ,len(iter_range)*[0.1428]     , label="chance", markevery=2, linewidth=2, color='k',linestyle='--')
plt.xlabel('Iterations')
plt.ylabel('Accuracy')
plt.ylim([0,0.8])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
plt.savefig(options['output_path']+'accuracy_loo_shuffle_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')



