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
#from scikits.learn.svm import NuSVC
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
alg_folder  = args.align_algo + ("_"+args.kernel if args.kernel else "") +( "_sig"+str(args.sigma) if args.sigma is not None else "")+'/'
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
if args.exptype == 'mysseg':
  if args.winsize == None:
    sys.exit('mysseg experiment need arg winsize')
  if args.expopt != '1st' and args.expopt != '2nd':
    sys.exit('mysseg experiment need expopt as 1st or 2nd')

# creating working folder
if not os.path.exists(options['working_path']):
    os.makedirs(options['working_path'])
#if not os.path.exists(options['output_path']):
    #os.makedirs(options['output_path'])

if args.strfresh:
  if os.path.exists(options['working_path']+args.align_algo+'__current.npz'):
    os.remove(options['working_path']+args.align_algo+'__current.npz')

# terminate the experiment early if the experiment is already done
#if os.path.exists(options['working_path']+args.align_algo+'_acc_10.npz'):
#    sys.exit('experiment already finished, early termination')


print 'start loading data'
# load data for alignment and prediction
# load movie data after voxel selection by matdata_preprocess.m 
if args.exptype == 'imgpred':
  image_data = scipy.io.loadmat(options['input_path']+'image_data.mat')
  pred_data = image_data['image_data']

  # load label for testing data
  label = scipy.io.loadmat(options['input_path']+'action_label.mat')
  label = label['label']
  label = np.squeeze(label)
  trn_label = np.hstack([label]*(pred_data.shape[2]-1))
  tst_label = label
  #trn_label = np.squeeze(np.asarray(trn_label))
  #tst_label = np.squeeze(np.asarray(tst_label))
  
  movie_data = scipy.io.loadmat(options['input_path']+'movie_data.mat')
  align_data = movie_data['movie_data'] 

elif args.exptype == 'mysseg':
  movie_data = scipy.io.loadmat(options['input_path']+'movie_data.mat')
  movie_data = movie_data['movie_data']

  if args.nTR % 2 == 0:
    movie_data_1st = movie_data[:,0:args.nTR/2,:]
    movie_data_2nd = movie_data[:,(args.nTR/2):args.nTR,:]
  else:
    movie_data_1st = movie_data[:,0:args.nTR/2,:]
    movie_data_2nd = movie_data[:,(args.nTR/2+1):args.nTR,:]

  align_data = np.zeros((movie_data_1st.shape))
  pred_data  = np.zeros((movie_data_2nd.shape))

  if '1st' == args.expopt:
    for m in range(align_data.shape[2]):
      align_data[:,:,m] = stats.zscore(movie_data_1st[:,:,m].T ,axis=0, ddof=1).T
      pred_data[:,:,m]  = stats.zscore(movie_data_2nd[:,:,m].T ,axis=0, ddof=1).T
  elif '2nd' == args.expopt:
    for m in range(align_data.shape[2]):
      align_data[:,:,m] = stats.zscore(movie_data_2nd[:,:,m].T ,axis=0, ddof=1).T
      pred_data[:,:,m]  = stats.zscore(movie_data_1st[:,:,m].T ,axis=0, ddof=1).T
  else:
    sys.exit('missing 1st or 2nd arg for mysseg experiment')

else:
  sys.exit('invalid experiment type')


if args.loo != None:
  align_data_loo = np.delete(align_data, args.loo,2)

(nvoxel_align, nTR_align, nsubjs_align) = align_data.shape
(nvoxel_pred , nTR_pred , nsubjs_pred)  = pred_data.shape
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
      new_niter = algo.align(align_data, options, args, '')
    else:
      new_niter = algo.align(align_data_loo, options, args, '')
    # make sure right and left brain alignment are working at the same iterations

  if args.align_algo in ['pica','ppca']:
    new_niter = 10

  # load transformation matrices
  if args.align_algo != 'noalign' :
    workspace = np.load(options['working_path']+args.align_algo+'__'+str(new_niter)+'.npz')
    workspace2 = np.load(options['working_path']+args.align_algo+'__'+str(new_niter)+'.npz')
    # load transformation matrices into transform_lrh for projecting testing data
    if args.loo == None:
      (transform, tmp) = form_transformation_matrix.transform(args,
                                     workspace, workspace2, nsubjs)
    else:
      (transform, tmp) = form_transformation_matrix_loo.transform(args,
                                     workspace, workspace2,
                                     align_data, copy.deepcopy(align_data), nsubjs)
    workspace.close()
    workspace2.close()
  else:
    new_niter = 10
    (transform, tmp) = form_transformation_matrix_noalign.transform(args, nsubjs)


  # transformed mkdg data with learned transformation matrices
  transformed_data = np.zeros((args.nfeature , nTR_pred ,nsubjs))

  for m in range(nsubjs):
    trfed_tmp = transform[:,:,m].T.dot(pred_data[:,:,m])
    transformed_data[:,:,m] = stats.zscore( trfed_tmp.T ,axis=0, ddof=1).T
    #transformed_data[:,:,m] = trfed_tmp

  # experiment
  if args.exptype == 'imgpred':
    if args.loo == None:
      accu = expt.predict(transformed_data, args, trn_label, tst_label)
    else:
      accu = expt.predict_loo(transformed_data, args, trn_label, tst_label)  
  elif args.exptype == 'mysseg':
    if args.loo == None:
      accu = expt.predict(transformed_data, args, options)
    else:
      accu = expt.predict_loo(transformed_data, args)

  np.savez_compressed(options['working_path']+args.align_algo+'_acc_'+str(new_niter)+'.npz',accu = accu)
  print np.mean(accu)
