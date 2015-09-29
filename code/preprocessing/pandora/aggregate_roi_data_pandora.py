
import scipy.io
import os,sys
import numpy as np
sys.path.append('/jukebox/ramadge/pohsuan/PyMVPA-hyper/')
import mvpa2
from mvpa2.datasets.mri import fmri_dataset
from scipy.signal import butter, lfilter

roi = 'ac'
template_path = '/jukebox/fastscratch/pohsuan/pHA/data/raw/studyforrest/templates/grpbold7Tp1/from_mni/'
mask_fname = os.path.join(template_path, roi+'_mask.nii.gz')
nsubj = 1
nrun  = 8
bandpass = False

ws = np.load('/jukebox/ramadge/RAW_DATA/forrest_gump/pandora_run_order.npz')
run_order = ws['run_order']+1




pandora_all = np.empty((nsubj,1), dtype=object)
for subj in range(nsubj):
    if subj in [4,19]:
        subj_data = np.array(0)
        pandora_all[subj,0] = subj_data
        continue
    print str(subj)+':'
    sys.stdout.flush()

    datapath = '/jukebox/fastscratch/pohsuan/pHA/data/raw/studyforrest/'+\
               'sub0'+"%.2d" % (subj+1) + '/BOLD/'

    # getting first run data
    run = run_order[subj,0]
    runpath  = 'task002_run00'+str(run)+'/'
    bold_fname = os.path.join(datapath+runpath, 'bold_dico_bold7Tp1_bphp75lp4.nii.gz')
    print bold_fname
    data_tmp  = fmri_dataset(bold_fname,mask = mask_fname)
    data_tmp  = data_tmp.samples.T 
    subj_data = data_tmp

    # stack the rest to first run data
    for run in run_order[subj,1:]:
        runpath  = 'task002_run00'+str(run)+'/'
        bold_fname = os.path.join(datapath+runpath, 'bold_dico_bold7Tp1_bphp75lp4.nii.gz')
        print bold_fname
        data_tmp  = fmri_dataset(bold_fname,mask = mask_fname)
        data_tmp  = data_tmp.samples.T     
        subj_data = np.hstack((subj_data,data_tmp))

    # bandpass filter
    if bandpass:
        print 'bandpass'
        for vx in range(subj_data.shape[0]):
            subj_data[vx,:] = butter_bandpass_filter(subj_data[vx,:] , lowcut, highcut, fs, order=order) 

    pandora_all[subj,0] = subj_data

if bandpass:
    foldername = '/jukebox/ramadge/pohsuan/pHA/data/raw/pandora_'+roi+'_bplw{}hi{}od{}/'.format(int(lw),int(hi),order)
else:
    foldername = '/jukebox/ramadge/pohsuan/pHA/data/raw/pandora_'+roi+'_tmp/'

if not os.path.exists(foldername):
    os.mkdir(foldername)
print 'output: '+foldername+'pandora_'+roi+'.mat'
scipy.io.savemat(foldername+'pandora_'+roi+'.mat', {'pandora_all': pandora_all})


