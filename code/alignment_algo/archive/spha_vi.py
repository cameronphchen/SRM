#!/usr/bin/env python

#variational inference algorithm for semiparametric probabilistic Hyperalignment

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
sys.path.append('/jukebox/ramadge/pohsuan/pyGPs')
import pyGPs
import copy


def align(movie_data, options, args, lrh):
    print 'spHA_VI'
    nvoxel = movie_data.shape[0]
    nTR    = movie_data.shape[1]
    nsubjs = movie_data.shape[2]

    align_algo = args.align_algo
    nfeature   = args.nfeature

    current_file = options['working_path']+align_algo+'_'+lrh+'_current.npz'
    # zscore the data
    bX = np.zeros((nsubjs*nvoxel,nTR))
    for m in range(nsubjs):
        bX[m*nvoxel:(m+1)*nvoxel,:] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T

    del movie_data

    # prior
    #bK_i   = np.identity((nvoxel,nvoxel))

    kernel = pyGPs.cov.RBFard(1) ## remember to modify the kernel in optimization objective function
    #kernel = pyGPs.cov.SM(Q=50,D=1) ## remember to modify the kernel in optimization objective function
    #kernel = pyGPs.cov.RQ() ## remember to modify the kernel in optimization objective function

    T_idx = np.arange(nTR)
    T_idx = T_idx[:, None]

    np.random.seed(args.randseed)
    kernel.hyp = [np.random.random() for rr in range(len(kernel.hyp))]
    btheta = kernel.hyp
    bK_i = kernel.getCovMatrix(T_idx, T_idx, 'train')

    # initialization when first time run the algorithm
    if not os.path.exists(current_file):
        # variational parameters
        #          --bmu_{\bs_1}^T--
        # bmu_s =  --bmu_{\bs_n}^T--
        #          --bmu_{\bs_N}^T--
        ES = np.zeros((nfeature,nTR))

        # hyperparameters
        bW = np.zeros((nsubjs*nvoxel,nfeature))
        bmu = np.zeros(nvoxel*nsubjs)
        sigma2 = np.zeros(nsubjs)
        btheta = kernel.hyp

        # initialization
        if args.randseed != None:
            print 'randinit',
            np.random.seed(args.randseed)
            A = np.mat(np.random.random((nvoxel,nfeature)))
            Q, R_qr = np.linalg.qr(A)
        else:
            Q = np.identity(nvoxel)

        for m in range(nsubjs):
            bW[m*nvoxel:(m+1)*nvoxel,:] = Q
            bmu[m*nvoxel:(m+1)*nvoxel] = np.mean(bX[m*nvoxel:(m+1)*nvoxel,:],1)
            sigma2[m] = 1

        niter = 0
        np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(niter)+'.npz',\
                                    bW = bW, bmu=bmu, sigma2=sigma2, ES=ES, btheta = btheta , niter=niter)

    # more iterations starts from previous results
    else:
        workspace = np.load(current_file)
        niter = workspace['niter']
        workspace = np.load(options['working_path']+align_algo+'_'+lrh+'_'+str(niter)+'.npz')
        bW     = workspace['bW']
        bmu    = workspace['bmu']
        sigma2 = workspace['sigma2']
        ES     = workspace['ES']
        niter  = workspace['niter']
        btheta = workspace['btheta']
    # remove mean
    bX = bX - bX.mean(axis=1)[:,np.newaxis]

    pert = np.zeros((bK_i.shape))
    np.fill_diagonal(pert,1)

    print str(niter+1)+'th',
    tmp_sum_tr_Sig_si = 0
    Sig_si_sum = np.zeros((nTR,nTR))
    mumuT_sum  = np.zeros((nTR,nTR))
    tmp_log_det_Sigsi = 0
    for i in range(nfeature):
        print '.',
        sys.stdout.flush()

        tmp_sig_si = 0
        # calculate \bSig_{\bs_i}
        for m in range(nsubjs):
            tmp_sig_si += ( np.linalg.norm(bW[m*nvoxel:(m+1)*nvoxel,i])**2 )/sigma2[m]

        Sig_si =  scipy.linalg.inv( scipy.linalg.inv(bK_i+  0.001*pert) + tmp_sig_si*np.identity(nTR) )
        #tmp_log_det_Sigsi += math.log(np.linalg.det(Sig_si))
        sign , tmp_log_det_Sigsi = np.linalg.slogdet(Sig_si)
        if sign == -1:
          print str(it)+'th iteration, log sign negative'
        Sig_si_sum += Sig_si
        tmp_sum_tr_Sig_si += np.trace(Sig_si)
        # calculate \bmu_{\bs_i}
        tmp_sigma2WxWE = np.zeros((nTR,1))
        for m in xrange(nsubjs):
            tmp_WxWE = np.zeros((nTR,1))
            for k in xrange(nvoxel):
                tmp_WmkjEsj = np.zeros((nTR,1))
                for j in xrange(nfeature):
                    if j == i: continue
                    tmp_WEST = bW[m*nvoxel+k,j]*ES[j,:].T
                    tmp_WEST = tmp_WEST[:,None]
                    tmp_WmkjEsj += tmp_WEST
                tmp_bX_k = bX[m*nvoxel+k,:].T
                tmp_bX_k = tmp_bX_k[:,None]
                tmp_WxWE += bW[m*nvoxel+k,i]*( tmp_bX_k- tmp_WmkjEsj)
            tmp_sigma2WxWE += tmp_WxWE/sigma2[m]
        ES[i,:]   = (Sig_si.dot(tmp_sigma2WxWE)).T
        mumuT_sum += np.outer(ES[i,:],ES[i,:])

    for m in range(nsubjs):
        Am = bX[m*nvoxel:(m+1)*nvoxel,:].dot(ES.T)
        Um, sm, Vm = np.linalg.svd(Am, full_matrices=False)

        bW[m*nvoxel:(m+1)*nvoxel,:] = Um.dot(Vm)
        tmp_sigma2 =   np.trace(bX[m*nvoxel:(m+1)*nvoxel,:].T.dot(bX[m*nvoxel:(m+1)*nvoxel,:])) \
                      -2*np.trace(ES.T.dot(bW[m*nvoxel:(m+1)*nvoxel,:].T).dot(bX[m*nvoxel:(m+1)*nvoxel,:]))\
                      +np.trace(ES.dot(ES.T)) + tmp_sum_tr_Sig_si
        sigma2[m] = nTR / tmp_sigma2

    # hyperparameter optimization TODO whether there's any bug

    def obj_func(btheta_opt): # ", kernel_opt):
        kernel_opt = pyGPs.cov.RBFard(1)
        kernel_opt.hyp = btheta_opt
        bK_i_opt = kernel_opt.getCovMatrix(T_idx, T_idx, 'train')
        bK_i_opt_inv = scipy.linalg.inv(bK_i_opt+0.001*pert)
        sign_opt , logdet_opt = np.linalg.slogdet(bK_i_opt)
        return 0.5*nfeature*sign_opt*logdet_opt + 0.5*np.trace(bK_i_opt_inv.dot(mumuT_sum+Sig_si_sum))

    def obj_func_der(btheta_opt):
        kernel_opt = pyGPs.cov.RBFard(1);
        kernel_opt.hyp = btheta_opt;
        bK_i_opt   = kernel_opt.getCovMatrix(T_idx,T_idx,'train')
        bK_i_opt_inv = scipy.linalg.inv(bK_i_opt)
        sign_opt , logdet_opt = np.linalg.slogdet(bK_i_opt)
        return 0.5*np.trace(bK_i_opt_inv.dot(bK_i_opt + mumuT_sum - Sig_si_sum).dot(bK_i_opt_inv)\
                            .dot( kernel.getDerMatrix(T_idx,T_idx,'train')))

    # btheta = scipy.optimize.minimize(obj_func, btheta)
    # maximize elbo == minimize -elbo
    # btheta = scipy.optimize.fmin(obj_func,btheta , (copy.deepcopy(kernel),), maxiter=10)
    btheta = scipy.optimize.fmin(obj_func, btheta, maxiter=10)
    print btheta,

    #### original error code
    #for l in range(len(btheta)):
    #  btheta[l]+=-0.5*np.trace(bK_i_inv.dot(bK_i + mumuT_sum - Sig_si_sum).dot(bK_i_inv)\
    #                      .dot( kernel.getDerMatrix( T_idx,T_idx, 'train',l ) ))

    ##### ADDED LINE TO MODIFY KERNEL HYPERPARAMETER
    kernel.hyp = btheta;
    bK_i   = kernel.getCovMatrix(T_idx,T_idx,'train')
    bK_i_inv = scipy.linalg.inv(bK_i+0.001*pert)

    new_niter = niter + 1
    np.savez_compressed(current_file, niter = new_niter)
    np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(new_niter)+'.npz',\
                              bW = bW, bmu=bmu, sigma2=sigma2, btheta = btheta, ES=ES, niter=new_niter)
    os.remove(options['working_path']+align_algo+'_'+lrh+'_'+str(new_niter-1)+'.npz')

    # calculate ELBO
    tmp_2rho2XmTXm = 0
    tmp_rho2WmTXm = 0
    tmp_1over2rho2 = 0
    for m in range(nsubjs):
        tmp_2rho2XmTXm += np.trace(bX[m*nvoxel:(m+1)*nvoxel,:].T.dot(bX[m*nvoxel:(m+1)*nvoxel,:]))/(2*sigma2[m])
        tmp_rho2WmTXm += np.trace(ES.T.dot(bW[m*nvoxel:(m+1)*nvoxel,:].T).dot(bX[m*nvoxel:(m+1)*nvoxel,:]))/sigma2[m]
        tmp_1over2rho2 += 1/(2*sigma2[m])

    tmp_muKmu = 0
    tmp_trKSig = 0
    for i in range(nfeature):
        tmp_muKmu  += ES[i,:].T.dot(bK_i_inv).dot(ES[i,:])
        tmp_trKSig += np.trace(bK_i_inv.dot(Sig_si_sum))
    sign , logdet = np.linalg.slogdet(bK_i)
    ELBO = nTR*nfeature*np.sum(sigma2)/2 - tmp_2rho2XmTXm + tmp_rho2WmTXm - tmp_1over2rho2*np.trace(ES.T.dot(ES))\
        -tmp_1over2rho2*np.trace(Sig_si_sum)  - 0.5*tmp_muKmu - 0.5*tmp_trKSig - 0.5*tmp_log_det_Sigsi #-0.5*nfeature*sign*logdet

    print 'ELBO'+str(ELBO)

    np.savez_compressed(options['working_path']+align_algo+'_'+'elbo_'+lrh+'_'+str(new_niter)+'.npz',\
                   ELBO=ELBO)

    return new_niter
