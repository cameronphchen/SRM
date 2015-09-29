#!/usr/bin/env python

# by Cameron Po-Hsuan Chen @ Princeton
#####THIS CODE IS NOT WORKING YET!!

import numpy as np, scipy, random, sys, math, os
import scipy.io
from scipy import stats
import argparse
from scikits.learn.svm import NuSVC
import importlib
import pprint
from transform_matrix import form_transformation_matrix, \
                             form_transformation_matrix_loo, \
                             form_transformation_matrix_noalign


parser = argparse.ArgumentParser()

parser.add_argument("dataset",    help="name of the dataset")
parser.add_argument("nvoxel", type = int,
                    help="number of voxels in the dataset")
parser.add_argument("nTR", type = int,
                    help="number of TRs in the dataset")
parser.add_argument("nsubjs", type = int,
                    help="number of subjects in the dataset")

parser.add_argument("exptype",    help="name of the experiment type")
parser.add_argument("-w", "--winsize", type = int,
                    help="mysseg winsize")
parser.add_argument("-l", "--loo",
                    help="check loo")

args = parser.parse_args()

align_algo_list=['noalign', 'ha', 'pha_em', 'ha_syn', 'ha_sm_retraction']
nfeature_list  = [10,50,100,500,1300]
rand_list      = range(5)
if args.loo is not None:
    loo_list       = range(args.nsubjs)


for align_algo in align_algo_list:
    for nfeature in nfeature_list:
        for rand in rand_list:
            for loo in loo_list:
                data_folder = args.dataset+'/'+str(args.nvoxel)+'vx/'+str(args.nTR)+'TR/'
                exp_folder  = args.exptype+("_"+args.expopt  if args.expopt else "" ) + \
                     ("_winsize"+str(args.winsize) if args.winsize else "" ) + '/' 
                alg_folder  = align_algo + ("_"+kernel if kernel else "") +'/'
                opt_folder  = str(nfeature) + 'feat/' + \
                     ("rand"+str(randseed)+'/' if randseed != None else "identity/" )+\
                     ("loo"+str(loo) if args.loo != None else "all" ) + '/'

                working_path='/fastscratch/pohsuan/pHA/data/working/'+\
                     data_folder+exp_folder+alg_folder+opt_folder

                # terminate the experiment early if the experiment is already done
                if not os.path.exists(options['working_path']+args.align_algo+'_acc_10.npz'):
                    print 'NO'+options['working_path']+args.align_algo+'_acc_10.npz'

