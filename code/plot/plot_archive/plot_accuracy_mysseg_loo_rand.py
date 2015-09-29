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

rand_num = 5;

acc_HA_all = np.zeros((nsubjs*2, niter/niter_unit))
acc_HA_rand_all = np.zeros((nsubjs*2*rand_num, niter/niter_unit))
acc_pHA_EM_all = np.zeros((nsubjs*2, niter/niter_unit))
acc_pHA_EM_rand_all = np.zeros((nsubjs*2*rand_num, niter/niter_unit))


for i in range(1,niter/niter_unit):
  for m in range(nsubjs):
    ws_ha_mysseg_1st = np.load(options['working_path']+'acc_HA_mysseg_1st_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_ha_mysseg_2nd = np.load(options['working_path']+'acc_HA_mysseg_2nd_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_pha_em_mysseg_1st = np.load(options['working_path']+'acc_pHA_EM_mysseg_1st_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_pha_em_mysseg_2nd = np.load(options['working_path']+'acc_pHA_EM_mysseg_2nd_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')

    acc_HA_all[m,i]        = ws_ha_mysseg_1st['accu']
    acc_HA_all[nsubjs+m,i] = ws_ha_mysseg_2nd['accu']
    acc_pHA_EM_all[m,i]        = ws_pha_em_mysseg_1st['accu'] 
    acc_pHA_EM_all[nsubjs+m,i] = ws_pha_em_mysseg_2nd['accu'] 

    ws_ha_mysseg_1st.close()
    ws_ha_mysseg_2nd.close()
    ws_pha_em_mysseg_1st.close()
    ws_pha_em_mysseg_2nd.close()
  
    for rand in range(rand_num):
      ws_ha_rand_mysseg_1st = np.load(options['working_path']+'rand'+str(rand)+'/HA_rand_mysseg_1st_loo/'+'acc_HA_rand_mysseg_1st_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
      ws_ha_rand_mysseg_2nd = np.load(options['working_path']+'rand'+str(rand)+'/HA_rand_mysseg_2nd_loo/'+'acc_HA_rand_mysseg_2nd_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')

      ws_pha_em_rand_mysseg_1st = np.load(options['working_path']+'rand'+str(rand)+'/pHA_EM_rand_mysseg_1st_loo/'+'acc_pHA_EM_rand_mysseg_1st_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
      ws_pha_em_rand_mysseg_2nd = np.load(options['working_path']+'rand'+str(rand)+'/pHA_EM_rand_mysseg_2nd_loo/'+'acc_pHA_EM_rand_mysseg_2nd_loo'+str(m)+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')

      acc_HA_rand_all[m*2*rand_num+rand,i]          = ws_ha_rand_mysseg_1st['accu']
      acc_HA_rand_all[m*2*rand_num+rand_num+rand,i] = ws_ha_rand_mysseg_2nd['accu']

      acc_pHA_EM_rand_all[m*2*rand_num+rand,i]          = ws_pha_em_rand_mysseg_1st['accu'] 
      acc_pHA_EM_rand_all[m*2*rand_num+rand_num+rand,i] = ws_pha_em_rand_mysseg_2nd['accu'] 

      ws_ha_rand_mysseg_1st.close()
      ws_ha_rand_mysseg_2nd.close()
      ws_pha_em_rand_mysseg_1st.close()
      ws_pha_em_rand_mysseg_2nd.close()

ws_none_mysseg_1st = np.load(options['working_path']+'acc_None_mysseg_1st_'+str(para['nvoxel'])+'vx_0.npz')
ws_none_mysseg_2nd = np.load(options['working_path']+'acc_None_mysseg_2nd_'+str(para['nvoxel'])+'vx_0.npz')

acc_HA_all[0:nsubjs,0]        = ws_none_mysseg_1st['accu'] 
acc_HA_all[nsubjs:2*nsubjs,0] = ws_none_mysseg_2nd['accu'] 
acc_pHA_EM_all[0:nsubjs,0]        = ws_none_mysseg_1st['accu'] 
acc_pHA_EM_all[nsubjs:2*nsubjs,0] = ws_none_mysseg_2nd['accu']
  
for rand in range(rand_num):
  acc_HA_rand_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),0]         = ws_none_mysseg_1st['accu'] 
  acc_HA_rand_all[range((2*rand+1)*nsubjs,(2*rand+2)*nsubjs),0]     = ws_none_mysseg_2nd['accu'] 
  acc_pHA_EM_rand_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),0]     = ws_none_mysseg_1st['accu'] 
  acc_pHA_EM_rand_all[range((2*rand+1)*nsubjs,(2*rand+2)*nsubjs),0] = ws_none_mysseg_2nd['accu']

iter_range = range(niter/niter_unit)
acc_HA_mean = acc_HA_all.mean(axis = 0).tolist()
acc_HA_se   = acc_HA_all.std(axis = 0)/math.sqrt(2*nsubjs)
acc_HA_rand_mean = acc_HA_rand_all.mean(axis = 0).tolist()
acc_HA_rand_se   = acc_HA_rand_all.std(axis = 0)/math.sqrt(2*nsubjs)

acc_pHA_EM_mean = acc_pHA_EM_all.mean(axis = 0)
acc_pHA_EM_se   = acc_pHA_EM_all.std(axis = 0)/math.sqrt(2*nsubjs)
acc_pHA_EM_rand_mean = acc_pHA_EM_rand_all.mean(axis = 0)
acc_pHA_EM_rand_se   = acc_pHA_EM_rand_all.std(axis = 0)/math.sqrt(2*nsubjs)

acc_None_mean = acc_pHA_EM_mean[0]
acc_None_se   = acc_pHA_EM_se[0]

# set font size
font = {#'family' : 'normal',
        'size'   : 14}

plt.rc('font', **font)

aspectratio=8

# plot accuracy
plt.figure()
plt.errorbar(iter_range ,acc_HA_mean    ,acc_HA_se      , label="HA"      , markevery=2,linewidth=2, color='b', marker = 'o')
plt.errorbar(iter_range ,acc_pHA_EM_mean,acc_pHA_EM_se  , label="pHA EM"  , markevery=2, linewidth=2, color='r', marker = 'D',linestyle='--', markersize=7)
plt.errorbar(iter_range ,acc_HA_rand_mean    ,acc_HA_se      , label="HA rand"      , markevery=3,linewidth=1, color='c', marker = 'x')
plt.errorbar(iter_range ,acc_pHA_EM_rand_mean,acc_pHA_EM_se  , label="pHA EM rand" , markevery=3, linewidth=1, color='m', marker = 'x')
plt.errorbar(iter_range ,len(iter_range)*[acc_None_mean],\
                         len(iter_range)*[acc_None_se]  , label="no align", markevery=2, linewidth=2, color='g', marker = '.')
plt.plot    (iter_range ,len(iter_range)*[0.001]       , label="chance", markevery=2, linewidth=2, color='k',linestyle='--')
plt.xlabel('Iterations')
plt.ylabel('Accuracy')
plt.ylim([0,0.8])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
plt.savefig(options['output_path']+'accuracy_mysseg_rand_loo_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')

