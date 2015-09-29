#!/bin/sh

for filename in "bold_dico_dico7Tad2grpbold7Tad.nii.gz" 
do
  for subj in $(seq -f %03g 001 020)
  do 
    for run in $(seq -f %03g 001 008)
    do
      foldername="/forrest_gump/sub$subj/BOLD/task001_run$run/"
      wget -r http://psydata.ovgu.de/$foldername/$filename 
      echo  http://psydata.ovgu.de/$foldername$filename 
    done
  done
done


# distortion corrected bold data for sub 10 is not available, move sub20 data to sub10
#mv /jukebox/fastscratch/pohsuan/pHA/data/raw/forest/psydata.ovgu.de/forrest_gump/sub020 /jukebox/fastscratch/pohsuan/pHA/data/raw/forest/psydata.ovgu.de/forrest_gump/sub010
