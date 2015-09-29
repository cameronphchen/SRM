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
         'win_size'  : 9,\
         'nsubjs'    : 10,\
         'niter_unit': 1 }

niter      = para['niter']
nvoxel     = para['nvoxel']
nTR        = para['nTR']
nsubjs     = para['nsubjs']
niter_unit = para['niter_unit']
nrand      = para['nrand']
win_size   = para['win_size']

# load experiment options
# rondo options
options = {'input_path'  : '/jukebox/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/jukebox/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}
#           'working_path': '/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\



nfeature = [10,50,100,500,1000,1300]

acc_HA_SM = np.zeros((2*nsubjs*nrand, niter/niter_unit, len(nfeature)))

for i in range(1,niter/niter_unit):

  for k in range(len(nfeature)):
    for rand in range(nrand):
      ws_ha_sm_mysseg_1st = np.load(options['working_path'] +'winsize' +str(win_size)+ '/lowrank'+str(nfeature[k]) +'/rand'+str(rand)+'/HA_SM_Retraction_mysseg_1st'+\
                                  '/acc_HA_SM_Retraction_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
      ws_ha_sm_mysseg_2nd = np.load(options['working_path'] +'winsize' +str(win_size)+'/lowrank'+str(nfeature[k]) +'/rand'+str(rand)+'/HA_SM_Retraction_mysseg_2nd'+\
                                  '/acc_HA_SM_Retraction_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
      acc_HA_SM[range(2*rand*nsubjs,(2*rand+1)*nsubjs),i,k]     = ws_ha_sm_mysseg_1st['accu'] 
      acc_HA_SM[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),i,k] = ws_ha_sm_mysseg_2nd['accu'] 
      ws_ha_sm_mysseg_1st.close()
      ws_ha_sm_mysseg_2nd.close()

ws_none_mysseg_1st = np.load(options['working_path']+'acc_None_mysseg_1st_'+str(para['nvoxel'])+'vx_0.npz')
ws_none_mysseg_2nd = np.load(options['working_path']+'acc_None_mysseg_2nd_'+str(para['nvoxel'])+'vx_0.npz')

for k in range(len(nfeature)):
  for rand in range(nrand):
    acc_HA_SM[range(2*rand*nsubjs,(2*rand+1)*nsubjs),0,k]       = ws_none_mysseg_1st['accu'] 
    acc_HA_SM[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),0,k] = ws_none_mysseg_2nd['accu']

iter_range = range(niter/niter_unit)

#acc_pHA_EM_all[0:nsubjs,0]        = ws_none_mysseg_1st['accu'] 
#acc_pHA_EM_all[nsubjs:2*nsubjs,0] = ws_none_mysseg_2nd['accu'] 
#acc_pHA_EM_mean = acc_pHA_EM_all.mean(axis = 0)
#acc_pHA_EM_se   = acc_pHA_EM_all.std(axis = 0)/math.sqrt(nsubjs)

# set font size
font = {#'family' : 'normal',
        'size'   : 12
        }

plt.rc('font', **font)

aspectratio=10

# plot accuracy
plt.figure()
#sys.exit()

color_code = 'cbgkmycbgkmy'
marker_code ='......******'
plt.errorbar(iter_range ,len(iter_range)*[0.706],\
    len(iter_range)*[0.026]          , label="Neuron HA "      , markevery=2, linewidth=2, color='k',linestyle='--')
#plt.errorbar(iter_range ,acc_pHA_EM_mean,acc_pHA_EM_se  , label='pHA EM identity' , linewidth=2, color='r')
for k in range(len(nfeature)):
  acc_HA_SM_mean = acc_HA_SM[:,:,k].mean(axis = 0)
  acc_HA_SM_se   = acc_HA_SM[:,:,k].std(axis = 0)/math.sqrt(nsubjs)
  plt.errorbar(iter_range ,acc_HA_SM_mean,acc_HA_SM_se  , label='HA SM '+str(nfeature[k]) ,markevery=1, markersize=4, linewidth=1, color=color_code[k], marker=marker_code[k])
plt.xlabel('Iterations')
plt.ylabel('Accuracy')
#plt.ylim([0,0.9])
#plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
plt.text(.12, .05, 'Movie Segment Classification ', horizontalalignment='left', verticalalignment='bottom')
plt.text(.12, .01, 'Skinny Random Matrices', horizontalalignment='left', verticalalignment='bottom')
plt.savefig(options['output_path']+'accuracy_mysseg_'+str(win_size)+'TR_HA_SM_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')

