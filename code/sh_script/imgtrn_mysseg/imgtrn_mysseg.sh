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

$submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg -e 1st -w $winsize noalign 1      $nvoxel --strfresh
$submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg -e 1st -w $winsize ha      $niter $nvoxel --strfresh
for nfeat in 5 10 50 100 500 
do 
    $submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg -e 1st -w $winsize pca   1 $nfeat --strfresh
    for rand in  $(seq 0 4)
    do
        $submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg   -e 1st -w $winsize srm  $niter $nfeat -r $rand --strfresh
        $submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg   -e 1st -w $winsize ica    1 $nfeat -r $rand --strfresh
    done
done

