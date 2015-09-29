#!/usr/bin/env python

# EM algorithm for probabilistic Hyperalignment

# movie_data is a three dimensional matrix of size voxel x TR x nsubjs
# movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
# mathematic notation

# E-step:
# E_s   : nvoxel x nTR
# E_sst : nvoexl x nvoxel x nTR
# M-step:
# W_m   : nvoxel x nvoxel x nsubjs
# sigma_m2 : nsubjs 
# Sig_s : nvoxel x nvoxel 

import numpy as np, scipy, random, sys, math, os
from scipy import stats

def align(movie_data, options, para, lrh):

  nvoxel = movie_data.shape[0]
  nTR    = movie_data.shape[1]
  nsubjs = movie_data.shape[2]

  nfeature   = para['nfeature']
  ran_seed = para['ranNum']
  align_algo = para['align_algo']

  if not os.path.exists(options['working_path']):
    os.makedirs(options['working_path'])

  current_file = options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_current.npz'
  # zscore the data
  bX = np.zeros((nsubjs*nvoxel,nTR))
  for m in range(nsubjs):
    bX[m*nvoxel:(m+1)*nvoxel,:] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T

  del movie_data

  # initialization when first time run the algorithm
  if not os.path.exists(current_file):
    bSig_s = np.identity(nfeature)
    bW     = np.zeros((nsubjs*nvoxel,nfeature))
    bmu    = np.zeros(nvoxel*nsubjs)
    sigma2  = np.zeros(nsubjs)
    ES     = np.zeros((nfeature,nTR)) 
    np.random.seed(ran_seed)
    A = np.mat(np.random.random((nvoxel,nfeature)))
    Q, R_qr = np.linalg.qr(A)
    for m in range(nsubjs):
      bW[m*nvoxel:(m+1)*nvoxel,:] = Q 
      bmu[m*nvoxel:(m+1)*nvoxel] = np.mean(bX[m*nvoxel:(m+1)*nvoxel,:],1)
      sigma2[m] = 1
    niter = 0
    np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(para['nvoxel'])+'vx_'+str(niter)+'.npz',\
                      bSig_s = bSig_s, bW = bW, bmu=bmu, sigma2=sigma2, ES=ES, niter=niter)

  # more iterations starts from previous results
  else:
    workspace = np.load(current_file)
    niter = workspace['niter']
    workspace = np.load(options['working_path']+align_algo+'_'+lrh+'_'+str(para['nvoxel'])+'vx_'+str(niter)+'.npz')
    bSig_s = workspace['bSig_s'] 
    bW     = workspace['bW']
    bmu    = workspace['bmu']
    sigma2 = workspace['sigma2']
    ES     = workspace['ES']
    niter  = workspace['niter']

  # remove mean
  bX = bX - bX.mean(axis=1)[:,np.newaxis]

  print str(niter+1)+'th',
  for i in range(para['niter_unit']):
    print('.'),
    sys.stdout.flush()

    bSig_x = np.zeros((nvoxel*nsubjs,nvoxel*nsubjs))
    bSig_x = bW.dot(bSig_s).dot(bW.T)
    for m in range(nsubjs):
      print('-'),
      sys.stdout.flush()
      bSig_x[m*nvoxel:(m+1)*nvoxel,m*nvoxel:(m+1)*nvoxel] += sigma2[m]*np.identity(nvoxel)

    inv_bSig_x = scipy.linalg.inv(bSig_x)
    ES = bSig_s.T.dot(bW.T).dot(inv_bSig_x).dot(bX)
    bSig_s = bSig_s - bSig_s.T.dot(bW.T).dot(inv_bSig_x).dot(bW).dot(bSig_s) + ES.dot(ES.T)/float(nTR)

    for m in range(nsubjs):
      print('-'),
      sys.stdout.flush()
      Am = bX[m*nvoxel:(m+1)*nvoxel,:].dot(ES.T)
      Um, sm, Vm = np.linalg.svd(Am,full_matrices=0)
      bW[m*nvoxel:(m+1)*nvoxel,:] = Um.dot(Vm)
      sigma2[m] =    np.trace(bX[m*nvoxel:(m+1)*nvoxel,:].T.dot(bX[m*nvoxel:(m+1)*nvoxel,:]))\
                  -2*np.trace(bX[m*nvoxel:(m+1)*nvoxel,:].T.dot(bW[m*nvoxel:(m+1)*nvoxel,:]).dot(ES))\
                +nTR*np.trace(bSig_s)
      sigma2[m] = sigma2[m]/float(nTR*nvoxel)

  new_niter = niter + para['niter_unit']
  np.savez_compressed(current_file, niter = new_niter)  
  np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_'+str(new_niter)+'.npz',\
                      bSig_s = bSig_s, bW = bW, bmu=bmu, sigma2=sigma2, ES=ES, niter=new_niter)
  
  # calculate log likelihood
  sign , logdet = np.linalg.slogdet(bSig_x)
  if sign == -1:
    print str(new_niter)+'th iteration, log sign negative'

  loglike = - 0.5*nTR*logdet - 0.5*np.trace(bX.T.dot(inv_bSig_x).dot(bX)) #-0.5*nTR*nvoxel*nsubjs*math.log(2*math.pi)

  np.savez_compressed(options['output_path']+align_algo+'_'+'loglikelihood_'+lrh+'_'+str(nvoxel)+'vx_'+str(new_niter)+'.npz',\
                   loglike=loglike)

#  print str(-0.5*nTR*logdet)+','+str(-0.5*np.trace(bX.T.dot(inv_bSig_x).dot(bX)))
#  print str(loglike) 







  return new_niter
