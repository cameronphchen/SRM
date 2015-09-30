#!/usr/bin/env python

# Standard Hyperalignment

# movie_data is a three dimensional matrix of size voxel x TR x nsubjs
# movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
# mathematic notation

import numpy as np, scipy, random, sys, math, os
from scipy import stats
sys.path.append('/jukebox/ramadge/pohsuan/scikit-learn/sklearn')
from sklearn import linear_model



def align(movie_data, options, args, lrh):
  print 'HA syn L1' + str(args.nfeature),
  sys.stdout.flush()


  alpha = 0.001
  print 'alpha:{}'.format(alpha)
  nvoxel = movie_data.shape[0]
  nTR    = movie_data.shape[1]
  nsubjs = movie_data.shape[2]
  align_algo = args.align_algo
  nfeature = args.nfeature
  base_iter = 1
  current_file = options['working_path']+align_algo+'_'+lrh+'_current.npz' 
  #print current_file

  X = np.zeros((nsubjs*nvoxel,nTR))
  for m in range(nsubjs):
      X[m*nvoxel:(m+1)*nvoxel,:] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T

  if not os.path.exists(current_file):
      bW     = np.zeros((nsubjs*nvoxel,nfeature))
      ES     = np.zeros((nfeature,nTR))

      #initialization
      if args.randseed != None:
          print 'randinit',
          np.random.seed(args.randseed)
          A = np.mat(np.random.random((nvoxel,nfeature)))
          Q, R_qr = np.linalg.qr(A)
      else:
          Q = np.identity(nvoxel)

      for m in range(nsubjs):
          bW[m*nvoxel:(m+1)*nvoxel,:] = Q 
          
      S = bW.T.dot(X)/float(nsubjs)

      niter = 0
      np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(niter)+'.npz',\
                      bW = bW, ES = ES, niter=niter)
  else:
      workspace = np.load(current_file)
      niter = workspace['niter']
      workspace = np.load(options['working_path']+align_algo+'_'+lrh+'_'+str(niter)+'.npz')
      bW = workspace['bW']
      ES = workspace['ES']
      niter = workspace['niter']

  clf = linear_model.Lasso(alpha=alpha)
  
  print str(niter+1)+'th',
  for i in range(base_iter):
      clf.fit(bW,X)
      ES = clf.coef_.T
      print 'avg nonzero:{}'.format(len(np.nonzero(ES))/float(ES.shape[1]))
      for m in range(nsubjs):
          print '.',
          sys.stdout.flush()

          sys.stdout.flush()
          Am = X[m*nvoxel:(m+1)*nvoxel,:].dot(ES.T)
          pert = np.zeros((Am.shape)) 
          np.fill_diagonal(pert,1)
          Um, sm, Vm = np.linalg.svd(Am+0.001*pert,full_matrices=False)

          bW[m*nvoxel:(m+1)*nvoxel,:] = Um.dot(Vm) # R = UV^T

  new_niter = niter + 1
  np.savez_compressed(current_file, niter = new_niter)
  np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(new_niter)+'.npz',\
                      bW = bW, ES = ES, niter=new_niter)
  #os.remove(options['working_path']+align_algo+'_'+lrh+'_'+str(new_niter-1)+'.npz')
  return new_niter
