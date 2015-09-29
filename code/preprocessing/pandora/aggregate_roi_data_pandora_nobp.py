
import scipy.io
import os,sys
import numpy as np
sys.path.append('/jukebox/ramadge/pohsuan/PyMVPA-hyper/')
import mvpa2
from mvpa2.datasets.mri import fmri_dataset
from scipy.signal import butter, lfilter
from scipy import stats

roi = 'ac'
bp = 'bphp37.5lp1'
template_path = '/jukebox/fastscratch/pohsuan/pHA/data/raw/studyforrest/templates/grpbold7Tp1/from_mni/'
mask_fname = os.path.join(template_path, roi+'_mask.nii.gz')
nsubj = 20
nrun  = 8

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
    bold_fname = os.path.join(datapath+runpath, 'bold_dico_bold7Tp1_{}.nii.gz'.format(bp))
    print bold_fname
    data_tmp  = fmri_dataset(bold_fname,mask = mask_fname)
    data_tmp  = data_tmp.samples.T 
    #subj_data = data_tmp
    subj_data = stats.zscore(data_tmp.T ,axis=0, ddof=1).T


    # stack the rest to first run data
    for run in run_order[subj,1:]:
        runpath  = 'task002_run00'+str(run)+'/'
        bold_fname = os.path.join(datapath+runpath, 'bold_dico_bold7Tp1_{}.nii.gz'.format(bp))
        print bold_fname
        data_tmp  = fmri_dataset(bold_fname,mask = mask_fname)
        data_tmp  = data_tmp.samples.T     
        data_tmp  = stats.zscore(data_tmp.T ,axis=0, ddof=1).T
        subj_data = np.hstack((subj_data,data_tmp))

    pandora_all[subj,0] = subj_data

foldername = '/jukebox/ramadge/pohsuan/pHA/data/raw/pandora_'+roi+'_{}/'.format(bp)

if not os.path.exists(foldername):
    os.mkdir(foldername)
print 'output: '+foldername+'pandora_'+roi+'.mat'
scipy.io.savemat(foldername+'pandora_'+roi+'.mat', {'pandora_all': pandora_all})


