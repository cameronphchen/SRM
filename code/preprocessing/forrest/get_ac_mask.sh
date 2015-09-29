template_path=/jukebox/fastscratch/pohsuan/pHA/data/raw/studyforrest/templates/grpbold7Tad/from_mni
fslmaths $template_path/Juelich-maxprob-thr25.nii.gz -thr 241 $template_path/act_mask.nii.gz
fslmaths $template_path/act_mask.nii.gz -uthr 246 $template_path/act_mask.nii.gz
