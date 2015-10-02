#!/usr/bin/env python

import pprint
import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import scipy.io
import math
import pickle
import os

posthoc_matchup = True

def pHAc(movie_data, nfeature, W_init=None, randseed = None):
    nvoxel = movie_data.shape[0]
    nTR    = movie_data.shape[1]
    nsubjs = movie_data.shape[2]
    niter = 10  
    #print 'nfeature:{}'.format(nfeature),
    movie_data_zscore = np.zeros ((nvoxel,nTR,nsubjs))
  
    W = np.zeros((nvoxel,nfeature,nsubjs))
    S = np.zeros((nfeature,nTR))
    #initialization
    if W_init != None:
        #print 'warmstart',
        Q = W_init
    elif randseed != None:
        #print 'randinit',
        np.random.seed(randseed)
        A = np.mat(np.random.random((nvoxel,nfeature)))
        Q, W_qr = np.linalg.qr(A)
    else:
        #print 'identity',
        Q = np.identity(nvoxel)
  
    for m in range(nsubjs):
        W[:,:,m] = Q
        S = S + W[:,:,m].T.dot(movie_data[:,:,m])
    S = S/float(nsubjs)
  
                   
    for i in range(niter):
        #print i,
        for m in range(nsubjs):
            Am = movie_data[:,:,m].dot(S.T)
            pert = np.zeros((Am.shape))
            np.fill_diagonal(pert,1,wrap=True)
            Um, sm, Vm = np.linalg.svd(Am+pert,full_matrices=False)
            W[:,:,m] = Um.dot(Vm) # R = UV^T
  
        S = np.zeros((nfeature,nTR))      
        for m in range(nsubjs):
            S = S + W[:,:,m].T.dot(movie_data[:,:,m])
        S = S/float(nsubjs)
  
    return S,W



nrnd = 5
nsmooth = 7    
nfeat_list = [50,100,200,400,813]
align = np.zeros((nrnd*2,nsmooth))
pred = np.zeros((nrnd*2,nsmooth))
phac_align = np.zeros((nrnd*2,len(nfeat_list),nsmooth))
phac_pred = np.zeros((nrnd*2,len(nfeat_list),nsmooth))

for smooth_idx in [int(sys.argv[1])] :#range(nsmooth):
    for rnd_idx in [int(sys.argv[2])] :#range(nrnd):
        print 'sherlock_pmc_smooth{}_rnd{}_noLR_g1'.format(smooth_idx,rnd_idx)
        for align_idx in [1,2]:
            ws1 = scipy.io.loadmat('/jukebox/ramadge/pohsuan/pHA/data/input/sherlock_pmc_smooth{}_rnd{}_noLR_g1/813vx/1976TR/movie_data.mat'.format(smooth_idx,rnd_idx))
            g1_orig = ws1['movie_data']
            ws2 = scipy.io.loadmat('/jukebox/ramadge/pohsuan/pHA/data/input/sherlock_pmc_smooth{}_rnd{}_noLR_g2/813vx/1976TR/movie_data.mat'.format(smooth_idx,rnd_idx))
            g2_orig = ws2['movie_data']


            if align_idx == 1:
                g1_orig_align = g1_orig[:,:988,:]
                g2_orig_align = g2_orig[:,:988,:]    
                g1_orig_pred = g1_orig[:,988:,:]
                g2_orig_pred = g2_orig[:,988:,:]
            elif align_idx == 2:
                g1_orig_align = g1_orig[:,988:,:]
                g2_orig_align = g2_orig[:,988:,:]    
                g1_orig_pred = g1_orig[:,:988,:]
                g2_orig_pred = g2_orig[:,:988,:]
            else:
                print 'ERROR!!!!!'

            for m in range(g1_orig.shape[2]):
                g1_orig_align[:,:,m] = stats.zscore(g1_orig_align[:,:,m].T ,axis=0, ddof=1).T
                g2_orig_align[:,:,m] = stats.zscore(g2_orig_align[:,:,m].T ,axis=0, ddof=1).T
                g1_orig_pred[:,:,m] = stats.zscore(g1_orig_pred[:,:,m].T ,axis=0, ddof=1).T
                g2_orig_pred[:,:,m] = stats.zscore(g2_orig_pred[:,:,m].T ,axis=0, ddof=1).T 

            g1_avg_align = np.mean(g1_orig_align,axis=2)
            g2_avg_align = np.mean(g2_orig_align,axis=2)
            g1_avg_pred = np.mean(g1_orig_pred,axis=2)
            g2_avg_pred = np.mean(g2_orig_pred,axis=2)

            assert g1_avg_align.shape == (813,988)
            assert g2_avg_align.shape == (813,988)
            assert g1_avg_pred.shape == (813,988)
            assert g2_avg_pred.shape == (813,988)


            corrmat   = np.corrcoef(g1_avg_align,g2_avg_align, rowvar=0)[:988,988:]
            align[nrnd*(align_idx-1)+rnd_idx,smooth_idx] = np.mean(np.diag(corrmat))

            corrmat   = np.corrcoef(g1_avg_pred,g2_avg_pred, rowvar=0)[:988,988:]
            pred [nrnd*(align_idx-1)+rnd_idx,smooth_idx] = np.mean(np.diag(corrmat))

            for i,nfeat in enumerate(nfeat_list):
                print nfeat,
                rseed = 0
                S1,W1 = pHAc(g1_orig_align,nfeature = nfeat, randseed=rseed)
                S2,W2 = pHAc(g2_orig_align,nfeature = nfeat, randseed=rseed)

                if posthoc_matchup:
                    Am = S2.dot(S1.T)
                    pert = np.zeros((Am.shape)) 
                    np.fill_diagonal(pert,1)
                    Uq, sq, Vqt = np.linalg.svd(Am+0.001*pert,full_matrices=False)
                    Q = Uq.dot(Vqt)
                else:
                    Q = np.identity(nfeat)

                S1_postHA = np.zeros((nfeat,g1_orig_pred.shape[1]))
                S2_postHA = np.zeros((nfeat,g2_orig_pred.shape[1]))
                nsubjs = g1_orig_pred.shape[2]
                for m in range(nsubjs):
                    S1_postHA = S1_postHA + Q.dot(W1[:,:,m].T.dot(g1_orig_pred[:,:,m]))
                    S2_postHA = S2_postHA + W2[:,:,m].T.dot(g2_orig_pred[:,:,m])
                S1_postHA = S1_postHA/float(nsubjs)
                S2_postHA = S2_postHA/float(nsubjs)

                corrmat    = np.corrcoef(S1,S2, rowvar=0)[:S1.shape[1],S2.shape[1]:]
                phac_align[nrnd*(align_idx-1)+rnd_idx,i,smooth_idx] = np.mean(np.diag(corrmat))

                corrmat    = np.corrcoef(S1_postHA,S2_postHA, rowvar=0)[:S1_postHA.shape[1],S2_postHA.shape[1]:]
                phac_pred [nrnd*(align_idx-1)+rnd_idx,i,smooth_idx]  = np.mean(np.diag(corrmat))
if posthoc_matchup:
    np.savez_compressed('correlation_posthocmatchup_sherlock_pmc_smooth{}_rnd{}_noLR.npz'.format(smooth_idx,rnd_idx),align=align,pred=pred, phac_align = phac_align,phac_pred=phac_pred)
else:
    np.savez_compressed('correlation_sherlock_pmc_smooth{}_rnd{}_noLR.npz'.format(smooth_idx,rnd_idx),align=align,pred=pred, phac_align = phac_align,phac_pred=phac_pred)