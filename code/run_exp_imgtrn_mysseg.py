#!/usr/bin/env python

# This is the code to run experiment 
# Please refer to --help for arguments setting
#
# before running the experiment, please make sure to execute 
# data_preprocessing.m and  transform_matdata2pydata.py to transformt the mat 
# format data into python .npz
#
# by Cameron Po-Hsuan Chen @ Princeton
 

import numpy as np
import scipy
import scipy.io
from scipy import stats
import random
import sys
import math
import os
import argparse
#from scikits.learn.svm import NuSVC
sys.path.append('/jukebox/ramadge/pohsuan/scikit-learn/sklearn')
from sklearn.svm import NuSVC
import importlib
import pprint
from transform_matrix import form_transformation_matrix, \
                             form_transformation_matrix_loo, \
                             form_transformation_matrix_noalign

## argument parsing
usage = '%(prog)s dataset nvoxel nTR  exptype [--loo] [--expopt] [--winsize] \
align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]'
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
parser.add_argument("-s", "--sigma" , type = float,  
                    help="sigma2 value")
parser.add_argument("niter"     , type = int,  
                    help="number of iterations to the algorithm")
parser.add_argument("nfeature", type=int, 
                    help="number of features")
parser.add_argument("-r", "--randseed", type=int, metavar='',
                    help="random seed for initialization")
parser.add_argument("--strfresh", action="store_true" ,
                    help="start alignment fresh, not picking up from where was left")


args = parser.parse_args()
print '--------------experiment arguments--------------'
pprint.pprint(args.__dict__,width=1)

# sanity check
assert args.nvoxel >= args.nfeature

data_folder = args.dataset+'/'+str(args.nvoxel)+'vx/'+str(args.nTR)+'TR/'
exp_folder  = args.exptype+("_"+args.expopt  if args.expopt else "" ) + \
              ("_winsize"+str(args.winsize) if args.winsize else "" ) + '/' 
alg_folder  = args.align_algo + ("_kr"+args.kernel if args.kernel else "") +("_sig"+str(args.sigma) if args.sigma is not None else "")+'/'
opt_folder  = str(args.nfeature) + 'feat/' + \
              ("rand"+str(args.randseed)+'/' if args.randseed != None else "identity/" )+\
              ("loo"+str(args.loo) if args.loo != None else "all" ) + '/'

# rondo options
options = {'input_path'  : '/jukebox/ramadge/pohsuan/SRM/data/input/'+data_folder,\
           'working_path': '/fastscratch/pohsuan/SRM/data/working/'+\
                            data_folder+exp_folder+alg_folder+opt_folder,\
           'output_path' : '/jukebox/ramadge/pohsuan/SRM/data/output/'+\
                            data_folder+exp_folder+alg_folder+opt_folder}
print '----------------experiment paths----------------'
pprint.pprint(options,width=1)
print '------------------------------------------------'

# sanity check of the input arguments
if args.exptype == 'imgtrn_mysseg':
  if args.winsize == None:
    sys.exit('mysseg experiment need arg winsize')

# creating working folder
if not os.path.exists(options['working_path']):
    os.makedirs(options['working_path'])
#if not os.path.exists(options['output_path']):
    #os.makedirs(options['output_path'])

if args.strfresh:
    if os.path.exists(options['working_path']+args.align_algo+'_rh_current.npz'):
        os.remove(options['working_path']+args.align_algo+'_rh_current.npz')
    if os.path.exists(options['working_path']+args.align_algo+'_lh_current.npz'):
        os.remove(options['working_path']+args.align_algo+'_lh_current.npz')
else:
    if os.path.exists(options['working_path']+args.align_algo+'_lh_current.npz') \
      and os.path.exists(options['working_path']+args.align_algo+'_rh_current.npz'):
        wslh = np.load(options['working_path']+args.align_algo+'_lh_current.npz')
        wsrh = np.load(options['working_path']+args.align_algo+'_rh_current.npz')
        tmp_niter = min(wslh['niter'],wsrh['niter'])
        np.savez_compressed(options['working_path']+args.align_algo+'_lh_current.npz', niter = tmp_niter)
        np.savez_compressed(options['working_path']+args.align_algo+'_rh_current.npz', niter = tmp_niter)
    else:
        if os.path.exists(options['working_path']+args.align_algo+'_rh_current.npz'):
            os.remove(options['working_path']+args.align_algo+'_rh_current.npz')
        if os.path.exists(options['working_path']+args.align_algo+'_lh_current.npz'):
            os.remove(options['working_path']+args.align_algo+'_lh_current.npz')

# terminate the experiment early if the experiment is already done
#if os.path.exists(options['working_path']+args.align_algo+'_acc_10.npz'):
#    sys.exit('experiment already finished, early termination')


print 'start loading data'
# load data for alignment and prediction
# load movie data after voxel selection by matdata_preprocess.m 
if args.exptype == 'imgtrn_mysseg':
  image_data_lh = scipy.io.loadmat(options['input_path']+'image_timeseries_data_lh.mat')
  image_data_rh = scipy.io.loadmat(options['input_path']+'image_timeseries_data_rh.mat')
  align_data_lh= image_data_lh['image_data_lh']
  align_data_rh= image_data_rh['image_data_rh']

  # load label for testing data
  movie_data_lh = scipy.io.loadmat(options['input_path']+'movie_data_lh.mat')
  movie_data_rh = scipy.io.loadmat(options['input_path']+'movie_data_rh.mat')
  pred_data_lh = movie_data_lh['movie_data_lh'] 
  pred_data_rh = movie_data_rh['movie_data_rh'] 
  
  for m in range(pred_data_lh.shape[2]):
      align_data_lh[:,:,m] = stats.zscore(align_data_lh[:,:,m].T ,axis=0, ddof=1).T 
      align_data_rh[:,:,m] = stats.zscore(align_data_rh[:,:,m].T ,axis=0, ddof=1).T 
      pred_data_lh[:,:,m] = stats.zscore(pred_data_lh[:,:,m].T ,axis=0, ddof=1).T 
      pred_data_rh[:,:,m] = stats.zscore(pred_data_rh[:,:,m].T ,axis=0, ddof=1).T 
      
else:
  sys.exit('invalid experiment type')


if args.loo != None:
  align_data_lh_loo = np.delete(align_data_lh, args.loo,2) 
  align_data_rh_loo = np.delete(align_data_rh, args.loo,2)

(nvoxel_align, nTR_align, nsubjs_align) = align_data_lh.shape
(nvoxel_pred , nTR_pred , nsubjs_pred)  = pred_data_lh.shape
nsubjs = nsubjs_pred
# make sure the dimension of dataset is consistent with input args
assert nvoxel_pred == nvoxel_align
assert nvoxel_pred == args.nvoxel
assert nsubjs_pred == nsubjs_align or args.loo

# run alignment
print 'start alignment'
if args.align_algo != 'noalign':
  algo = importlib.import_module('alignment_algo.'+args.align_algo)
expt = importlib.import_module('experiments.'+args.exptype)
for i in range(args.niter):
  
  if args.align_algo != 'noalign':
    if args.loo == None:
        new_niter_lh = algo.align(align_data_lh, options, args, 'lh')
        new_niter_rh = algo.align(align_data_rh, options, args, 'rh')
    else:
        new_niter_lh = algo.align(align_data_lh_loo, options, args, 'lh')
        new_niter_rh = algo.align(align_data_rh_loo, options, args, 'rh')
      # make sure right and left brain alignment are working at the same iterations
    assert new_niter_lh == new_niter_rh


  if args.align_algo in ['pica','ppca']:
    new_niter_lh = new_niter_rh = 10
  #elif args.align_algo in ['ha_sm_retraction','ha_syn','ha_syn_noagg']:
  #  new_niter_lh = new_niter_rh = 0

  # load transformation matrices
  if args.align_algo != 'noalign' :
    workspace_lh = np.load(options['working_path']+args.align_algo+'_lh_'+str(new_niter_lh)+'.npz')
    workspace_rh = np.load(options['working_path']+args.align_algo+'_rh_'+str(new_niter_rh)+'.npz')
    # load transformation matrices into transform_lrh for projecting testing data
    if args.loo == None:
      (transform_lh, transform_rh) = form_transformation_matrix.transform(args, 
                                     workspace_lh, workspace_rh, nsubjs)
    else:
      (transform_lh, transform_rh) = form_transformation_matrix_loo.transform(args, 
                                     workspace_lh, workspace_rh, 
                                     align_data_lh, align_data_rh, nsubjs)
  else:
    new_niter_lh = new_niter_rh = 10
    (transform_lh, transform_rh)=form_transformation_matrix_noalign.transform(args,nsubjs)

  # transformed mkdg data with learned transformation matrices
  transformed_data = np.zeros((args.nfeature*2 , nTR_pred ,nsubjs))

  for m in range(nsubjs):
    trfed_lh_tmp = transform_lh[:,:,m].T.dot(pred_data_lh[:,:,m])
    #np.savez_compressed(options['working_path']+args.align_algo+'_trfed_lh_'+str(new_niter_lh)+'.npz',trfed_lh = trfed_lh_tmp)
    trfed_rh_tmp = transform_rh[:,:,m].T.dot(pred_data_rh[:,:,m])
    #np.savez_compressed(options['working_path']+args.align_algo+'_trfed_rh_'+str(new_niter_lh)+'.npz',trfed_rh = trfed_rh_tmp)
    transformed_data[:,:,m] = stats.zscore( np.vstack((trfed_lh_tmp,trfed_rh_tmp)).T ,axis=0, ddof=1).T
  #np.savez_compressed(options['working_path']+args.align_algo+'_trfed_'+str(new_niter_lh)+'.npz',transformed_data = transformed_data)

  # experiment
  if args.exptype == 'imgtrn_mysseg':
    if args.loo == None:
      accu = expt.predict(transformed_data, args)
    else:
      accu = expt.predict_loo(transformed_data, args)

  np.savez_compressed(options['working_path']+args.align_algo+'_acc_'+str(new_niter_lh)+'.npz',accu = accu)
  if args.align_algo in ['noalign','pica','ppca']:
      for iteration in range(10):
          np.savez_compressed(options['working_path']+args.align_algo+'_acc_'+str(iteration)+'.npz',accu = accu)
  print np.mean(accu)