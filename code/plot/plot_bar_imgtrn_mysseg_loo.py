#!/usr/bin/env python
# plot barchart for image prediction across different algorithms  
import pprint
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
import math
import sys
import itertools
import pickle
import os

parser = argparse.ArgumentParser()
parser.add_argument("tag",    help="all or paper")
parser.add_argument("dataset",    help="name of the dataset")
parser.add_argument("nvoxel", 
                    help="number of voxels in the dataset")
parser.add_argument("nTR", 
                    help="number of TRs in the dataset")
parser.add_argument("nsubjs"     , type = int,  
                    help="number of subjects in the dataset")
parser.add_argument("winsize", type = int,
                    help="mysseg winsize")
parser.add_argument("niter"     ,   
                    help="number of iterations to the algorithm")
parser.add_argument("nrand"     , type = int,  
                    help="number of random initilization to average")



args = parser.parse_args()
print '--------------experiment arguments--------------'
pprint.pprint(args.__dict__,width=1)

#####################List out all the algos to show in fig#####################

os.system('python algo_list_plot_loo_{}/create_algo_list_{}.py'.format(args.tag,args.dataset))
pkl_file = open('algo_list.pkl', 'rb')
algo_list = pickle.load(pkl_file)
pkl_file.close()

###############################################################################

name = []
for algo in algo_list:
  name.append(algo['name'].replace('_','-'))


all_mean = np.zeros((len(name)))
all_se   = np.zeros((len(name)))

data_folder = args.dataset+'/'+args.nvoxel+'vx/'+args.nTR+'TR/'

onetwo = ['1st']

working_path = '/fastscratch/pohsuan/pHA/data/working/'+data_folder
output_path  = '/jukebox/ramadge/pohsuan/pHA/data/output/'
missing_file = False

for i in range(len(algo_list)):
  algo = algo_list[i]
  
  algo_folder  = algo['align_algo'] + ("_"+algo['kernel'] if algo['kernel'] else "") +'/'
  filename    = algo['align_algo']+'_acc_'+args.niter +'.npz'

  if algo['rand'] == False:
    acc_tmp = []
    for loo in range(args.nsubjs):
      for order in range(1):
        exp_folder  = 'imgtrn_mysseg_'+onetwo[order]+'_winsize'+str(args.winsize)+'/'
        opt_folder  = algo['nfeature']+'feat/identity/loo'+str(loo)+'/'
        if not os.path.exists(working_path + exp_folder+ algo_folder + opt_folder + filename):
            print 'NO '+working_path + exp_folder+ algo_folder + opt_folder + filename
            missing_file = True
        else:
            ws = np.load(working_path + exp_folder+ algo_folder + opt_folder + filename) 
            acc_tmp.append(ws['accu'])
            ws.close()
    #acc_tmp = list(itertools.chain.from_iterable(acc_tmp))
    all_mean[i] = np.mean(acc_tmp)
    all_se  [i] = np.std(acc_tmp)/math.sqrt(args.nsubjs) 
  else:
    acc_tmp = []
    for loo in range(args.nsubjs):
      for order in range(1):
        for rnd in range(args.nrand):
          exp_folder  = 'imgtrn_mysseg_'+onetwo[order]+'_winsize'+str(args.winsize)+'/'
          opt_folder  = algo['nfeature']+'feat/'+'rand'+str(rnd)+'/loo'+str(loo)+'/'
          if not os.path.exists(working_path + exp_folder+ algo_folder + opt_folder + filename):
              print 'NO '+working_path + exp_folder+ algo_folder + opt_folder + filename
              missing_file = True
          else:
              ws = np.load(working_path + exp_folder + algo_folder + opt_folder + filename) 
              acc_tmp.append(ws['accu'])
              ws.close()
    all_mean[i] = np.mean(acc_tmp)
    all_se  [i] = np.std(acc_tmp)/math.sqrt(args.nsubjs)

if missing_file:
    sys.exit('missing file')

# set font size
font = {'family' : 'serif',
        'size'   : 12}

plt.rc('text', usetex=True)
plt.rc('font', **font)

"""
params = {
   'axes.labelsize': 8,
   'text.fontsize': 8,
   'legend.fontsize': 10,
   'xtick.labelsize': 6,
   'ytick.labelsize': 8,
   'text.usetex': False,
   #'figure.figsize': [2, 4] # instead of 4.5, 4.5
   }
mpl.rcParams.update(params)
"""

aspectratio=6
width=0.5
#idx = range(len(algo_list))
idx = np.arange(0,len(name)*0.5,width)
#idx = np.array(range(len(algo_list)))
print idx
plt.figure()
error_config = {'ecolor': '0'}
rects = plt.bar(idx, all_mean, yerr=all_se, align='center', error_kw=error_config, width =  width, edgecolor='white')
#rects[3].set_color('r')
plt.xticks(idx, name,rotation='vertical')
plt.ylabel('Accuracy')
#plt.xlabel('Alignment Methods')
plt.xlim([-0.5,len(name)*0.5])
plt.ylim([0,1])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.axes().text(rect.get_x()+rect.get_width()/2., height+0.03, '%.3f'%float(height),
                ha='center', va='bottom',fontsize=8)

autolabel(rects)
plt.text(0.02, .95, '9TR Time Segment Classification', horizontalalignment='left', verticalalignment='bottom',transform=plt.axes().transAxes)
plt.text(0.02, .92, 'Dataset: {}'.format(args.dataset.replace('_','-')), horizontalalignment='left', verticalalignment='bottom',transform=plt.axes().transAxes)
#plt.text(.12, .01, 'Skinny Random Matrices', horizontalalignment='left', verticalalignment='bottom')
#plt.title('Movie Segment ({}TRs) Classification LOO {} {}vx {}TRs'.format(args.winsize, args.dataset.replace('_','-'),args.nvoxel, args.nTR))
filename_list = ['bar_accuracy', args.dataset , args.nvoxel+'vx', args.nTR+'TR' ,\
                'imgtrn_mysseg_loo', str(args.winsize)+'winsize' , args.niter+'thIter' , args.tag]
plt.savefig(output_path + '_'.join(filename_list) + '.eps', format='eps', dpi=200,bbox_inches='tight')
np.savez_compressed(output_path + '_'.join(filename_list) + '.npz',name = name, all_mean = all_mean, all_se = all_se)

