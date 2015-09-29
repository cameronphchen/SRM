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
acc_pHA_EM_all = np.zeros((nsubjs, niter/niter_unit))
acc_HA_rand_all = np.zeros((nsubjs*10, niter/niter_unit))
acc_pHA_EM_rand_all = np.zeros((nsubjs*10, niter/niter_unit))

rand_num = 10

for i in range(niter/niter_unit):
  ws_ha     = np.load(options['working_path']+'acc_HA_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
  ws_pha_em = np.load(options['working_path']+'acc_pHA_EM_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')

  acc_HA_all[:,i]             = ws_ha['accu']
  acc_pHA_EM_all[:,i]         = ws_pha_em['accu'] 

  for rnd in range(rand_num):
    ws_ha_rand     = np.load(options['working_path']+'HA_rand/HA_rand_'+str(rnd)+'/acc_HA_rand_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_pha_em_rand = np.load(options['working_path']+'pHA_EM_rand/pHA_EM_rand_'+str(rnd)+'/acc_pHA_EM_rand_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')

    acc_HA_rand_all[range(rnd*rand_num,(rnd+1)*rand_num),i]     = ws_ha_rand['accu']
    acc_pHA_EM_rand_all[range(rnd*rand_num,(rnd+1)*rand_num),i] = ws_pha_em_rand['accu'] 
    
    ws_ha_rand.close()
    ws_pha_em_rand.close()

  ws_ha.close()
  ws_pha_em.close()

iter_range = range(niter/niter_unit)
acc_HA_mean = acc_HA_all.mean(axis = 0).tolist()
acc_HA_se   = acc_HA_all.std(axis = 0)/math.sqrt(nsubjs)
acc_HA_rand_mean = acc_HA_rand_all.mean(axis = 0).tolist()
acc_HA_rand_se   = acc_HA_rand_all.std(axis = 0)/math.sqrt(nsubjs)

acc_pHA_EM_mean = acc_pHA_EM_all.mean(axis = 0)
acc_pHA_EM_se   = acc_pHA_EM_all.std(axis = 0)/math.sqrt(nsubjs)
acc_pHA_EM_rand_mean = acc_pHA_EM_rand_all.mean(axis = 0)
acc_pHA_EM_rand_se   = acc_pHA_EM_rand_all.std(axis = 0)/math.sqrt(nsubjs)
 

acc_None_mean = acc_pHA_EM_mean[0]
acc_None_se   = acc_pHA_EM_se[0]

# set font size
font = {#'family' : 'normal',
        'size'   : 10}

plt.rc('font', **font)

aspectratio=8

# plot accuracy
plt.figure()
plt.errorbar(iter_range ,len(iter_range)*[0.639],\
                         len(iter_range)*[0.022]          , label="Neuron HA "      , markevery=2, linewidth=2, color='k',linestyle='--')
plt.errorbar(iter_range ,acc_HA_mean    ,acc_HA_se      , label="HA identity"      , markevery=2,linewidth=2, color='b', marker = 'o')
plt.errorbar(iter_range ,acc_pHA_EM_mean,acc_pHA_EM_se  , label="pHA EM identity"  , markevery=2, linewidth=2, color='r', marker = 'D',linestyle='--', markersize=4)
#plt.errorbar(iter_range ,len(iter_range)*[acc_None_mean],\
#                         len(iter_range)*[acc_None_se]  , label="no align", markevery=2, linewidth=2, color='g', marker = '.')
#plt.plot    (iter_range ,len(iter_range)*[0.1428]       , label="chance", markevery=2, linewidth=2, color='k',linestyle='--')
#plt.xlabel('Iterations')
#plt.ylabel('Accuracy')
#plt.ylim([0,0.8])
#plt.axes().set_aspect(aspectratio)
#plt.legend(loc=4)
#plt.savefig(options['output_path']+'accuracy_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')

#plt.figure()
plt.errorbar(iter_range ,acc_HA_rand_mean    ,acc_HA_rand_se    , label="HA rand"    , markevery=3,linewidth=2, color='c', marker = 'x')
plt.errorbar(iter_range ,acc_pHA_EM_rand_mean,acc_pHA_EM_rand_se, label="pHA EM rand", markevery=3, linewidth=2, color='m', marker = 'x')

plt.errorbar(iter_range ,len(iter_range)*[acc_None_mean],\
                         len(iter_range)*[acc_None_se]                , label="no align"      , markevery=2, linewidth=2, color='g', marker = '.')
plt.plot    (iter_range ,len(iter_range)*[0.1428]                     , label="chance"        , markevery=2, linewidth=3, color='k',linestyle=':')

plt.xlabel('Iterations')
plt.ylabel('Accuracy')
plt.ylim([0,0.8])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
plt.text(.12, .05, 'Image Classification', horizontalalignment='left', verticalalignment='bottom')
plt.text(.12, .01, 'Square Random Matrices', horizontalalignment='left', verticalalignment='bottom')
plt.savefig(options['output_path']+'accuracy_rand_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')



# plot subject specific prediciton accuracy
#plt.figure()
#plt.plot(iter_range ,acc_pHA_EM_all[0,:], marker = 'x', markevery=2, label = str(0))
#plt.plot(iter_range ,acc_pHA_EM_all[1,:], marker = 'x', markevery=2, label = str(1))
#plt.plot(iter_range ,acc_pHA_EM_all[2,:], marker = 'x', markevery=2, label = str(2))
#plt.plot(iter_range ,acc_pHA_EM_all[3,:], marker = 'x', markevery=3, label = str(3))
#plt.plot(iter_range ,acc_pHA_EM_all[4,:], marker = 'x', markevery=3, label = str(4))
#plt.plot(iter_range ,acc_pHA_EM_all[5,:], marker = 'x', markevery=2, label = str(5))
#plt.plot(iter_range ,acc_pHA_EM_all[6,:], marker = 'x', markevery=3, label = str(6))
#plt.plot(iter_range ,acc_pHA_EM_all[7,:], marker = 'o', markevery=2, label = str(7))
#plt.plot(iter_range ,acc_pHA_EM_all[8,:], marker = 'o', markevery=3, label = str(8))
#plt.plot(iter_range ,acc_pHA_EM_all[9,:], marker = 'o', markevery=3, label = str(9))
#plt.xlabel('Iteartions')
#plt.ylabel('Accuracy')
#plt.ylim([0,0.8])
#plt.legend(loc=4)
#plt.savefig(options['output_path']+'pHAEM_allsubj_accuracy_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000)

