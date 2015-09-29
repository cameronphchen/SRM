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
para  = {#'niter'     : int(sys.argv[1]),\
    'nvoxel'    : 1300,\
    'nTR'       : 2203,\
    'nrand'     : 5,\
    'win_size'  : 9,\
    'nsubjs'    : 10,\
    'niter_unit': 1 }

#niter      = para['niter']
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

nfeature = [1300]

#load movie data
movie_data_lh = scipy.io.loadmat(options['working_path']+'movie_data_lh_'+str(para['nvoxel'])+'vx.mat')
movie_data_rh = scipy.io.loadmat(options['working_path']+'movie_data_rh_'+str(para['nvoxel'])+'vx.mat')
movie_data_lh = movie_data_lh['movie_data_lh'] 
movie_data_rh = movie_data_rh['movie_data_rh'] 

movie_data_lh_1st = movie_data_lh[:,0:nTR/2,:]
movie_data_lh_2nd = movie_data_lh[:,(nTR/2+1):nTR,:]
movie_data_rh_1st = movie_data_rh[:,0:nTR/2,:]
movie_data_rh_2nd = movie_data_rh[:,(nTR/2+1):nTR,:]

movie_data_lh_1st_zscore = np.zeros((movie_data_lh_1st.shape))
movie_data_rh_1st_zscore = np.zeros((movie_data_rh_1st.shape))
movie_data_lh_2nd_zscore = np.zeros((movie_data_lh_2nd.shape))
movie_data_rh_2nd_zscore = np.zeros((movie_data_rh_2nd.shape))

for m in range(nsubjs):
  movie_data_lh_1st_zscore[:,:,m] = stats.zscore(movie_data_lh_1st[:,:,m].T ,axis=0, ddof=1).T
  movie_data_rh_1st_zscore[:,:,m] = stats.zscore(movie_data_rh_1st[:,:,m].T ,axis=0, ddof=1).T 
  movie_data_lh_2nd_zscore[:,:,m] = stats.zscore(movie_data_lh_2nd[:,:,m].T ,axis=0, ddof=1).T 
  movie_data_rh_2nd_zscore[:,:,m] = stats.zscore(movie_data_rh_2nd[:,:,m].T ,axis=0, ddof=1).T 

HA_Retr_range = 50;
pHA_range = 10;

obj_pHA       = np.zeros((2*nrand, pHA_range/niter_unit, len(nfeature)))
#obj_pHA       = np.zeros((2, pHA_range/niter_unit, len(nfeature)))
obj_HA_Retr   = np.zeros((2*nrand, HA_Retr_range/niter_unit, len(nfeature)))
#obj_HA_Retr   = np.zeros((2, HA_Retr_range/niter_unit, len(nfeature)))

# load HA_Retraction Results
for i in range(HA_Retr_range):
  print i,
  sys.stdout.flush()
  for k in range(len(nfeature)):
    for rand in range(nrand):
      HA_Retr_ws_lh = np.load(options['working_path']+'winsize9/'+'lowrank'+str(nfeature[k])+'/'+'rand'+str(rand)+'/' \
          +'HA_SM_Retraction_mysseg_1st_lh_1300vx_'+str(i)+'.npz')
      HA_Retr_ws_rh = np.load(options['working_path']+'winsize9/'+'lowrank'+str(nfeature[k])+'/'+'rand'+str(rand)+'/' \
          +'HA_SM_Retraction_mysseg_1st_rh_1300vx_'+str(i)+'.npz')
      bW_lh = HA_Retr_ws_lh['W']
      bW_rh = HA_Retr_ws_rh['W']
      HA_Retr_ws_lh.close()
      HA_Retr_ws_rh.close()
      for m in range(nsubjs):
        for n in range(m,nsubjs):
          obj_HA_Retr[rand,i,k] += np.linalg.norm(bW_lh[:,:,m].T.dot(movie_data_lh_1st_zscore[:,:,m]) - bW_lh[:,:,n].T.dot(movie_data_lh_1st_zscore[:,:,n]),'fro')
          obj_HA_Retr[nrand+rand,i,k] += np.linalg.norm(bW_rh[:,:,m].T.dot(movie_data_rh_1st_zscore[:,:,m]) - bW_rh[:,:,n].T.dot(movie_data_rh_1st_zscore[:,:,n]),'fro')

for i in range(pHA_range):
  print i,
  sys.stdout.flush()
  for k in range(len(nfeature)):
    for rand in range(nrand):
      pHA_ws_lh = np.load(options['working_path']+'winsize9/'+'lowrank'+str(nfeature[k])+'/'+'rand'+str(rand)+'/'+'pHA_EM_lowrank_mysseg_1st_lh_1300vx_'+str(i)+'.npz')
      pHA_ws_rh = np.load(options['working_path']+'winsize9/'+'lowrank'+str(nfeature[k])+'/'+'rand'+str(rand)+'/'+'pHA_EM_lowrank_mysseg_1st_rh_1300vx_'+str(i)+'.npz')

      transform_lh = np.zeros((nvoxel,nfeature[k],nsubjs))
      transform_rh = np.zeros((nvoxel,nfeature[k],nsubjs))
      bW_lh_pHA = pHA_ws_lh['bW']
      bW_rh_pHA = pHA_ws_rh['bW']
      pHA_ws_lh.close()
      pHA_ws_rh.close()
      for m in range(nsubjs):
        transform_lh[:,:,m] = bW_lh_pHA[m*nvoxel:(m+1)*nvoxel,:]
        transform_rh[:,:,m] = bW_rh_pHA[m*nvoxel:(m+1)*nvoxel,:]
      for m in range(nsubjs):
        for n in range(m,nsubjs):
          obj_pHA[rand,i,k] += np.linalg.norm(transform_lh[:,:,m].T.dot(movie_data_lh_1st_zscore[:,:,m]) - transform_lh[:,:,n].T.dot(movie_data_lh_1st_zscore[:,:,n]),'fro')
          obj_pHA[nrand+rand,i,k] += np.linalg.norm(transform_rh[:,:,m].T.dot(movie_data_rh_1st_zscore[:,:,m]) - transform_rh[:,:,n].T.dot(movie_data_rh_1st_zscore[:,:,n]),'fro')

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
for k in range(len(nfeature)):
  obj_HA_Retr_mean = obj_HA_Retr[:,:,k].mean(axis = 0)
  obj_HA_Retr_se   = obj_HA_Retr[:,:,k].std(axis = 0)/math.sqrt(nrand)
  plt.errorbar(range(HA_Retr_range) ,obj_HA_Retr_mean, obj_HA_Retr_se  , label='obj HA Retr '+str(nfeature[k]) ,\
               markevery=1, markersize=4, linewidth=1, color='b', marker=marker_code[k])
  obj_pHA_mean = obj_pHA[:,:,k].mean(axis = 0)
  obj_pHA_se   = obj_pHA[:,:,k].std(axis = 0)/math.sqrt(nsubjs)
  print obj_pHA_mean.shape
  print obj_pHA_se.shape
  plt.errorbar(range(pHA_range) ,obj_pHA_mean, obj_pHA_se  , label='obj pHA '+str(nfeature[k]) ,\
               markevery=1, markersize=4, linewidth=1, color='r', marker=marker_code[k])
plt.xlabel('Iterations')
plt.ylabel('Objective Value')
#plt.ylim([0,0.9])
#plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
#plt.text(.12, .09, 'Movie Segment Classification TR', horizontalalignment='left', verticalalignment='bottom')
#plt.text(.12, .05, 'Skinny Random Matrices', horizontalalignment='left', verticalalignment='bottom')
#plt.text(.12, .015, 'RBFard kernel', horizontalalignment='left', verticalalignment='bottom')
plt.savefig(options['output_path']+'objValue_mysseg_'+str(win_size)+'TR_spha_vi_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')

