#!/usr/bin/env python
# plot barchart for image prediction across different algorithms  
import pprint
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math
import pickle
import os
import sys
import scipy
import scipy.io
import copy
sys.path.append('/jukebox/ramadge/pohsuan/pHA/code/')
from transform_matrix import form_transformation_matrix, \
                             form_transformation_matrix_loo, \
                             form_transformation_matrix_noalign

parser = argparse.ArgumentParser()
parser.add_argument("dataset",    help="name of the dataset")
parser.add_argument("nvoxel", type=int,
                    help="number of voxels in the dataset")
parser.add_argument("nTR", type=int,
                    help="number of TRs in the dataset")
parser.add_argument("nsubjs", type=int,
                    help="number of subjects in the dataset")
parser.add_argument("niter", type=int,
                    help="number of iterations to the algorithm")
parser.add_argument("nrand", type=int,
                    help="number of random initilization to average")

args = parser.parse_args()
print '--------------experiment arguments--------------'
pprint.pprint(args.__dict__,width=1)

#####################List out all the algos to show in fig#####################

os.system("python create_algo_list_objVSacc.py")
pkl_file = open('algo_list.pkl', 'rb')
algo_list = pickle.load(pkl_file)
pkl_file.close()

###############################################################################

name = []
for algo in algo_list:
  name.append(algo['name'])

acc_mean = np.zeros((len(name), args.niter))
acc_se = np.zeros((len(name), args.niter))
obj_mean = np.zeros((len(name), args.niter))
obj_se = np.zeros((len(name), args.niter))

data_folder = args.dataset+'/'+str(args.nvoxel)+'vx/'+str(args.nTR)+'TR/'
exp_folder = 'imgpred/'

input_path = '/jukebox/ramadge/pohsuan/pHA/data/input/'+data_folder
working_path = '/fastscratch/pohsuan/pHA/data/working/'+data_folder+exp_folder
output_path = '/jukebox/ramadge/pohsuan/pHA/data/output/'

movie_data_lh = scipy.io.loadmat(input_path+'movie_data_lh.mat')
movie_data_rh = scipy.io.loadmat(input_path+'movie_data_rh.mat')
align_data_lh = movie_data_lh['movie_data_lh']
align_data_rh = movie_data_rh['movie_data_rh']

def get_acc(acc_file):
    if not os.path.exists(acc_file):
        print 'NO ' + acc_file
        return -1, True
    else:
        ws_acc = np.load(acc_file)
        accu = ws_acc['accu']
        ws_acc.close()
        return accu, False

def get_args_copy(algo):
    args_tmp = copy.deepcopy(args)
    args_tmp.__dict__['align_algo'] = algo['align_algo']
    args_tmp.__dict__['nfeature'] = int(algo['nfeature'])
    args_tmp.__dict__['loo'] = loo
    return args_tmp

def get_obj(obj_file_lh, obj_file_rh, args_tmp):
    def obj_func(obj_ws_lf, obj_ws_rf):
        (transform_lh, transform_rh) = form_transformation_matrix_loo.transform(args_tmp, obj_ws_lf, obj_ws_rf,
                                                                                align_data_lh, align_data_rh,
                                                                                args_tmp.nsubjs)
        obj_val_tmp = 0
        for m in range(args_tmp.nsubjs):
            if args_tmp.align_algo in ['ha','ha_sm_retraction']:
                obj_val_tmp += np.linalg.norm(transform_lh[:, :, m].T.dot(align_data_lh[:, :, m]) - obj_ws_lf['G'].T, 'fro')
                obj_val_tmp += np.linalg.norm(transform_rh[:, :, m].T.dot(align_data_rh[:, :, m]) - obj_ws_rf['G'].T, 'fro')
            elif args_tmp.align_algo in ['ha_syn','pha_em','ha_syn_noagg']:
                obj_val_tmp += np.linalg.norm(align_data_lh[:, :, m] - transform_lh[:, :, m].dot(obj_ws_lf['G'].T), 'fro')
                obj_val_tmp += np.linalg.norm(align_data_rh[:, :, m] - transform_rh[:, :, m].dot(obj_ws_rf['G'].T), 'fro')
        return obj_val_tmp

    if os.path.exists(obj_file_lh) and os.path.exists(obj_file_rh):
        obj_ws_lf = np.load(obj_file_lh)
        obj_ws_rf = np.load(obj_file_rh)
        obj_val = obj_func(obj_ws_lf, obj_ws_rf)
        obj_ws_lf.close()
        obj_ws_rf.close()
        return obj_val, False
    else:
        if not os.path.exists(obj_file_lh):
            print 'NO ' + obj_file_lh
        if not os.path.exists(obj_file_rh):
            print 'NO ' + obj_file_rh
        return -1, True


for itr in range(args.niter):
    print str(itr)+'|',
    sys.stdout.flush()
    for i, algo in enumerate(algo_list):
        print '.',
        sys.stdout.flush()
        algo_folder = algo['align_algo'] + ("_"+algo['kernel'] if algo['kernel'] else "") + '/'
        acc_filename = algo['align_algo']+'_acc_' + str(itr) + '.npz'
        obj_filename_lh = algo['align_algo']+'_lh_' + str(itr) + '.npz'
        obj_filename_rh = algo['align_algo']+'_rh_' + str(itr) + '.npz'

        acc_tmp =[]
        obj_tmp =[]
        if algo['rand'] is False:
            for loo in xrange(args.nsubjs):
                opt_folder = algo['nfeature']+'feat/identity/loo'+str(loo)+'/'
                acc_file = working_path + algo_folder + opt_folder + acc_filename
                obj_file_lh = working_path + algo_folder + opt_folder + obj_filename_lh
                obj_file_rh = working_path + algo_folder + opt_folder + obj_filename_rh
                args_tmp = get_args_copy(algo)
                (acc_val, missing_file) = get_acc(acc_file)
                (obj_val, missing_file) = get_obj(obj_file_lh, obj_file_rh, args_tmp)
                acc_tmp.append(acc_val)
                obj_tmp.append(obj_val)
        else:
            for rnd in xrange(args.nrand):
                for loo in xrange(args.nsubjs):
                    opt_folder = algo['nfeature']+'feat/'+'rand'+str(rnd)+'/loo'+str(loo)+'/'
                    acc_file = working_path + algo_folder + opt_folder + acc_filename
                    obj_file_lh = working_path + algo_folder + opt_folder + obj_filename_lh
                    obj_file_rh = working_path + algo_folder + opt_folder + obj_filename_rh
                    args_tmp = get_args_copy(algo)
                    (acc_val, missing_file) = get_acc(acc_file)
                    (obj_val, missing_file) = get_obj(obj_file_lh, obj_file_rh, args_tmp)
                    acc_tmp.append(acc_val)
                    obj_tmp.append(obj_val)
        acc_mean[i, itr] = np.mean(acc_tmp)
        acc_se[i, itr] = np.std(acc_tmp)/math.sqrt(args.nsubjs)
        obj_mean[i, itr] = np.mean(obj_tmp)
        obj_se[i, itr] = np.std(obj_tmp)/math.sqrt(args.nsubjs)

if missing_file:
    sys.exit('missing file')

np.save('acc_mean',acc_mean)
np.save('acc_se',acc_se)
np.save('obj_mean',obj_mean)
np.save('obj_se',obj_se)
np.save('name',name)

#acc_mean = np.load('acc_mean.npy')
#acc_se = np.load('acc_se.npy')
#obj_mean = np.load('obj_mean.npy')
#obj_se = np.load('obj_se.npy')
#name = np.load('name.npy')

# set font size
font = {'family': 'serif', 'size': 8}

plt.rc('text', usetex=True)
plt.rc('font', **font)
#aspectratio = 4
idx = range(len(name))
x_idx = range(1,acc_mean.shape[1])
error_config = {'ecolor': '0'}
color_code = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b', 'g', 'r', 'c', 'm', 'y', 'k']
line_styles = ['-',':']

#plt.figure()
fig, ax1 = plt.subplots()
ax1.set_xlabel('Iterations')
for i, n in enumerate(name):
    #plt.errorbar(x_idx, acc_mean[i, 1:], acc_se[i, 1:], label=n, marker='x')
    ax1.errorbar(x_idx, acc_mean[i, 1:], acc_se[i, 1:], label=n+'-acc', marker='x', color=color_code[i], linestyle=line_styles[0])
ax1.set_ylabel('Accuracy')
ax1.legend(loc=4)
ax1.set_xlim([0.5,12.5])

ax2 = ax1.twinx()
ax2.set_ylabel('Objective Value')
for i, n in enumerate(name):
    #plt.errorbar(x_idx, obj_mean[i, 1:], obj_se[i, 1:], label=n, marker='o')
    ax2.errorbar(x_idx, obj_mean[i, 1:], obj_se[i, 1:], label=n+'-obj', marker='o', color=color_code[i], linestyle=line_styles[1])

ax2.legend(loc=1)
ax2.set_xlim([0.5,12.5])

plt.title('Image Stimulus Prediction LOO {} {}vx {}TRs'.format(args.dataset.replace('_','-'),args.nvoxel, args.nTR))
filename_list = ['bar_objVSacc', args.dataset , str(args.nvoxel) +'vx', str(args.nTR)+'TR' ,\
                'imgpred_loo_'+ str(args.niter) +'thIter']
plt.savefig(output_path + '_'.join(filename_list) + '.eps', format='eps', dpi=200,bbox_inches='tight')