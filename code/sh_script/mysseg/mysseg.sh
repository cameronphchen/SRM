#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [-l, --loo] [-e, --expopt] [-w, --winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

## experiment configuration
#dataset: raider, forrest_pt, sherlock_smooth_pmc_noLR
#nvoxel:   500  , 1300      , 813                     
#nTR:     2203  , 3535      , 1976                    
#nsubj:   10    , 18        , 16                      
#winsize: 6     , 9         , 9                       

## Different type of submits to run
#submittype='pni_submit'
#submittype='pni_submit -l vf=12G'
submittype='pni_submit -q long.q -P long -l vf=24G'
#submittype='python'

## Experiment Type
#exp='run_exp_noLR.py'
exp='run_exp.py'

## Dataset Parameters
dataset='raider'
nvoxel=500
nTR=2203
winsize=6
niter=10

ln -s /jukebox/ramadge/pohsuan/SRM/code/$exp $exp
chmod +x $exp

$submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize noalign $niter $nvoxel --strfresh
$submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize noalign $niter $nvoxel --strfresh
$submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ha      $niter $nvoxel --strfresh
$submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ha      $niter $nvoxel --strfresh
for nfeat in 10 50 100 500 1300
do
    $submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize pca   $niter $nfeat --strfresh
    $submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize pca   $niter $nfeat --strfresh
    for rand in $(seq 0 4)
    do
        $submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize srm  $niter $nfeat -r $rand --strfresh
        $submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize srm  $niter $nfeat -r $rand --strfresh
        $submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ica    $niter $nfeat -r $rand --strfresh
        $submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ica    $niter $nfeat -r $rand --strfresh
    done
done
