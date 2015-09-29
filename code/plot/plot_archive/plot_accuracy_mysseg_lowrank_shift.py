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

nfeature = [10,20,30,40,50,100,500,1000,1300]

acc_pHA_EM_lowrank_all = np.zeros((2*nsubjs, niter/niter_unit, len(nfeature)))
acc_pHA_EM_all = np.zeros((nsubjs*2, niter/niter_unit))

for i in range(1,niter/niter_unit):
  ws_pha_em_mysseg_1st = np.load(options['working_path']+'acc_pHA_EM_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
  ws_pha_em_mysseg_2nd = np.load(options['working_path']+'acc_pHA_EM_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
  acc_pHA_EM_all[0:nsubjs,i]        = ws_pha_em_mysseg_1st['accu'] 
  acc_pHA_EM_all[nsubjs:2*nsubjs,i] = ws_pha_em_mysseg_2nd['accu'] 
  ws_pha_em_mysseg_1st.close()
  ws_pha_em_mysseg_2nd.close()

  for k in range(len(nfeature)):
    ws_pha_em_lowrank_mysseg_1st = np.load(options['working_path']+ 'lowrank'+str(nfeature[k]) +'/pHA_EM_shift_lowrank_mysseg_1st'+\
                                '/acc_pHA_EM_shift_lowrank_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_pha_em_lowrank_mysseg_2nd = np.load(options['working_path']+ 'lowrank'+str(nfeature[k]) +'/pHA_EM_shift_lowrank_mysseg_2nd'+\
                                '/acc_pHA_EM_shift_lowrank_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    acc_pHA_EM_lowrank_all[range(0,nsubjs),i,k]     = ws_pha_em_lowrank_mysseg_1st['accu'] 
    acc_pHA_EM_lowrank_all[range(nsubjs,2*nsubjs),i,k] = ws_pha_em_lowrank_mysseg_2nd['accu'] 
    ws_pha_em_lowrank_mysseg_1st.close()
    ws_pha_em_lowrank_mysseg_2nd.close()

ws_none_mysseg_1st = np.load(options['working_path']+'acc_None_mysseg_1st_'+str(para['nvoxel'])+'vx_0.npz')
ws_none_mysseg_2nd = np.load(options['working_path']+'acc_None_mysseg_2nd_'+str(para['nvoxel'])+'vx_0.npz')

for k in range(len(nfeature)):
  acc_pHA_EM_lowrank_all[0:nsubjs,0,k]        = ws_none_mysseg_1st['accu'] 
  acc_pHA_EM_lowrank_all[nsubjs:2*nsubjs,0,k] = ws_none_mysseg_2nd['accu']

acc_pHA_EM_all[0:nsubjs,0]        = ws_none_mysseg_1st['accu'] 
acc_pHA_EM_all[nsubjs:2*nsubjs,0] = ws_none_mysseg_2nd['accu'] 

iter_range = range(niter/niter_unit)

acc_pHA_EM_mean = acc_pHA_EM_all.mean(axis = 0)
acc_pHA_EM_se   = acc_pHA_EM_all.std(axis = 0)/math.sqrt(nsubjs)

# set font size
font = {#'family' : 'normal',
        'size'   : 12}

plt.rc('font', **font)

aspectratio=10

# plot accuracy
plt.figure()
#sys.exit()

color_code = 'cbgkmycbgkmy'
marker_code ='......******'

plt.errorbar(iter_range ,len(iter_range)*[0.706],\
                         len(iter_range)*[0.026]          , label="Neuron HA"      , markevery=2, linewidth=2, color='k',linestyle='--')
plt.errorbar(iter_range ,acc_pHA_EM_mean,acc_pHA_EM_se  , label='pHA EM identity' , linewidth=2, color='r')
for k in range(len(nfeature)):
  acc_pHA_EM_lowrank_mean = acc_pHA_EM_lowrank_all[:,:,k].mean(axis = 0)
  acc_pHA_EM_lowrank_se   = acc_pHA_EM_lowrank_all[:,:,k].std(axis = 0)/math.sqrt(nsubjs)
  plt.errorbar(iter_range ,acc_pHA_EM_lowrank_mean,acc_pHA_EM_lowrank_se  , label='pHA EM '+str(nfeature[k]),markevery=1, markersize=4, linewidth=1, color=color_code[k], marker=marker_code[k])
plt.xlabel('Iterations')
plt.ylabel('Accuracy')
plt.ylim([0,0.9])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
plt.text(.12, .05, 'Movie Segment Classification', horizontalalignment='left', verticalalignment='bottom')
plt.text(.12, .01, 'Skinny Shift Matrices', horizontalalignment='left', verticalalignment='bottom')
plt.savefig(options['output_path']+'accuracy_mysseg_shift_lowrank_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')

