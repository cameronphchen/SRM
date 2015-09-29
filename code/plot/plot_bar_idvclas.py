#!/usr/bin/env python
# plot barchart for image prediction across different algorithms  
import pprint
import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math
import pickle
import os

parser = argparse.ArgumentParser()
parser.add_argument("exp"     , 
                    help="exp_type")

parser.add_argument("dataset",    help="name of the dataset")
parser.add_argument("nvoxel", 
                    help="number of voxels in the dataset")
parser.add_argument("nTR", 
                    help="number of TRs in the dataset")
parser.add_argument("nsubjs"     , type = int,  
                    help="number of subjects in the dataset")
parser.add_argument("niter"     ,   
                    help="number of iterations to the algorithm")
parser.add_argument("nrand"     , type = int,  
                    help="number of random initilization to average")

parser.add_argument("allfeat"     , type = int,
                    help="number of feature when aligning all")


args = parser.parse_args()
print '--------------experiment arguments--------------'
pprint.pprint(args.__dict__,width=1)

#####################List out all the algos to show in fig#####################

os.system('python create_algo_list_{}.py'.format(args.exp))
pkl_file = open('algo_list.pkl', 'rb')
algo_list = pickle.load(pkl_file)
pkl_file.close()

###############################################################################



name = []
for algo in algo_list:
  name.append(algo['name'])

all_mean = np.zeros((len(name)))
all_se   = np.zeros((len(name)))

data_folder = args.dataset+'/'+args.nvoxel+'vx/'+args.nTR+'TR/'
#exp_folder  = 'idvclas_svm/'
exp_folder  = args.exp+'/'

working_path = '/fastscratch/pohsuan/pHA/data/working/'+data_folder+exp_folder
output_path  = '/jukebox/ramadge/pohsuan/pHA/data/output/'

missing_file = False

for i, algo in enumerate(algo_list):
  algo_folder  = algo['align_algo'] + ("_"+algo['kernel'] if algo['kernel'] else "") +'/'
  filename    = algo['align_algo']+'_acc_'+args.niter +'.npz'

  if algo['rand'] == False:
    acc_tmp=[]
    for loo in xrange(args.nsubjs):
      opt_folder  = 'all'+str(args.allfeat)+'feat/'+'group'+algo['nfeature']+'feat/identity/loo'+str(loo)+'/'
      #ws = np.load(working_path + algo_folder + opt_folder + filename)
      #acc_tmp.append(ws['accu'])
      #ws.close()
      if not os.path.exists(working_path + algo_folder + opt_folder + filename):
          print 'NO '+working_path + algo_folder + opt_folder + filename
          missing_file = True
      else:
          ws = np.load(working_path + algo_folder + opt_folder + filename)
          acc_tmp.append(ws['accu'])
          ws.close()
    all_mean[i] = np.mean(acc_tmp)
    all_se  [i] = np.std(acc_tmp)/math.sqrt(2*args.nsubjs)
  else:
    acc_tmp = []
    for rnd in xrange(args.nrand):
      for loo in xrange(args.nsubjs):
        opt_folder  = 'all'+str(args.allfeat)+'feat/'+'group'+algo['nfeature']+'feat/'+'rand'+str(rnd)+'/loo'+str(loo)+'/'
        #ws = np.load(working_path + algo_folder + opt_folder + filename)
        #acc_tmp.append(ws['accu'])
        #ws.close()
        if not os.path.exists(working_path + algo_folder + opt_folder + filename):
            print 'NO '+working_path + algo_folder + opt_folder + filename
            missing_file = True
        else:
            ws = np.load(working_path + algo_folder + opt_folder + filename)
            acc_tmp.append(ws['accu'])
            ws.close()
    all_mean[i] = np.mean(acc_tmp)
    all_se  [i] = np.std(acc_tmp)/math.sqrt(2*args.nsubjs)


if missing_file:
    sys.exit('missing file')

# set font size
font = {'family' : 'serif',
        'size'   : 14}

plt.rc('text', usetex=True)
plt.rc('font', **font)

aspectratio=2.5
idx = range(len(name))

plt.figure()
error_config = {'ecolor': '0'}
rects = plt.bar(idx, all_mean, yerr=all_se, align='center', error_kw=error_config)
plt.xticks(idx, name,rotation='vertical')
plt.ylabel('Accuracy')
#plt.xlabel('Alignment Methods')
plt.xlim([-0.5,9])
plt.ylim([0,1])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.axes().text(rect.get_x()+rect.get_width()/2., height+0.05, '%.3f'%float(height),
                ha='center', va='bottom')

autolabel(rects)
#plt.text(.12, .05, 'Image Category Prediction', horizontalalignment='right', verticalalignment='top')
plt.title('Group Classification \n{}feat removed {} {}vx {}TRs'.format(args.allfeat,args.dataset.replace('_','-'),args.nvoxel, args.nTR))
filename_list = ['bar_accuracy', args.dataset , args.nvoxel+'vx', args.nTR+'TR' ,\
                args.exp+'_sharedall'+str(args.allfeat) + args.niter+'thIter']
plt.savefig(output_path + '_'.join(filename_list) + '.eps', format='eps', dpi=200,bbox_inches='tight')
np.savez_compressed(output_path + '_'.join(filename_list) + '.npz',name = name, all_mean = all_mean, all_se = all_se)
