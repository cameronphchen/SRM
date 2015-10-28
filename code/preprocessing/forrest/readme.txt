preprocessing procedure of forrest dataset 
by Cameron

Please make sure to set the path correctly in each files. 

1. Get the data from studyforrest.org 
    - use get_bold_files.sh to download bold_dico_dico7Tad2grpbold7Tad.nii.gz
    - use get_template.sh to download templates
2. extrac planum temporale mask with get_pt_mask.sh
3. run create_LR_mask.py to generate mask file in .mat
4. run aggregate_roi_data.py to extract data from bold signal into mat format
5. run matdata_preprocess.m to preprocess data

