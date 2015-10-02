#!/usr/bin/env python

# using PCA for multisubject fMRI data alignment

#movie_data is a three dimensional matrix of size voxel x TR x nsubjs
#movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
#mathematic notation

# do PCA on bX (nsubjs*nvoxel x nTR) concatenate the data vertically


import numpy as np, scipy, random, sys, math, os
from scipy import stats
import sys
sys.path.append('/jukebox/ramadge/pohsuan/scikit-learn/sklearn')
from sklearn.decomposition import PCA

def align(movie_data, options, args, lrh):
    print 'PCA(scikit-learn)'
    nvoxel = movie_data.shape[0]
    nTR    = movie_data.shape[1]
    nsubjs = movie_data.shape[2]
    
    align_algo = args.align_algo
    nfeature   = args.nfeature

    if not os.path.exists(options['working_path']):
        os.makedirs(options['working_path'])

    # zscore the data
    bX = np.zeros((nsubjs*nvoxel,nTR))
    for m in range(nsubjs):
        bX[m*nvoxel:(m+1)*nvoxel,:] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T
    del movie_data

    pert = np.zeros((bX.shape))
    np.fill_diagonal(pert,1,wrap=True)
    U, s, VT = np.linalg.svd(bX+0.001*pert, full_matrices=False)

    bW = U[:,range(nfeature)]
    ES = np.diag(s).dot(VT)
    ES = ES[:nfeature,:]

    R = np.zeros((nvoxel,nfeature,nsubjs))
    for m in range(nsubjs):
        R[:,:,m] = bW[m*nvoxel:(m+1)*nvoxel,:]

    niter = 10 
    # initialization when first time run the algorithm
    np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(niter)+'.npz',\
          R = R, G=ES.T, niter=niter)
    return niter
