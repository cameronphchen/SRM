# SRM
Shared Response Model 

Library for Shared Response Model, related methods and experiment pipeline

Developed by Cameron PH Chen @ Princeton (https://cameronphchen.github.io)

If you use this code or SRM in scientific publication, citing the following paper is appreciated: 

**A Reduced-Dimension fMRI Shared Response Model**

Po-Hsuan Chen, Janice Chen, Yaara Yeshurun-Dishon, Uri Hasson, James Haxby, Peter Ramadge 
Advances in Neural Information Processing Systems (NIPS), 2015. 


Code Structure:
1. SRM/code:
⋅⋅* alignment_algo   : alignmetn algorithms
⋅⋅* experiments      : experiments, called by run_exp*.py
⋅⋅* plot		     : pipelines for aggregating results and generating figures
⋅⋅* preprocessing    : preprocessing procedure for each dataset
⋅⋅* sh_script	     : shell script for running experiments in batch
⋅⋅* test  		     : testing 
⋅⋅* transform_matrix : code to match up the testing subject after having template
⋅⋅* run_exp_imgtrn_mysseg.py : experiment code for training on image testing on mystery segment
⋅⋅* run_exp_noLR_idvclas.py  : experiment code for group classification
⋅⋅* run_exp_noLR.py          : experiment code for image prediction and myster segment identification without seperating left and right hemisphere
⋅⋅* run_exp.py               : experiment code for image prediction and myster segment identification seperating left and right hemisphere

2. SRM/data
In data folder, there should be data/input, data/working, data/output


