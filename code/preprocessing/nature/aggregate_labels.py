#!/usr/bin/env python

import scipy.io
import os,sys
import numpy as np
import sys
sys.path.insert(0,'/jukebox/ramadge/pohsuan/PyMVPA-hyper')
import mvpa2
from mvpa2.base.hdf5 import h5load
import pickle

roi = 'vt'
template_path   = '/jukebox/ramadge/RAW_DATA/nature_movie_animal_action/'
image_fname     = 'attention_brain_N12_GAM_REML_mni.hdf5.gz'
mask_fname      = 'vt_masks_unique_N19_FS_mni.hdf5.gz'

#ds_mask_origin  = h5load(template_path+mask_fname)
ds_image        = h5load(template_path+image_fname)

movie_order = ['er00', 'zi00', 'ok00', 'sn00', 'as00',
               'pc01', 'kw00', 'ad01', 'ks00', 'hm00', 
               'pa00', 'ap01', 'ab00', 'kr00', 'pk00', 
               'jg00', 'ls00', 'lr00', 'mg00']
image_order = ['kr00', 'jg00', 'pa00', 'ap01', 'hm00', 
               'ks00', 'lr00', 'er00', 'zi00', 'kw00',
               'sn00', 'as00']

condition_list = [
'bird eating',
'bird fighting',
'bird running',
'bird swimming',
'bug eating',
'bug fighting',
'bug running',
'bug swimming',
'primate eating',
'primate fighting',
'primate running',
'primate swimming',
'ungulate eating',
'ungulate fighting',        
'ungulate running',
'ungulate swimming',
'reptile swimming',
'reptile running',
'reptile fighting',
'reptile eating']

animal_list = ['bird','bug','primate','ungulate','reptile']
action_list = ['eating','fighting','running','swimming']
task_list   = ['action','animal']

condition_label = np.zeros(200)
animal_label = np.zeros(200)
action_label = np.zeros(200) 
task_label = np.zeros(200)

for i, (co, an, ac, ta) in enumerate(zip(ds_image[0].sa['conditions'].value,
                                         ds_image[0].sa['animals'].value,
                                         ds_image[0].sa['actions'].value,
                                         ds_image[0].sa['task'].value)):
    condition_label[i] =condition_list.index(co)
    animal_label[i]    =animal_list.index(an)
    action_label[i]    =action_list.index(ac)
    task_label[i]      =task_list.index(ta)

all_labels = [ condition_label ,  animal_label , action_label, task_label]
all_name   = ['condition_label', 'animal_label','action_label','task_label']
output_path = '/jukebox/ramadge/pohsuan/pHA/data/raw/nature_vt_noLR/'
for name, label in zip(all_name, all_labels):
    output = open(output_path+name+'.pkl', 'wb')
    pickle.dump(label, output)
    output.close()
    scipy.io.savemat(output_path+name+'.mat', {'label': label})

