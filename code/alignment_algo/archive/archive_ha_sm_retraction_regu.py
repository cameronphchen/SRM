#!/usr/bin/env python

# Hyperalignment on Stiefel Manifold with retraction method


# movie_data is a three dimensional matrix of size voxel x TR x nsubjs
# movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
# mathematic notation

import numpy as np, scipy, random, sys, math, os
from scipy import stats
from line_search_local import line_search_wolfe2
#from scipy.optimize import line_search

def retraction(W, X, G):
  n   = W.shape[0]
  f   = W.shape[1]
  XTX = X.T.dot(X)
  DW  = XTX.dot(W) - X.T.dot(G)
  P = DW.dot(W.T) - W.dot(DW.T)

  def Y(tau1):
    ANS = np.linalg.inv(np.identity(n) + 0.5*tau1*P).dot(np.identity(n) - 0.5*tau1*P).dot(W)
    return ANS
  def Y_prime(tau2):
    ANS2 = - np.linalg.inv(np.identity(n) + 0.5*tau2*P).dot(P).dot(0.5*(W+Y(tau2)))
    return ANS2
  def F(tau3):
    return np.linalg.norm( X.dot(Y(tau3))-G ,'fro')
  def F_prime(tau4):
    return np.trace(DW.T.dot(Y_prime(tau4))) 
  search_dir = 1e-4
  step       = 5e-6
  new_tau  = scipy.optimize.fmin(F, 0, disp = 0)
  print F(new_tau)-F(0)
  return Y(new_tau)

def HA_SM_Retraction_Regu(movie_data, options, para, lrh):
  nvoxel = movie_data.shape[0]
  nTR    = movie_data.shape[1]
  nsubjs = movie_data.shape[2]
  align_algo = para['align_algo']
  nfeature   = para['nfeature']
  gamma      = para['gamma']

#  print align_algo,
  current_file = options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_current.npz' 
  #print current_file

  movie_data_zscore = np.zeros ((nvoxel,nTR,nsubjs))
  for m in range(nsubjs):
    movie_data_zscore[:,:,m] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T

  if not os.path.exists(current_file):
    W = np.zeros((nvoxel,nfeature,nsubjs))
    G = np.zeros((nTR,nfeature))
    ran_seed = para['ranNum']
    np.random.seed(ran_seed)
    A = np.mat(np.random.random((nvoxel,nfeature)))
    Q, R_qr = np.linalg.qr(A)
    for m in range(nsubjs):
      W[:,:,m] = Q
      G = G + movie_data_zscore[:,:,m].T.dot(W[:,:,m])
    G = G/float(nsubjs+gamma)
    niter = 0
    np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_'+str(niter)+'.npz',\
                      W = W, G = G, niter=niter)
  else:
    workspace = np.load(current_file)
    niter = workspace['niter']
    workspace = np.load(options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_'+str(niter)+'.npz')
    W = workspace['W'] 
    G = workspace['G']
    niter = workspace['niter']

  print str(niter+1)+'th',
  for i in range(para['niter_unit']):
    print('.'),
    sys.stdout.flush()
    r = 0
    for m in range(nsubjs):
      r += np.linalg.norm( movie_data_zscore[:,:,m].T.dot(W[:,:,m])-G ,'fro') 
    print 'obj value:'+str(r)
    for m in range(nsubjs):
      print(m),
#      W_tmp = retraction(W[:,:,m],movie_data_zscore[:,:,m].T,G)
#      W[:,:,m] = W_tmp
      Am = movie_data_zscore[:,:,m].dot(G)
      Um, sm, Vm = np.linalg.svd(Am,full_matrices=0)
      W[:,:,m] = -1*Um.dot(Vm)
    G_new = np.zeros(G.shape)
    for m in range(nsubjs):
      G_new = G_new + movie_data_zscore[:,:,m].T.dot(W[:,:,m])
      G     = G_new/float(nsubjs+gamma)
  
  new_niter = niter + para['niter_unit']
  np.savez_compressed(current_file, niter = new_niter)
  np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_'+str(new_niter)+'.npz',\
                      W = W, G = G, niter=new_niter)
  
  return new_niter
