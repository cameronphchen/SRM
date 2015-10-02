# mystery segment identification experiment code

import numpy as np, sys
from scipy import stats
sys.path.append('/jukebox/ramadge/pohsuan/scikit-learn/sklearn')
from sklearn.svm import NuSVC
#from scikits.learn.svm import NuSVC

def predict(transformed_data, args, options = None):
    print 'mysseg',
    sys.stdout.flush()
  
    (ndim, nsample , nsubjs) = transformed_data.shape
    accu = np.zeros(shape=nsubjs)
  
    win_size = args.winsize
    nseg = nsample - win_size #TODO remove +1
    # mysseg prediction prediction
    trn_data = np.zeros((ndim*win_size, nseg))
  
    # the trn data also include the tst data, but will be subtracted when 
    # calculating A
    for m in range(nsubjs):
        for w in range(win_size):
            trn_data[w*ndim:(w+1)*ndim,:] += transformed_data[:,w:(w+nseg),m]
  
    for tst_subj in range(nsubjs):
        tst_data = np.zeros((ndim*win_size, nseg))
        for w in range(win_size):
            tst_data[w*ndim:(w+1)*ndim,:] = transformed_data[:,w:(w+nseg),tst_subj]
        
        A =  stats.zscore((trn_data - tst_data),axis=0, ddof=1)
        B =  stats.zscore(tst_data,axis=0, ddof=1)
    
        #A =  stats.zscore((trn_data - tst_data),axis=1, ddof=1)
        #B =  stats.zscore(tst_data,axis=1, ddof=1)
    
        #A =  trn_data - tst_data
        #B =  tst_data
    
        corr_mtx = B.T.dot(A)
    
        if options is not None:
            np.savez_compressed(options['working_path']+args.align_algo+'_acc_subj{}corr_mtx.npz'.format(tst_subj),corr_mtx = corr_mtx)
    
        for i in range(nseg):
            for j in range(nseg):
                if abs(i-j)<win_size and i != j :
                    corr_mtx[i,j] = -np.inf
    
        rank =  np.argmax(corr_mtx, axis=1)
        accu[tst_subj] = sum(rank == range(nseg)) / float(nseg)
  
    return accu

def predict_loo(transformed_data, args):
    print 'mysseg loo',
    sys.stdout.flush()
  
    (ndim, nsample , nsubjs) = transformed_data.shape
  
    tst_subj = args.loo
    win_size = args.winsize
    nseg = nsample - win_size
    # mysseg prediction prediction
    trn_data = np.zeros((ndim*win_size, nseg))
  
    # the trn data also include the tst data, but will be subtracted when 
    # calculating A
    for m in range(nsubjs):
        for w in range(win_size):
            trn_data[w*ndim:(w+1)*ndim,:] += transformed_data[:,w:(w+nseg),m]
  
    tst_data = np.zeros((ndim*win_size, nseg))
    for w in range(win_size):
        tst_data[w*ndim:(w+1)*ndim,:] = transformed_data[:,w:(w+nseg),tst_subj]
      
    A =  stats.zscore((trn_data - tst_data),axis=0, ddof=1)
    B =  stats.zscore(tst_data,axis=0, ddof=1)
    corr_mtx = B.T.dot(A)
  
    for i in range(nseg):
        for j in range(nseg):
            if abs(i-j)<win_size and i != j :
                corr_mtx[i,j] = -np.inf
  
    rank = np.argmax(corr_mtx, axis=1)
    accu = sum(rank == range(nseg)) / float(nseg)
  
    return accu
