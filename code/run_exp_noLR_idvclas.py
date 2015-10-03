#!/usr/bin/env python

# This is the code to run experiment without separating data from left
# and right hemisphere
# Please refer to --help for arguments setting
#
# before running the experiment, please make sure to execute 
# data_preprocessing.m and  transform_matdata2pydata.py to transformt the mat 
# format data into python .npz
#
# by Cameron Po-Hsuan Chen @ Princeton
 

import numpy as np, scipy, random, sys, math, os, copy
import scipy.io
from scipy import stats
import argparse
sys.path.append('/jukebox/ramadge/pohsuan/scikit-learn/sklearn')
from sklearn.svm import NuSVC
from sklearn import preprocessing
#from scikits.learn.svm import NuSVC
import importlib
import pprint
from transform_matrix import form_transformation_matrix, \
                             form_transformation_matrix_loo, \
                             form_transformation_matrix_noalign

## argument parsing
usage = '%(prog)s dataset nvoxel nTR  exptype [--loo] [--expopt] [--winsize] \
align_algo [-k kernel] niter nfeature_all nfeature_group [-r RANDSEED] [--strfresh]'
parser = argparse.ArgumentParser(usage=usage)

parser.add_argument("dataset",    help="name of the dataset")
parser.add_argument("nvoxel", type = int,
                    help="number of voxels in the dataset")
parser.add_argument("nTR", type = int,
                    help="number of TRs in the dataset")

parser.add_argument("exptype",    help="name of the experiment type")
parser.add_argument("-l", "--loo", type = int,
                    help="whether this experiment is loo experiment")
parser.add_argument("-e","--expopt",    help="experiment options e.g. 1st or 2nd")
parser.add_argument("-w", "--winsize", type = int,
                    help="mysseg winsize")

parser.add_argument("align_algo", help="name of the alignment algorithm")
parser.add_argument("-k", "--kernel", metavar='',
                    help="type of kernel to use")

parser.add_argument("niter"     , type = int,  
                    help="number of iterations to the algorithm")

parser.add_argument("nfeature_all", type=int,
                    help="number of features")

parser.add_argument("nfeature_group", type=int,
                    help="number of features")

parser.add_argument("-r", "--randseed", type=int, metavar='',
                    help="random seed for initialization")
parser.add_argument("--strfresh", action="store_true" ,
                    help="start alignment fresh, not picking up from where was left")
parser.add_argument("--nfeature", type=int,
                    help="number of features")


args = parser.parse_args()
print '--------------experiment arguments--------------'
pprint.pprint(args.__dict__,width=1)


data_folder = args.dataset+'/'+str(args.nvoxel)+'vx/'+str(args.nTR)+'TR/'
exp_folder  = args.exptype+("_"+args.expopt  if args.expopt else "" ) + \
              ("_winsize"+str(args.winsize) if args.winsize else "" ) + '/' 
alg_folder  = args.align_algo + ("_"+args.kernel if args.kernel else "") +'/'
opt_all_folder = 'all' + str(args.nfeature_all) + 'feat/' + \
              ("rand"+str(args.randseed)+'/' if args.randseed != None else "identity/" )+'all/'

opt_group_folder = 'all' + str(args.nfeature_all) + 'feat/' + 'group' + str(args.nfeature_group) + 'feat/' + \
              ("rand"+str(args.randseed)+'/' if args.randseed != None else "identity/" )+\
              "loo"+str(args.loo) + '/'

# rondo options


options = {'input_path'  : '/jukebox/ramadge/pohsuan/SRM/data/input/'+data_folder,\
           'working_path': '/fastscratch/pohsuan/SRM/data/working/'+\
                           data_folder+exp_folder+alg_folder,\
           'output_path' : '/jukebox/ramadge/pohsuan/SRM/data/output/'+\
                            data_folder+exp_folder+alg_folder+opt_group_folder}
print '----------------experiment paths----------------'
pprint.pprint(options,width=1)
print '------------------------------------------------'


if os.path.exists(options['working_path']+opt_group_folder+args.align_algo+'_acc_'+str(10)+'.npz'):
    sys.exit('experiment finished, early termination')

# creating working folder
if not os.path.exists(options['working_path']):
    os.makedirs(options['working_path'])
#if not os.path.exists(options['output_path']):
    #os.makedirs(options['output_path'])

# terminate the experiment early if the experiment is already done
#if os.path.exists(options['working_path']+args.align_algo+'_acc_10.npz'):
#  sys.exit('experiment already finished, early termination')

print 'start loading data'
# load data for alignment and prediction
# load movie data after voxel selection by matdata_preprocess.m
if args.exptype in ['idvclas', 'idvclas_svm', 'idvclas_svm_no2ndSRM','idvclas_svm_on1st']:
    if args.loo == None:
        sys.exit('no loo subject')

    movie_data = scipy.io.loadmat(options['input_path']+'movie_data.mat')
    movie_data = movie_data['movie_data']

    align_data = np.zeros((movie_data.shape))
    nsubj_group = movie_data.shape[2]/2 #assuming two groups, and they have equal amount of people

    for m in range(align_data.shape[2]):
        align_data[:,:,m] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T

    # align all data to remove the shared part
    options_all = copy.deepcopy(options)
    options_all['working_path'] = options['working_path']+opt_all_folder
    args.nfeature = args.nfeature_all


    if not os.path.exists(options_all['working_path']):
        os.makedirs(options_all['working_path'])

    if args.nfeature_all is not 0:
        if not os.path.exists(options_all['working_path']+args.align_algo+'__10.npz'):
            for iter in range(10):
                if os.path.exists(options_all['working_path']+args.align_algo+'__10.npz'):
                    break
                algo = importlib.import_module('alignment_algo.'+args.align_algo)
                algo.align(align_data, options_all, args, '')

        workspace = np.load(options_all['working_path']+args.align_algo+'__10.npz')

        W = workspace['R']
        S = workspace['G'].T

        if args.exptype != 'idvclas_svm_on1st':
            for m in range(align_data.shape[2]):
                tmp = align_data[:,:,m] - W[:,:,m].dot(S)
                align_data[:,:,m] = stats.zscore(tmp.T ,axis=0, ddof=1).T
        elif args.exptype == 'idvclas_svm_on1st':
            for m in range(align_data.shape[2]):
                tmp = W[:,:,m].dot(S)
                align_data[:,:,m] = stats.zscore(tmp.T ,axis=0, ddof=1).T    
    else:
        print 'shared all feature = 0'        


    align_data_group1 = np.copy(align_data[:,:,:nsubj_group])
    align_data_group2 = np.copy(align_data[:,:,nsubj_group:])

    pred_data_group1 = np.copy(align_data_group1[:,:,args.loo])
    pred_data_group2 = np.copy(align_data_group2[:,:,args.loo])
else:
    sys.exit('invalid experiment type')

if args.loo != None:
    align_data_group1_loo = np.delete(align_data_group1, args.loo,2)
    align_data_group2_loo = np.delete(align_data_group2, args.loo,2)

# run alignment
print 'start alignment'
if args.align_algo != 'noalign':
    algo = importlib.import_module('alignment_algo.'+args.align_algo)

options_group1 = copy.deepcopy(options)
options_group1['working_path'] = options['working_path']+opt_group_folder+'group1/'
options_group2 = copy.deepcopy(options)
options_group2['working_path'] = options['working_path']+opt_group_folder+'group2/'
args.nfeature = args.nfeature_group

if args.strfresh:
  if os.path.exists(options_group1['working_path']+args.align_algo+'__current.npz'):
    os.remove(options_group1['working_path']+args.align_algo+'__current.npz')
  if os.path.exists(options_group2['working_path']+args.align_algo+'__current.npz'):
    os.remove(options_group2['working_path']+args.align_algo+'__current.npz')

if not os.path.exists(options_group1['working_path']):
    os.makedirs(options_group1['working_path'])
if not os.path.exists(options_group2['working_path']):
    os.makedirs(options_group2['working_path'])


for itr in range(args.niter):
    if  args.align_algo not in ['noalign'] and  args.exptype not in ['idvclas_svm_no2ndSRM','idvclas_svm_on1st']:

        print '\nalign group1'
        new_niter = algo.align(align_data_group1_loo, options_group1, args, '')
        workspace_group1 = np.load(options_group1['working_path']+args.align_algo+'__'+str(new_niter)+'.npz')
        S_group1 = workspace_group1['G'].T
        W_group1 = workspace_group1['R']
        #S_group1 = stats.zscore(workspace_group1['G'], axis=0, ddof=1).T
        workspace_group1.close()

        print '\nalign group2'
        new_niter = algo.align(align_data_group2_loo, options_group2, args, '')
        workspace_group2 = np.load(options_group2['working_path']+args.align_algo+'__'+str(new_niter)+'.npz')
        S_group2 = workspace_group2['G'].T
        W_group2 = workspace_group2['R']
        #S_group2 = stats.zscore(workspace_group2['G'],axis=0, ddof=1).T
        workspace_group2.close()

    print args.exptype
    if args.exptype == 'idvclas':
        accu = []
        for label, pred_data in enumerate([pred_data_group1, pred_data_group2]):
            Am = pred_data.dot(S_group1.T)
            pert = np.zeros((Am.shape))
            np.fill_diagonal(pert,1)

            U1, _, V1 = np.linalg.svd(Am+0.00*pert,full_matrices=False)
            Am = pred_data.dot(S_group2.T)
            U2, _, V2 = np.linalg.svd(Am+0.00*pert,full_matrices=False)

            W1 = U1.dot(V1)
            W2 = U2.dot(V2)

            err1 = np.linalg.norm(pred_data-W1.dot(S_group1),'fro')
            err2 = np.linalg.norm(pred_data-W2.dot(S_group2),'fro')
            if label == 0:
                print '\nerr1:{:.3f}, err2:{:.3f}, err2-err1:{}'.format(err1,err2,err2-err1),
            else:
                print 'err1:{:.3f}, err2:{:.3f}, err1-err2:{}'.format(err1,err2,err1-err2),

            if err2 - err1 > 0:
                accu.append(int(label == 0))
            elif err1 - err2 > 0:
                accu.append(int(label == 1))
            print accu
    elif args.exptype == 'idvclas_svm':
        dim = args.nvoxel*args.nTR
        trn_data  = np.zeros((nsubj_group*2-2, dim))
        tst_data  = np.zeros((2, dim))

        trn_label = np.zeros(nsubj_group*2-2)
        tst_label = np.zeros(2)

        for i in xrange(W_group1.shape[2]):
            tmp1 = W_group1[:, :, i].dot(S_group1)
            trn_data[i,:] = tmp1.reshape(1, dim)
            trn_label[i] = 0
            tmp2 = W_group2[:, :, i].dot(S_group2)
            trn_data[i+nsubj_group-1,:] = tmp2.reshape(1, dim)
            trn_label[i+nsubj_group-1] = 1

        tst_data[0, :] = pred_data_group1.reshape(1, dim)
        tst_data[1, :] = pred_data_group2.reshape(1, dim)
        tst_label[0] = 0
        tst_label[1] = 1

        """
        print 'standardization'
        print trn_data
        print tst_data
        trn_data_scaled = preprocessing.scale(trn_data)
        tst_data_scaled = preprocessing.scale(tst_data)
        print trn_data_scaled
        print tst_data_scaled
        clf = NuSVC(nu=0.5, kernel = 'linear')
        clf.fit(trn_data_scaled, trn_label)
        pred_label = clf.predict(tst_data_scaled)
        print pred_label
        print clf.decision_function(tst_data_scaled)
        accu = sum(pred_label == tst_label)/float(len(pred_label))
        """
    
    elif args.exptype == 'idvclas_svm_no2ndSRM':
        dim = args.nvoxel*args.nTR
        trn_data  = np.zeros((nsubj_group*2-2, dim))
        tst_data  = np.zeros((2, dim))

        trn_label = np.zeros(nsubj_group*2-2)
        tst_label = np.zeros(2)

        for i in xrange(align_data_group1_loo.shape[2]):
            trn_data[i,:] = align_data_group1_loo[:,:,i].reshape(1, dim)
            trn_label[i] = 0
            trn_data[i+nsubj_group-1,:] = align_data_group2_loo[:,:,i].reshape(1, dim)
            trn_label[i+nsubj_group-1] = 1

        tst_data[0, :] = pred_data_group1.reshape(1, dim)
        tst_data[1, :] = pred_data_group2.reshape(1, dim)
        tst_label[0] = 0
        tst_label[1] = 1

        """
        print 'standardization'
        trn_data_scaled = preprocessing.scale(trn_data)
        tst_data_scaled = preprocessing.scale(tst_data)
        print trn_data_scaled
        print tst_data_scaled
        clf = NuSVC(nu=0.5, kernel = 'linear')
        clf.fit(trn_data_scaled, trn_label)
        pred_label = clf.predict(tst_data_scaled)
        print pred_label
        print clf.decision_function(tst_data_scaled)
        accu = sum(pred_label == tst_label)/float(len(pred_label))
        """

    elif args.exptype == 'idvclas_svm_on1st':
        dim = args.nvoxel*args.nTR
        trn_data  = np.zeros((nsubj_group*2-2, dim))
        tst_data  = np.zeros((2, dim))

        trn_label = np.zeros(nsubj_group*2-2)
        tst_label = np.zeros(2)

        for i in xrange(align_data_group1_loo.shape[2]):
            trn_data[i,:] = align_data_group1_loo[:,:,i].reshape(1, dim)
            trn_label[i] = 0
            trn_data[i+nsubj_group-1,:] = align_data_group2_loo[:,:,i].reshape(1, dim)
            trn_label[i+nsubj_group-1] = 1

        tst_data[0, :] = pred_data_group1.reshape(1, dim)
        tst_data[1, :] = pred_data_group2.reshape(1, dim)
        tst_label[0] = 0
        tst_label[1] = 1

        """
        print 'standardization'
        trn_data = preprocessing.scale(trn_data)
        tst_data = preprocessing.scale(tst_data)
        clf = NuSVC(nu=0.5, kernel = 'linear')
        clf.fit(trn_data, trn_label)
        pred_label = clf.predict(tst_data)
        print pred_label
        print clf.decision_function(tst_data)
        accu = sum(pred_label == tst_label)/float(len(pred_label))
        """

    print 'standardization'
    #print trn_data
    #print tst_data
    #trn_data_scaled = preprocessing.scale(trn_data)
    #tst_data_scaled = preprocessing.scale(tst_data)
    scaler = preprocessing.StandardScaler().fit(trn_data)
    trn_data_scaled = scaler.transform(trn_data)
    tst_data_scaled = scaler.transform(tst_data)
    #print trn_data_scaled
    #print tst_data_scaled
    clf = NuSVC(nu=0.5, kernel = 'linear')
    clf.fit(trn_data_scaled, trn_label)
    pred_label = clf.predict(tst_data_scaled)
    print pred_label
    print clf.decision_function(tst_data_scaled)
    accu = sum(pred_label == tst_label)/float(len(pred_label))


    
    if args.align_algo in ['ppca_idvclas','pica_idvclas']:
        for it in range(11):
            np.savez_compressed(options['working_path']+opt_group_folder+args.align_algo+'_acc_'+str(it)+'.npz',accu = accu)
    else:
        np.savez_compressed(options['working_path']+opt_group_folder+args.align_algo+'_acc_'+str(itr)+'.npz',accu = accu)
        #np.savez_compressed(options['working_path']+opt_group_folder+args.align_algo+'_acc_'+str(10)+'.npz',accu = accu)
    print options['working_path']+opt_group_folder+args.align_algo+'_acc_'+str(itr)+'.npz'
    print np.mean(accu)

