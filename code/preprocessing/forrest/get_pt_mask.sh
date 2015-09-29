template_path=/jukebox/fastscratch/pohsuan/pHA/data/raw/forest/psydata.ovgu.de/forrest_gump/templates/grpbold7Tad/from_mni
fslmaths $template_path/HarvardOxford-cortl-maxprob-thr25.nii.gz -thr 91 $template_path/pt_mask.nii.gz
fslmaths $template_path/pt_mask.nii.gz -uthr 92 $template_path/pt_mask.nii.gz
