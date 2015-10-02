# image prediction experiment code

import numpy as np, sys
#from scikits.learn.svm import NuSVC
sys.path.append('/jukebox/ramadge/pohsuan/scikit-learn/sklearn')
from sklearn.svm import NuSVC

def predict(transformed_data, args, trn_label ,tst_label):
    print 'imgpred',
    sys.stdout.flush()
    
    (ndim, nsample , nsubjs) = transformed_data.shape
    accu = np.zeros(shape=nsubjs)
  
    tst_data = np.zeros(shape = (ndim,nsample))
    trn_data = np.zeros(shape = (ndim,(nsubjs-1)*nsample))
    # image stimulus prediction 
    for tst_subj in range(nsubjs):
        tst_data = transformed_data[:,:,tst_subj]
    
        trn_subj = range(nsubjs)
        trn_subj.remove(tst_subj)
    
        for m in range(nsubjs-1):
          trn_data[:,m*nsample:(m+1)*nsample] = transformed_data[:,:,trn_subj[m]]
    
        # scikit-learn svm for classification
        #clf = NuSVC(nu=0.5, kernel = 'linear')
        clf = NuSVC(nu=0.5, kernel = 'linear')
        clf.fit(trn_data.T, trn_label)
    
        pred_label = clf.predict(tst_data.T)
          
        accu[tst_subj] = sum(pred_label == tst_label)/float(len(pred_label))
        
    return accu

def predict_loo(transformed_data, args, trn_label ,tst_label):
    print 'imgpred loo',
    print args.loo,
    sys.stdout.flush()
  
    (ndim, nsample , nsubjs) = transformed_data.shape
  
    loo = args.loo
    loo_idx = range(nsubjs)
    loo_idx.remove(loo)
  
    #tst_data = np.zeros(shape = (ndim,nsample))
    trn_data = np.zeros(shape = (ndim,(nsubjs-1)*nsample))
    # image stimulus prediction
    # tst_data : ndim x nsample
    tst_data = transformed_data[:,:,loo]
  
    for m in range(len(loo_idx)):
        trn_data[:,m*nsample:(m+1)*nsample] = transformed_data[:,:,loo_idx[m]]
    
    # scikit-learn svm for classification
    clf = NuSVC(nu=0.5, kernel = 'linear')
    clf.fit(trn_data.T, trn_label)
    pred_label = clf.predict(tst_data.T)
        
    accu = sum(pred_label == tst_label)/float(len(pred_label))
  
    return accu
