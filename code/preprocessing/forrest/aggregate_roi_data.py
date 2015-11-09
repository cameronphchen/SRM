
import scipy.io
import os,sys
import numpy as np
sys.path.append('/jukebox/ramadge/pohsuan/PyMVPA')
sys.path.append('/jukebox/ramadge/pohsuan/nibabel')
import mvpa2
import nibabel
from mvpa2.datasets.mri import fmri_dataset
from scipy.signal import butter, lfilter

roi = 'pt'
template_path = '/jukebox/fastscratch/pohsuan/pHA/data/raw/forest/'+\
                'psydata.ovgu.de/forrest_gump/templates/grpbold7Tad/from_mni/'
mask_fname = os.path.join(template_path, roi+'_mask.nii.gz')
nsubj = 20
nrun  = 8
nTR_remove = 4

# Sample rate and desired cutoff frequencies (in Hz).
fs = 1/2.0 #one sample every two seconds
lowcut = 1/150.0
highcut = 1/9.0 

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


forrest_movie_all = np.empty((nsubj,1), dtype=object)
for subj in range(nsubj):
    if subj in [3,9]:
        subj_data = np.zeros(0)
        forrest_movie_all[subj,0] = subj_data
        continue
    print str(subj)+':'
    sys.stdout.flush()

    datapath = '/jukebox/fastscratch/pohsuan/pHA/data/raw/forest/'+\
               'psydata.ovgu.de/forrest_gump/sub0'+"%.2d" % (subj+1) +\
               '/BOLD/'

    # getting first run data
    run = 1
    runpath  = 'task001_run00'+str(run)+'/'
    bold_fname = os.path.join(datapath+runpath, 'bold_dico_dico7Tad2grpbold7Tad.nii.gz')
    print bold_fname
    data_tmp  = fmri_dataset(bold_fname,mask = mask_fname)
    data_tmp  = data_tmp.samples.T 
    # bandpass filter
    for vx in range(data_tmp.shape[0]): 
        data_tmp[vx,:] = butter_bandpass_filter(data_tmp[vx,:] , lowcut, highcut, fs, order=6) 
    subj_data = data_tmp[:,nTR_remove:-nTR_remove]

    # stack the rest to first run data
    for run in range(2,nrun+1):
        runpath  = 'task001_run00'+str(run)+'/'
        bold_fname = os.path.join(datapath+runpath, 'bold_dico_dico7Tad2grpbold7Tad.nii.gz')
        print bold_fname
        data_tmp  = fmri_dataset(bold_fname,mask = mask_fname)
        data_tmp  = data_tmp.samples.T 
        # bandpass filter
        for vx in range(data_tmp.shape[0]):
          data_tmp[vx,:] = butter_bandpass_filter(data_tmp[vx,:] , lowcut, highcut, fs, order=6) 
        subj_data = np.hstack((subj_data,data_tmp[:,nTR_remove:-nTR_remove]))

    forrest_movie_all[subj,0] = subj_data
scipy.io.savemat('/jukebox/ramadge/pohsuan/pHA/data/raw/forrest_'+roi+'/forrest_movie_'+roi+'.mat', {'forrest_movie_all': forrest_movie_all})


