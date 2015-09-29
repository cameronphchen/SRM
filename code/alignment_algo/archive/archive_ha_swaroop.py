#!/usr/bin/env python

# Standard Hyperalignment

# movie_data is a three dimensional matrix of size voxel x TR x nsubjs
# movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
# mathematic notation

import numpy as np, scipy, random, sys, math, os
from scipy import stats

def align(movie_data, options, para, lrh):

  nvoxel = para['nvoxel']
  nsubjs = para['nsubjs']
  nTR    = para['nTR']  

  current_file = options['working_path']+'HA_'+lrh+'_'+str(para['nvoxel'])+'vx_current.npz' 

  movie_data_zscore = np.zeros ((nvoxel,nTR,nsubjs))
  for m in range(para['nsubjs']):
    movie_data_zscore[:,:,m] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T
  
  if not os.path.exists(current_file):
    R = np.zeros((para['nvoxel'],para['nvoxel'],para['nsubjs']))
    G = np.zeros((para['nTR'],para['nvoxel']))
    for m in range(para['nsubjs']):
      R[:,:,m] = np.identity(para['nvoxel'])
    G = movie_data_zscore[:,:,1].T
    niter = 0
    np.savez_compressed(options['working_path']+'HA_'+lrh+'_'+str(para['nvoxel'])+'vx_'+str(niter)+'.npz',\
                      R = R, G = G, niter=niter)
  else:
    workspace = np.load(current_file)
    niter = workspace['niter']
    workspace = np.load(options['working_path']+'HA_'+lrh+'_'+str(para['nvoxel'])+'vx_'+str(niter)+'.npz')
    R = workspace['R'] 
    G = workspace['G']
    niter = workspace['niter']

  print str(niter+1)+'th',
  for i in range(0,para['niter_unit']):
    print('.'),
    sys.stdout.flush()
    for m in range(para['nsubjs']):
      U, s, V = np.linalg.svd(movie_data_zscore[:,:,m].dot(G), full_matrices=False) #USV^T = svd(X^TG)
      R[:,:,m] = U.dot(V) # R = UV^T
      G = (G + stats.zscore(movie_data_zscore[:,:,m].T.dot(R[:,:,m]),axis=1, ddof=0) )/2 
      G = stats.zscore(G ,axis=1, ddof=0)

  new_niter = niter + para['niter_unit']
  np.savez_compressed(current_file, niter = new_niter)
  
  np.savez_compressed(options['working_path']+'HA_'+lrh+'_'+str(para['nvoxel'])+'vx_'+str(new_niter)+'.npz',\
                      R = R, G = G, niter=new_niter)
  
  return new_niter
