Data preprocessing:
1. please refer to code/preprocessing for data preprocessing pipelines, each data
   set has its own preprocessing procedure

1.run matdata_preprocess.m for voxel selection for movie and image data
2.run run_exp.py for running the experiment, please refer to comment for arguments



To replicate results in NIPS paper:
1. properly preprocess dataset into correct format
2. Set input, working, and output path in following files to the proper location
    - code/run_exp.py
    - code/run_exp_noLR.py
    - code/run_exp_noLR_idvclas.py
    - code/run_exp_imgtrn_mysseg.py
    - code/run_calculate_correlation.py
3. Run experiments:
    1) Experiment 1: 
        - Run code/correlation/run_calculate_correlation.sh
    2) Experiment 2: 
        - Run code/sh_script/mysseg_loo/mysseg_loo.sh
        - Run code/sh_script/imgpred_loo/imgpred_loo.sh
    3) Experiment 3:
        - Run code/sh_script/idvclas/idvclas.sh
4. Plot figures:
    - Run code/plot/plot_bar_XXX.py

abbreviations:
mysseg       : time segment matching (mystery segment identification)
imgpred      : image prediction
idvclas      : individual class prediction (differentiating groups)
loo:         : leave-one-out
imgtrn_mysseg: train on image data and then do mysseg