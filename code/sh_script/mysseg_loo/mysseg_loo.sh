#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [-l, --loo] [-e, --expopt] [-w, --winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

## experiment configuration
#dataset: raider, forrest_pt, sherlock_smooth_pmc_noLR
#nvoxel:   500  , 1300      , 813                     
#nTR:     2203  , 3535      , 1976                    
#nsubj:   10    , 18        , 16                      
#winsize: 6     , 9         , 9                       

## Submit Type
#submittype='pni_submit'
submittype='pni_submit -l vf=12G'
#submittype='pni_submit -q long.q -P long -l vf=24G'
#submittype='python'

## Experiment Type
exp='run_exp_noLR.py'
#exp='run_exp.py'

## Dataset Parameters
dataset='sherlock_smooth_pmc_noLR'
nvoxel=813
nTR=1976
niter=10
winsize=9
nsubj_minus_1=16 #number of subjs-1

ln -s /jukebox/ramadge/pohsuan/SRM/code/$exp $exp
chmod +x $exp

for loo in $(seq 8  $nsubj_minus_1)
do

    #$submittype $exp $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize noalign 1      $nvoxel --strfresh
    #$submittype $exp $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize noalign 1      $nvoxel --strfresh
    #$submittype $exp $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize ha      $niter $nvoxel --strfresh
    #$submittype $exp $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize ha      $niter $nvoxel --strfresh
    for nfeat in 50  #10 50 100 500 
    do 
        $submittype $exp $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize pca   1 $nfeat --strfresh
        $submittype $exp $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize pca   1 $nfeat --strfresh 
        for rand in  $(seq 0 4)
        do
            #$submittype $exp $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize srm  $niter $nfeat -r $rand --strfresh
            #$submittype $exp $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize srm  $niter $nfeat -r $rand --strfresh
            $submittype $exp $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize ica       1 $nfeat -r $rand --strfresh
            $submittype $exp $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize ica       1 $nfeat -r $rand --strfresh
        done
    done
done
