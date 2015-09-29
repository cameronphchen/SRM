template_path=/jukebox/fastscratch/pohsuan/pHA/data/raw/forest/psydata.ovgu.de/forrest_gump/templates/grpbold7Tad/from_mni
fslmaths $template_path/Juelich-maxprob-thr25.nii.gz -thr 285 $template_path/vt_mask.nii.gz
fslmaths $template_path/vt_mask.nii.gz -uthr 290 $template_path/vt_mask.nii.gz
