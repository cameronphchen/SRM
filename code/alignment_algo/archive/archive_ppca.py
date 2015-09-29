#!/usr/bin/env python

# using pPCA for multisubject fMRI data alignment

#movie_data is a three dimensional matrix of size voxel x TR x nsubjs
#movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
#mathematic notation

# prior
# bK_i  : TR x TR

# Variational Parameters:
# mu_s  : nvoxel x TR
# Sig_s : TR x TR x nvoxel

# Hyperparameters:
# W_m   : nvoxel x nfeature x nsubjs
# rho2  : nsubjs 
# mu    : nvoxel*nsubj 

import numpy as np, scipy, random, sys, math, os
from scipy import stats
import sys
sys.path.append('/jukebox/ramadge/pohsuan/scikit-learn/sklearn')
from sklearn.decomposition import PCA

def align(movie_data, options, args, lrh):
    print 'pPCA(scikit-learn)'
    nvoxel = movie_data.shape[0]
    nTR    = movie_data.shape[1]
    nsubjs = movie_data.shape[2]

    align_algo = args.align_algo
    nfeature   = args.nfeature

    # zscore the data
    bX = np.nan((nsubjs*nvoxel,nTR))

    for m in xrange(nsubjs):
        bX[m*nvoxel:(m+1)*nvoxel,:] = stats.zscore(movie_data[:, :, m].T, axis=0, ddof=1).T
    del movie_data

    U, s, VT = np.linalg.svd(bX, full_matrices=False)

    bW = np.zeros((nsubjs*nvoxel,nfeature))
    for m in xrange(nsubjs):
        bW[m*nvoxel:(m+1)*nvoxel,:] = U[m*nvoxel:(m+1)*nvoxel,:nfeature]

    niter = 10
    # initialization when first time run the algorithm
    np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(niter)+'.npz',\
                                  bW = bW,  niter=niter)
    return niter
