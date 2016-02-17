# Shared Response Model (SRM)

Library for Shared Response Model, related methods and experiment pipelines
Developed by Cameron PH Chen @ Princeton (https://cameronphchen.github.io)

### If you just want to use SRM on your dataset, checkout https://github.com/cameronphchen/Use_SRM

### Paper:

If you use this code or SRM in scientific publication, citing the following paper is appreciated: 

**A Reduced-Dimension fMRI Shared Response Model**

Po-Hsuan Chen, Janice Chen, Yaara Yeshurun, Uri Hasson, James V. Haxby, Peter J. Ramadge 
Advances in Neural Information Processing Systems (NIPS), 2015. 
[Paper](http://papers.nips.cc/paper/5855-a-reduced-dimension-fmri-shared-response-model)

Bibtex:
```
@inproceedings{phchen2015srm,
  title={A Reduced-Dimension f{MRI} Shared Response Model},
  author={Chen, Po-Hsuan and Chen, Janice and Yeshurun, Yaara and Hasson, Uri and Haxby, James V. and Ramadge, Peter J. },
  year={2015},
  booktitle={Advances in Neural Information Processing Systems (NIPS) },
}
```

### To use the code please do 
```
git clone https://github.com/cameronphchen/SRM.git
```
### After git clone, to get the data please do 
(make sure git-lfs is installed on your machine https://git-lfs.github.com/)
```
git lfs pull
```

Please refer to code/readme.txt for procedure to replicate NIPS results

##Code Structure:

1. SRM/code:
  * alignment_algo   : alignmetn algorithms
  * experiments      : experiments, called by run_exp*.py
  * plot		       : pipelines for aggregating results and generating figures
  * preprocessing    : preprocessing procedure for each dataset
  * sh_script	       : shell script for running experiments in batch
  * test  		   : testing 
  * transform_matrix : code to match up the testing subject after having template
  * run_exp_imgtrn_mysseg.py : experiment code for training on image testing on mystery segment
  * run_exp_noLR_idvclas.py  : experiment code for group classification
  * run_exp_noLR.py          : experiment code for image prediction and myster segment identification without seperating left and right hemisphere
  * run_exp.py               : experiment code for image prediction and myster segment identification seperating left and right hemisphere

2. SRM/data:
  * In data folder, there should be data/input, data/working, data/output

##Data :

raider : 
.mat files at data/input/raider/ 
If you use this dataset please refer to Haxby et at. 2011 Neuron paper. 

Bibtex:
```
@article{haxby2011common,
  title={A common, high-dimensional model of the representational space in human ventral temporal cortex},
  author={Haxby, James V and Guntupalli, J Swaroop and Connolly, Andrew C and Halchenko, Yaroslav O and Conroy, Bryan R and Gobbini, M Ida and Hanke, Michael and Ramadge, Peter J},
  journal={Neuron},
  volume={72},
  number={2},
  pages={404--416},
  year={2011},
  publisher={Elsevier}
}
```

forrest: 
Please refer to www.studyforrest.org for forrest dataset

sherlock and audiobook: 
The papers for these two datasets are still under review, so the datasets are not available at this point. 


