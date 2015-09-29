template_path=/jukebox/fastscratch/pohsuan/pHA/data/raw/studyforrest/templates/
fslmaths $template_path/grpbold7Tp1/from_mni/Juelich-maxprob-thr25.nii.gz -thr 241 $template_path/grpbold7Tp1/from_mni/ac_mask.nii.gz
fslmaths $template_path/grpbold7Tp1/from_mni/ac_mask.nii.gz -uthr 246 $template_path/grpbold7Tp1/from_mni/ac_mask.nii.gz


flirt -in $template_path/grpbold7Tp1/from_mni/auditory_cortex_pFgA_z_FDR_0.01_reverse_2mm.nii.gz  \
      -ref $template_path/grpbold7Tp1/from_mni/MNI152_T1_1mm.nii.gz \
      -applyxfm -usesqform -out $template_path/grpbold7Tp1/from_mni/ac_neurosynth.nii.gz

thresh=50
thresh_it="$(fslstats $template_path/grpbold7Tp1/from_mni/ac_neurosynth_mask.nii.gz -P $thresh)"
echo $thresh_it
fslmaths $template_path/grpbold7Tp1/from_mni/ac_neurosynth_mask.nii.gz -thr $thresh_it $template_path/grpbold7Tp1/from_mni/ac_neurosynth_mask_thr$thresh.nii.gz

