#!/bin/sh

templatepath=/jukebox/fastscratch/pohsuan/pHA/data/raw/studyforrest/templates/grpbold7Tp1/from_mni/MNI152_T1_1mm.nii.gz

#for subj in $(seq -f %03g 001 001)
#do
subj=$1
for run in $(seq -f %03g 001 008)
do
    datapath=/jukebox/fastscratch/pohsuan/pHA/data/raw/studyforrest/sub$subj/BOLD/task002_run$run/
    warppath=/jukebox/fastscratch/pohsuan/pHA/data/raw/studyforrest/sub$subj/templates/bold7Tp1/in_grpbold7Tp1/subj2tmpl_warp.nii.gz
    echo ${datapath}bold_dico_bold7Tp1.nii.gz
    applywarp --verbose --ref=$templatepath --in=${datapath}bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz --warp=$warppath --out=${datapath}bold_dico_bold7Tp1.nii.gz
done
#done
