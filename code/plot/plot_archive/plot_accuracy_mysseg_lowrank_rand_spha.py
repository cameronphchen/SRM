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
# local options
#options = {'input_path'  : '/Volumes/ramadge/pohsuan/pHA/data/input/', \
#           'working_path': '/Volumes/ramadge/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
#           'output_path' : '/Volumes/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

nfeature = [10,50,100]

acc_spHA_VI_all = np.zeros((2*nsubjs*nrand, niter/niter_unit, len(nfeature)))

for i in range(1,niter/niter_unit):

  for k in range(len(nfeature)):
    for rand in range(nrand):
      ws_spha_vi_mysseg_1st = np.load(options['working_path'] +'winsize' +str(win_size)+ '/lowrank'+str(nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_1st'+\
                                  '/acc_spHA_VI_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
      ws_spha_vi_mysseg_2nd = np.load(options['working_path'] +'winsize' +str(win_size)+'/lowrank'+str(nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_2nd'+\
                                  '/acc_spHA_VI_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
      acc_spHA_VI_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),i,k]     = ws_spha_vi_mysseg_1st['accu'] 
      acc_spHA_VI_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),i,k] = ws_spha_vi_mysseg_2nd['accu'] 
      ws_spha_vi_mysseg_1st.close()
      ws_spha_vi_mysseg_2nd.close()

ws_none_mysseg_1st = np.load(options['working_path']+'acc_None_mysseg_1st_'+str(para['nvoxel'])+'vx_0.npz')
ws_none_mysseg_2nd = np.load(options['working_path']+'acc_None_mysseg_2nd_'+str(para['nvoxel'])+'vx_0.npz')

for k in range(len(nfeature)):
  for rand in range(nrand):
    acc_spHA_VI_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),0,k]     = ws_none_mysseg_1st['accu'] 
    acc_spHA_VI_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),0,k] = ws_none_mysseg_2nd['accu']

iter_range = range(niter/niter_unit)


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
    len(iter_range)*[0.026]          , label="Neuron HA"      , markevery=2, linewidth=2, color='k',linestyle='--')
for k in range(len(nfeature)):
  acc_spHA_VI_mean = acc_spHA_VI_all[:,:,k].mean(axis = 0)
  acc_spHA_VI_se   = acc_spHA_VI_all[:,:,k].std(axis = 0)/math.sqrt(nsubjs)
  plt.errorbar(iter_range ,acc_spHA_VI_mean,acc_spHA_VI_se  , label='spHA VI '+str(nfeature[k]) ,markevery=1, markersize=4, linewidth=1, color=color_code[k], marker=marker_code[k])
plt.xlabel('Iterations')
plt.ylabel('Accuracy')
plt.ylim([0,0.9])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
plt.text(.12, .09, 'Movie Segment Classification TR', horizontalalignment='left', verticalalignment='bottom')
plt.text(.12, .05, 'Skinny Random Matrices', horizontalalignment='left', verticalalignment='bottom')
plt.text(.12, .015, 'RBFard kernel', horizontalalignment='left', verticalalignment='bottom')
plt.savefig(options['output_path']+'accuracy_mysseg_'+str(win_size)+'TR_spha_vi_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')

