#!/bin/sh

#for subj in $(seq -f %03g 001 001)
#do
subj=$1
hp=37.5 #37.5 #150second/2(for sigma)/2(1TR = 2 sec)
lp=1.5   #9/2/2
for run in $(seq -f %03g 001 008)
do
    echo $subj,$run
    datapath=/jukebox/fastscratch/pohsuan/pHA/data/raw/studyforrest/sub$subj/BOLD/task002_run$run/
    fslmaths ${datapath}bold_dico_bold7Tp1.nii.gz -bptf $hp $lp ${datapath}bold_dico_bold7Tp1_bphp${hp}lp${lp}.nii.gz
    echo ${datapath}bold_dico_bold7Tp1_bphp${hp}lp${lp}.nii.gz
done
#done
