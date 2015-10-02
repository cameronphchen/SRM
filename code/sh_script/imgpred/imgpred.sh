#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [--loo] [--expopt] [--winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

## experiment configuration
#dataset: raider
#nvoxel:   500  
#nTR:     2203  
#nsubj:   10    
#winsize: 6     

## Different type of submits to run
#submittype='pni_submit'
#submittype='pni_submit -l vf=12G'
submittype='pni_submit -q long.q -P long -l vf=24G'
#submittype='python'

## Dataset Parameters
dataset='raider'
nvoxel=500
nTR=2203
winsize=6
niter=10

ln -s /jukebox/ramadge/pohsuan/SRM/code/run_exp.py run_exp.py
chmod +x run_exp.py
$submittype run_exp.py $dataset $nvoxel $nTR imgpred noalign $niter $nvoxel --strfresh
$submittype run_exp.py $dataset $nvoxel $nTR imgpred ha      $niter $nvoxel --strfresh
for nfeat in  10 50 100 500 1300  
do
  $submittype run_exp.py $dataset $nvoxel $nTR imgpred pca $niter $nfeat --strfresh
  for rand in $(seq 0 4)
  do
    $submittype run_exp.py $dataset $nvoxel $nTR imgpred srm  $niter $nfeat -r $rand --strfresh
    $submittype run_exp.py $dataset $nvoxel $nTR imgpred ica    $niter $nfeat -r $rand --strfresh
  done
done
