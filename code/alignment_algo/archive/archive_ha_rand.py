#!/usr/bin/env python

# Standard Hyperalignment

# movie_data is a three dimensional matrix of size voxel x TR x nsubjs
# movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
# mathematic notation

# using random orthgonoal matrix to initialize the transformation matrix
# different from the heuristic way of using identity matrix
# however, every subject specific transformation matrices are intialized with
# the identical random transformation matrices

import numpy as np, scipy, random, sys, math, os
from scipy import stats

def HA_rand(movie_data, options, para, lrh):
  nvoxel = movie_data.shape[0]
  nTR    = movie_data.shape[1]
  nsubjs = movie_data.shape[2]
  align_algo = para['align_algo']

  print align_algo,
  current_file = options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_current.npz' 

  movie_data_zscore = np.zeros ((nvoxel,nTR,nsubjs))
  for m in range(nsubjs):
    movie_data_zscore[:,:,m] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T

  if not os.path.exists(current_file):
    R = np.zeros((nvoxel,nvoxel,nsubjs))
    G = np.zeros((nTR,nvoxel))
    ran_seed = para['ranNum']
    random.seed(ran_seed)
    A = np.mat(np.random.random((nvoxel,nvoxel)))
    Q, R_qr = np.linalg.qr(A)
    for m in range(nsubjs):
      R[:,:,m] = Q
      G = G + movie_data_zscore[:,:,m].T
    G = G/float(nsubjs)
    niter = 0
    np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_'+str(niter)+'.npz',\
                      R = R, G = G, niter=niter)
  else:
    workspace = np.load(current_file)
    niter = workspace['niter']
    workspace = np.load(options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_'+str(niter)+'.npz')
    R = workspace['R'] 
    G = workspace['G']
    niter = workspace['niter']

  print str(niter+1)+'th',
  for i in range(para['niter_unit']):
    print('.'),
    sys.stdout.flush()
    for m in range(nsubjs):
      G_tmp = G*nsubjs - movie_data_zscore[:,:,m].T.dot(R[:,:,m]) # G_tmp = G-XR
#      print movie_data_zscore[:,:,m].dot(G)
#      print np.amax(movie_data_zscore[:,:,m].dot(G))
#      print np.amin(movie_data_zscore[:,:,m].dot(G))
      U, s, V = np.linalg.svd(movie_data_zscore[:,:,m].dot(G)+0.001*np.eye(nvoxel), full_matrices=False) #USV = svd(X^TG)
#      U, s, V = np.linalg.svd(movie_data_zscore[:,:,m].dot(G), full_matrices=False) #USV = svd(X^TG)

      R[:,:,m] = U.dot(V) # R = UV^T
      G = G_tmp + movie_data_zscore[:,:,m].T.dot(R[:,:,m]) #G = G_tmp + XR
      G = G/nsubjs

  new_niter = niter + para['niter_unit']
  np.savez_compressed(current_file, niter = new_niter)
  
  np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_'+str(new_niter)+'.npz',\
                      R = R, G = G, niter=new_niter)
  
  return new_niter
