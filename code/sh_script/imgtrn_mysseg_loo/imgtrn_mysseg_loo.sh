#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [-l, --loo] [-e, --expopt] [-w, --winsize] 
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

exp='run_exp_imgtrn_mysseg.py'

## Dataset Parameters
dataset='raider'
nvoxel=500
nTR=2203
winsize=6
niter=10
nsubj_minus_1=10 #number of subjs-1

ln -s /jukebox/ramadge/pohsuan/SRM/code/$exp $exp
chmod +x $exp

for loo in $(seq 0 $nsubj_minus_1)
do
    $submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -w $winsize noalign 1      $nvoxel --strfresh
    $submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -w $winsize ha      $niter $nvoxel --strfresh
    for nfeat in 5 10 50 100 500 
    do 
        $submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize ppca   1 $nfeat --strfresh
        for rand in  $(seq 0 4)
        do
            echo ''
            $submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize pha_em  $niter $nfeat -r $rand --strfresh
            $submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize pica         1 $nfeat -r $rand --strfresh
        done
    done
done
