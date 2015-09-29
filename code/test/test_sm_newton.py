#!/usr/bin/env python

# Hyperalignment on Stiefel Manifold with newton method
# Edelman et. at. 1998 The Geometry og Algorithms with Orthogonality Constraints

# movie_data is a three dimensional matrix of size voxel x TR x nsubjs
# movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
# mathematic notation

import numpy as np, scipy, random, sys, math, os
from scipy import stats

def stiefgeod(W,Z):
  n   = W.shape[0]
  f   = W.shape[1]

  A   = W.T.dot(Z)
  A   = (A - A.T)/2
  Q,R = np.linalg.qr( Z - W.dot(A) )
  Top = np.concatenate( (A, -R.T) ,axis = 1)
  Down= np.concatenate( (R, np.zeros((f,f)) ), axis = 1)
  MN_tmp = scipy.linalg.expm( np.concatenate( (Top,Down), axis = 0) )
  MN = MN_tmp[:,range(f)]
  W_new = W.dot(MN[range(f),:]) + Q.dot(MN[range(f,2*f),:])
  return W_new

def stiefCanIP(W,X,G):
  n   = W.shape[0]
  f   = W.shape[1]
  ip = np.trace(X.T.dot(np.identity(n)-0.5*W.dot(W.T)).dot(G))
  return ip

def newton_step(W, X, G):
  n   = W.shape[0]
  f   = W.shape[1]
  eps = 0.001

  XTX = X.T.dot(X)
  DW  = XTX.dot(W) - X.T.dot(G)
  WDW = W.T.dot(DW)
  Fw   = DW - W.dot(WDW.T)

  dim = f*(f-1)/2 + f*(n-f)
  # use linear conjugate gradient to find the newton step 
  Z  = np.zeros(W.shape)
  R1 = -Fw
  P  = R1
  P0 = np.zeros(W.shape)

  for k in range(dim):
    normR1 = math.sqrt(stiefCanIP(W,R1,R1))
    if normR1 < n*f*eps: break
    if k == 0 : 
      beta = 0
    else :
      beta = (normR1/normR0)**2
    P0 = P
    P  = R1 + beta*P
    DWP= DW.T.dot(P)
    WTP= W.T.dot(P)
    LP = XTX.dot(P) - W.dot(P.T).dot(XTX).dot(W) - W.dot((DWP-DWP.T)/2) - (P.dot(WDW.T)-DW.dot(WTP.T))/2 -(P-W.dot(WTP)).dot(WDW/2)
    
    alpha = normR1**2/stiefCanIP(W,P,LP)
    Z = Z + alpha*P
    R0 = R1
    normR0 = normR1
    R1 = R1-alpha*LP

  return Z

def test_SM_Newton():
  nvoxel   = 5
  nfeature = 3
  nTR      = 5
  eps      = 0.001

  X = np.mat(np.random.random((nTR,nvoxel)))

  A = np.mat(np.random.random((nvoxel,nvoxel)))
  Q, R_qr = np.linalg.qr(A)
  W0 = Q[:,range(nfeature)]
  print '---W0---'
  print W0

  #W0 = np.zeros((nvoxel, nfeature))
  for i in range(nfeature):
    W0[i,i] = 1
  G = X.dot(W0)

  Z = 0.1*np.mat(np.random.random((nvoxel,nfeature)))
  Z = Z - W0.dot(Z.T.dot(W0))

  W = stiefgeod(W0,Z)

  d = np.linalg.norm( W-W0 ,'fro')
  print d
  print W
  while d > math.sqrt(eps):
    W = stiefgeod(W, newton_step(W,X,G))
    d = np.linalg.norm( W-W0 ,'fro')
    print d
    print W



def HA_SM_Newton(movie_data, options, para, lrh):
  nvoxel = movie_data.shape[0]
  nTR    = movie_data.shape[1]
  nsubjs = movie_data.shape[2]
  align_algo = para['align_algo']
  nfeature   = para['nfeature']

  print align_algo,
  current_file = options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_current.npz' 

  movie_data_zscore = np.zeros ((nvoxel,nTR,nsubjs))
  for m in range(nsubjs):
    movie_data_zscore[:,:,m] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T

  if not os.path.exists(current_file):
    W = np.zeros((nvoxel,nfeature,nsubjs))
    G = np.zeros((nTR,nfeature))
    ran_seed = para['ranNum']
    random.seed(ran_seed)
    A = np.mat(np.random.random((nvoxel,nvoxel)))
    Q, R_qr = np.linalg.qr(A)
    for m in range(nsubjs):
      W[:,:,m] = Q[:,range(nfeature)]
      G = G + movie_data_zscore[:,:,m].T
    G = G/float(nsubjs)
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
    for m in range(nsubjs):
      #update W by moving it along geodesic with calculated tangent direction
      print('|'),
      W[:,:,m] = stiefgeod(W[:,:,m],newton_step(W[:,:,m],movie_data_zscore[:,:,m],G))
    G_new = np.zeros(G.shape)
    for m in range(nsubjs):
      G_new = G_new + movie_data_zscore[:,:,m].T.dot(W[:,:,m])
      G     = G_new/nsubjs

  new_niter = niter + para['niter_unit']
  np.savez_compressed(current_file, niter = new_niter)
  
  np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_'+str(new_niter)+'.npz',\
                      W = W, G = G, niter=new_niter)
  
  return new_niter
