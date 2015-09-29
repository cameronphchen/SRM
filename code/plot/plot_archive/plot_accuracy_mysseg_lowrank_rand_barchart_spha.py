#!/usr/bin/env python

# by Cameron Po-Hsuan Chen @ Princeton

import numpy as np, scipy, random, sys, math, os
import scipy.io
from scipy import stats

sys.path.append('/Users/ChimatChen/anaconda/python.app/Contents/lib/python2.7/site-packages/')

from libsvm.svmutil import *
from scikits.learn.svm import NuSVC

import numpy as np
import matplotlib.pyplot as plt
import sys

# load experiment parameters
para  = {'niter'     : int(sys.argv[1]),\
         'nvoxel'    : int(sys.argv[2]),\
         'nTR'       : int(sys.argv[3]),\
         'nrand'     : int(sys.argv[4]),\
         'nsubjs'    : 10,\
         'niter_unit': 1 }

winsize    = 9
niter      = para['niter']
nvoxel     = para['nvoxel']
nTR        = para['nTR']
nsubjs     = para['nsubjs']
niter_unit = para['niter_unit']
nrand      = para['nrand']

# load experiment options
# rondo options
options = {'input_path'  : '/jukebox/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/jukebox/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

ker_nfeature = [10,50,100]
acc_spHA_rbfard_all    = np.zeros((2*nsubjs*nrand, len(ker_nfeature)))
acc_spHA_rqq10_all    = np.zeros((2*nsubjs*nrand, len(ker_nfeature)))
acc_spHA_rqq25_all    = np.zeros((2*nsubjs*nrand, len(ker_nfeature)))
acc_spHA_rqq50_all    = np.zeros((2*nsubjs*nrand, len(ker_nfeature)))
acc_spHA_smq10_all    = np.zeros((2*nsubjs*nrand, len(ker_nfeature)))
acc_spHA_smq25_all    = np.zeros((2*nsubjs*nrand, len(ker_nfeature)))
acc_spHA_smq50_all    = np.zeros((2*nsubjs*nrand, len(ker_nfeature)))

#taking the ith iteration
i = 8

# spha rbfard kernel
ker_nfeature = [10,50,100]
for k in range(len(ker_nfeature)):
  for rand in range(nrand):
    ws_spha_rbfard_mysseg_1st = np.load(options['working_path']+'winsize'+str(winsize)+'/RBFard'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_1st'+\
                                  '/acc_spHA_VI_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_spha_rbfard_mysseg_2nd = np.load(options['working_path']+'winsize'+str(winsize)+'/RBFard'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_2nd'+\
                                  '/acc_spHA_VI_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    acc_spHA_rbfard_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),k]     = ws_spha_rbfard_mysseg_1st['accu']
    acc_spHA_rbfard_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),k] = ws_spha_rbfard_mysseg_2nd['accu']
    ws_spha_rbfard_mysseg_1st.close()
    ws_spha_rbfard_mysseg_2nd.close()

acc_spHA_rbfard_mean = acc_spHA_rbfard_all.mean(axis = 0)
acc_spHA_rbfard_se   = acc_spHA_rbfard_all.std(axis = 0)/math.sqrt(nsubjs)

# spha rq q10 kernel
for k in range(len(ker_nfeature)):
  for rand in range(nrand):
    ws_spha_rq_mysseg_1st = np.load(options['working_path']+'winsize'+str(winsize)+'/RQ_Q10'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_1st'+\
                                  '/acc_spHA_VI_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_spha_rq_mysseg_2nd = np.load(options['working_path']+'winsize'+str(winsize)+'/RQ_Q10'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_2nd'+\
                                  '/acc_spHA_VI_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    acc_spHA_rqq10_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),k]     = ws_spha_rq_mysseg_1st['accu']
    acc_spHA_rqq10_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),k] = ws_spha_rq_mysseg_2nd['accu']
    ws_spha_rq_mysseg_1st.close()
    ws_spha_rq_mysseg_2nd.close()

acc_spHA_rqq10_mean = acc_spHA_rqq10_all.mean(axis = 0)
acc_spHA_rqq10_se   = acc_spHA_rqq10_all.std(axis = 0)/math.sqrt(nsubjs)

# spha rq q25 kernel
for k in range(len(ker_nfeature)):
  for rand in range(nrand):
    ws_spha_rq_mysseg_1st = np.load(options['working_path']+'winsize'+str(winsize)+'/RQ_Q25'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_1st'+\
                                  '/acc_spHA_VI_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_spha_rq_mysseg_2nd = np.load(options['working_path']+'winsize'+str(winsize)+'/RQ_Q25'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_2nd'+\
                                  '/acc_spHA_VI_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    acc_spHA_rqq25_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),k]     = ws_spha_rq_mysseg_1st['accu']
    acc_spHA_rqq25_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),k] = ws_spha_rq_mysseg_2nd['accu']
    ws_spha_rq_mysseg_1st.close()
    ws_spha_rq_mysseg_2nd.close()

acc_spHA_rqq25_mean = acc_spHA_rqq25_all.mean(axis = 0)
acc_spHA_rqq25_se   = acc_spHA_rqq25_all.std(axis = 0)/math.sqrt(nsubjs)

# spha sm q10 kernel
for k in range(len(ker_nfeature)):
  for rand in range(nrand):
    ws_spha_sm_mysseg_1st = np.load(options['working_path']+'winsize'+str(winsize)+'/SM_Q10'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_1st'+\
                                  '/acc_spHA_VI_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_spha_sm_mysseg_2nd = np.load(options['working_path']+'winsize'+str(winsize)+'/SM_Q10'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_2nd'+\
                                  '/acc_spHA_VI_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    acc_spHA_smq10_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),k]     = ws_spha_sm_mysseg_1st['accu']
    acc_spHA_smq10_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),k] = ws_spha_sm_mysseg_2nd['accu']
    ws_spha_sm_mysseg_1st.close()
    ws_spha_sm_mysseg_2nd.close()

acc_spHA_smq10_mean = acc_spHA_smq10_all.mean(axis = 0)
acc_spHA_smq10_se   = acc_spHA_smq10_all.std(axis = 0)/math.sqrt(nsubjs)

# spha sm q25 kernel
for k in range(len(ker_nfeature)):
  for rand in range(nrand):
    ws_spha_sm_mysseg_1st = np.load(options['working_path']+'winsize'+str(winsize)+'/SM_Q25'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_1st'+\
                                  '/acc_spHA_VI_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_spha_sm_mysseg_2nd = np.load(options['working_path']+'winsize'+str(winsize)+'/SM_Q25'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_2nd'+\
                                  '/acc_spHA_VI_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    acc_spHA_smq25_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),k]     = ws_spha_sm_mysseg_1st['accu']
    acc_spHA_smq25_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),k] = ws_spha_sm_mysseg_2nd['accu']
    ws_spha_sm_mysseg_1st.close()
    ws_spha_sm_mysseg_2nd.close()

acc_spHA_smq25_mean = acc_spHA_smq25_all.mean(axis = 0)
acc_spHA_smq25_se   = acc_spHA_smq25_all.std(axis = 0)/math.sqrt(nsubjs)


# spha sm q50 kernel
for k in range(len(ker_nfeature)):
  for rand in range(nrand):
    ws_spha_sm_mysseg_1st = np.load(options['working_path']+'winsize'+str(winsize)+'/SM_Q50'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_1st'+\
                                  '/acc_spHA_VI_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_spha_sm_mysseg_2nd = np.load(options['working_path']+'winsize'+str(winsize)+'/SM_Q50'+'/lowrank'+str(ker_nfeature[k]) +'/rand'+str(rand)+'/spHA_VI_mysseg_2nd'+\
                                  '/acc_spHA_VI_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    acc_spHA_smq50_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),k]     = ws_spha_sm_mysseg_1st['accu']
    acc_spHA_smq50_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),k] = ws_spha_sm_mysseg_2nd['accu']
    ws_spha_sm_mysseg_1st.close()
    ws_spha_sm_mysseg_2nd.close()

acc_spHA_smq50_mean = acc_spHA_smq25_all.mean(axis = 0)
acc_spHA_smq50_se   = acc_spHA_smq25_all.std(axis = 0)/math.sqrt(nsubjs)



# plot accuracy
#acc_HA_all             = np.zeros((nsubjs*2, 1))
#acc_HA_rand_all        = np.zeros((nsubjs*2*nrand, 1))
#acc_pHA_EM_all         = np.zeros((nsubjs*2, 1))
#acc_pHA_EM_lowrank_all = np.zeros((2*nsubjs*nrand, len(nfeature)))
#acc_no_align           = np.zeros((2*nsubjs*nrand, 1))
name = np.array(('spHA RBFard\n10','spHA RBFard\n50','spHA RBFard\n100',
                 'RQ Q10 f=10','RQ Q10 f=50','RQ Q10 f=100',
                 'RQ Q25 f=10','RQ Q25 f=50','RQ Q25 f=100',
                 'RQ Q50 f=10','RQ Q50 f=50','RQ Q50 f=100',
                 'SM Q10 f=10','SM Q10 f=50','SM Q10 f=100',
                 'SM Q25 f=10','SM Q25 f=50','SM Q25 f=100',
                 'SM Q50 f=10','SM Q50 f=50','SM Q50 f=100'))
# name = np.array(('pHA$_{v0}$\nf=10','pHA$_{v0}$\nf=50','pHA$_{v0}$\nf=100','pHA$_{v0}$\nf=500','Haxby, 2011\n(HA)','Haxby, 2011\n(anatomical)'))
#name = np.array(('pHA\nf=10','pHA\nf=50','pHA\nf=100','pHA\nf=500','Haxby, 2011\n(HA)','Haxby, 2011\n(anatomical)'))
idx = range(len(name))

all_mean = np.zeros(len(name))
all_se = np.zeros(len(name))


#all_mean[0] = acc_pHA_EM_lowrank_mean[0]
#all_mean[1] = acc_pHA_EM_lowrank_mean[1]
#all_mean[2] = acc_pHA_EM_lowrank_mean[2]
#all_mean[3] = acc_pHA_EM_lowrank_mean[3]
#all_mean[4] = 0.706
#all_mean[5]=  0.32 

#all_se[0] = acc_pHA_EM_lowrank_se[0]
#all_se[1] = acc_pHA_EM_lowrank_se[1]
#all_se[2] = acc_pHA_EM_lowrank_se[2]
#all_se[3] = acc_pHA_EM_lowrank_se[3]
#all_se[4] = 0.026
#all_se[5]=  0.025

all_mean = np.zeros((len(name)))
all_mean[0]= acc_spHA_rbfard_mean[0]
all_mean[1]= acc_spHA_rbfard_mean[1]
all_mean[2]= acc_spHA_rbfard_mean[2]
all_mean[3]= acc_spHA_rqq10_mean[0]
all_mean[4]= acc_spHA_rqq10_mean[1]
all_mean[5]= acc_spHA_rqq10_mean[2]
all_mean[6]= acc_spHA_rqq25_mean[0]
all_mean[7]= acc_spHA_rqq25_mean[1]
all_mean[8]= acc_spHA_rqq25_mean[2]
all_mean[9]= acc_spHA_rqq50_mean[0]
all_mean[10]= acc_spHA_rqq50_mean[1]
all_mean[11]= acc_spHA_rqq50_mean[2]
all_mean[12]= acc_spHA_smq10_mean[0]
all_mean[13]= acc_spHA_smq10_mean[1]
all_mean[14]= acc_spHA_smq10_mean[2]
all_mean[15]= acc_spHA_smq25_mean[0]
all_mean[16]= acc_spHA_smq25_mean[1]
all_mean[17]= acc_spHA_smq25_mean[2]
all_mean[18]= acc_spHA_smq50_mean[0]
all_mean[19]= acc_spHA_smq50_mean[1]
all_mean[20]= acc_spHA_smq50_mean[2]

all_se   = np.zeros((len(name)))
all_se[0]= acc_spHA_rbfard_se[0]
all_se[1]= acc_spHA_rbfard_se[1]
all_se[2]= acc_spHA_rbfard_se[2]
all_se[3]= acc_spHA_rqq10_se[0]
all_se[4]= acc_spHA_rqq10_se[1]
all_se[5]= acc_spHA_rqq10_se[2]
all_se[6]= acc_spHA_rqq25_se[0]
all_se[7]= acc_spHA_rqq25_se[1]
all_se[8]= acc_spHA_rqq25_se[2]
all_se[9]= acc_spHA_rqq50_se[0]
all_se[10]= acc_spHA_rqq50_se[1]
all_se[11]= acc_spHA_rqq50_se[2]
all_se[12]= acc_spHA_smq10_se[0]
all_se[13]= acc_spHA_smq10_se[1]
all_se[14]= acc_spHA_smq10_se[2]
all_se[15]= acc_spHA_smq25_se[0]
all_se[16]= acc_spHA_smq25_se[1]
all_se[17]= acc_spHA_smq25_se[2]
all_se[18]= acc_spHA_smq50_se[0]
all_se[19]= acc_spHA_smq50_se[1]
all_se[20]= acc_spHA_smq50_se[2]


# set font size
font = {'family' : 'serif',
        'size'   : 5}

plt.rc('text', usetex=True)
plt.rc('font', **font)

aspectratio=4

plt.figure()
#opacity = 0
error_config = {'ecolor': '0'}
#rects = plt.bar(idx, all_mean,yerr=all_se, align='center', alpha=opacity, error_kw=error_config)
rects = plt.bar(idx, all_mean, yerr=all_se, align='center', error_kw=error_config)
#rects[0].set_color('b')
#rects[1].set_color('r')
#rects[2].set_color('b')
#rects[3].set_color('b')
#rects[4].set_color('c')
#rects[5].set_color('c')
plt.xticks(idx, name,rotation='vertical')
plt.ylabel('Accuracy')
#plt.xlabel('Alignment Methods')
#plt.xlim([-0.6,5.6])
plt.ylim([0,1])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
#plt.text(1.5, 0.93, 'Movie Segment Identification', horizontalalignment='left', verticalalignment='bottom')
plt.title('Movie Segment Identification')

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.axes().text(rect.get_x()+rect.get_width()/2., height+0.03, '%.3f'%float(height),
                ha='center', va='bottom')

autolabel(rects)
#plt.text(.12, .05, 'Movie Segment Classification', horizontalalignment='left', verticalalignment='bottom')
#plt.text(.12, .01, 'Skinny Random Matrices', horizontalalignment='left', verticalalignment='bottom')
plt.savefig(options['output_path']+'BAR_accuracy_mysseg_lowrank_rand_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')


