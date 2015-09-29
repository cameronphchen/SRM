#!/usr/bin/env python

# Regularized Hyperalignment (or Shrinkage CCA)

# movie_data is a three dimensional matrix of size voxel x TR x nsubjs
# movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
# mathematic notation

import numpy as np, scipy, random, sys, math, os
from scipy import stats

def RHA(movie_data, options, para, lrh):
  nvoxel = movie_data.shape[0]
  nTR    = movie_data.shape[1]
  nsubjs = movie_data.shape[2]
  align_algo = para['align_algo']
  alpha      = para['alpha'] 
  print align_algo,
  print alpha,
  current_file = options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_current.npz' 

  movie_data_zscore = np.zeros ((nvoxel,nTR,nsubjs))

  W = np.zeros((nvoxel,nvoxel,nsubjs))
  for m in range(nsubjs):
    movie_data_zscore[:,:,m] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T
    #Ux, Sx, Vx = np.linalg.svd(movie_data_zscore[:,:,m].T, full_matrices=False) #Ux*diag(Sx)*Vx = X
    Xdata = movie_data_zscore[:,:,m]
    Ltmp = np.linalg.cholesky(  (1-alpha)*Xdata.dot(Xdata.T)  + alpha*np.identity(Xdata.shape[0])  )
    #Ltmp_inv = scipy.linalg.inv(Ltmp)
    W[:,:,m] = scipy.linalg.inv(Ltmp)
    #W[:,:,m] = Vx.T.dot(Ltmp_inv).dot(Vx)
    movie_data_zscore[:,:,m] = W[:,:,m].T.dot(movie_data_zscore[:,:,m])
    #movie_data_zscore[:,:,m] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T 

  if not os.path.exists(current_file):
    R = np.zeros((nvoxel,nvoxel,nsubjs))
    G = np.zeros((nTR,nvoxel))
    for m in range(nsubjs):
      R[:,:,m] = np.identity(nvoxel)
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
    for m in range(nsubjs):
      R[:,:,m] = scipy.linalg.inv(W[:,:,m]).dot(R[:,:,m])
    G = workspace['G']
    niter = workspace['niter']

  print str(niter+1)+'th',
  for i in range(para['niter_unit']):
    print('.'),
    sys.stdout.flush()
    for m in range(nsubjs):
      G_tmp = G*nsubjs - movie_data_zscore[:,:,m].T.dot(R[:,:,m]) # G_tmp = G-XR
      U, s, V = np.linalg.svd(movie_data_zscore[:,:,m].dot(G)+0.001*np.eye(nvoxel), full_matrices=False) #USV = svd(X^TG)
      R[:,:,m] = U.dot(V) # R = UV^T
      G = G_tmp + movie_data_zscore[:,:,m].T.dot(R[:,:,m]) #G = G_tmp + XR
      G = G/nsubjs

  new_niter = niter + para['niter_unit']
  np.savez_compressed(current_file, niter = new_niter)
  
  for m in range(nsubjs):
    R[:,:,m] = W[:,:,m].dot(R[:,:,m])

  np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_'+str(new_niter)+'.npz',\
                      R = R, G = G, niter=new_niter)
  
  return new_niter
