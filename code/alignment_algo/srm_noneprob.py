#!/usr/bin/env python

# Inference code for non-probabilistic Shared Response Model

# A Reduced-Dimension fMRI Shared Response Model                                                                                       
# Po-Hsuan Chen, Janice Chen, Yaara Yeshurun-Dishon, Uri Hasson, James Haxby, Peter Ramadge                                            
# Advances in Neural Information Processing Systems (NIPS), 2015.

# movie_data is a three dimensional matrix of size voxel x TR x nsubjs
# movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
# mathematic notation

# By Cameron PH Chen @ Princeton 

import numpy as np, scipy, random, sys, math, os
from scipy import stats

def align(movie_data, options, args, lrh):
    print 'SRM None-Prob' + str(args.nfeature),
    sys.stdout.flush()
  
    nvoxel = movie_data.shape[0]
    nTR    = movie_data.shape[1]
    nsubjs = movie_data.shape[2]
    align_algo = args.align_algo
    nfeature = args.nfeature
    base_iter = 1
    current_file = options['working_path']+align_algo+'_'+lrh+'_current.npz' 
    #print current_file
  
    movie_data_zscore = np.zeros ((nvoxel,nTR,nsubjs))
    for m in range(nsubjs):
        movie_data_zscore[:,:,m] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T
  
    if not os.path.exists(current_file):
        R = np.zeros((nvoxel,nfeature,nsubjs))
        G = np.zeros((nTR,nfeature))
  
        #initialization
        if args.randseed != None:
            print 'randinit',
            np.random.seed(args.randseed)
            A = np.mat(np.random.random((nvoxel,nfeature)))
            Q, R_qr = np.linalg.qr(A)
        else:
            Q = np.identity(nvoxel)
  
        for m in range(nsubjs):
            R[:,:,m] = Q
            G = G + movie_data_zscore[:,:,m].T.dot(R[:,:,m])
        G = G/float(nsubjs)
  
        niter = 0
        np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(niter)+'.npz',\
                        R = R, G = G, niter=niter)
    else:
        workspace = np.load(current_file)
        niter = workspace['niter']
        workspace = np.load(options['working_path']+align_algo+'_'+lrh+'_'+str(niter)+'.npz')
        R = workspace['R']
        G = workspace['G']
        niter = workspace['niter']
  
    print str(niter+1)+'th',
    for i in range(base_iter+1):
        for m in range(nsubjs):
            print '.',
            sys.stdout.flush()
  
            G_tmp = G*nsubjs - movie_data_zscore[:,:,m].T.dot(R[:,:,m]) # G_tmp = G-XR
            G_tmp = G_tmp/float(nsubjs-1)
  
            sys.stdout.flush()
            Am = movie_data_zscore[:,:,m].dot(G_tmp)
            pert = np.zeros((Am.shape)) 
            np.fill_diagonal(pert,1)
            Um, sm, Vm = np.linalg.svd(Am+0.001*pert,full_matrices=False)
  
            R[:,:,m] = Um.dot(Vm) # R = UV^T
            G = G_tmp*(nsubjs-1) + movie_data_zscore[:,:,m].T.dot(R[:,:,m]) #G = G_tmp + XR
            G = G/float(nsubjs)
  
        for m in range(nsubjs):
            Am = movie_data_zscore[:,:,m].dot(G)
            pert = np.zeros((Am.shape))
            np.fill_diagonal(pert,1)
            Um, sm, Vm = np.linalg.svd(Am+0.001*pert, full_matrices=False) #USV = svd(X^TG)
            R[:,:,m] = Um.dot(Vm) # R = UV^T
  
  
    def obj_func(bX, bW, S):
        obj_val_tmp = 0
        for m in range(nsubjs):
            obj_val_tmp += np.linalg.norm(bX[:, :, m] - bW[:, :, m].dot(S), 'fro')
        print obj_val_tmp
        return obj_val_tmp
  
    new_niter = niter + 1
    np.savez_compressed(current_file, niter = new_niter)
    np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(new_niter)+'.npz',\
                        R = R, G = G, niter=new_niter)
    np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(new_niter)+'_obj.npz',\
                        obj = obj_func(movie_data_zscore, R, G.T))
    ## clean up results of previous iteration
    #os.remove(options['working_path']+align_algo+'_'+lrh+'_'+str(new_niter-1)+'.npz')
    return new_niter
