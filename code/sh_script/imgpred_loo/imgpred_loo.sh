#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [--loo] [--expopt] [--winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

#raider, forrest_pt, nature_vt
#1300  , 1300      , 850
#2203  , 3535      , 1509

#dataset='raider'
#nvoxel=1300
#nTR=2203
#niter=10

#submittype='python'
submittype='pni_submit'
#submittype='pni_submit -q long.q -P long -l vf=24G'
dataset='raider'
nvoxel=500 #850
nTR=2203
niter=1
nsubj=10

ln -s /jukebox/ramadge/pohsuan/pHA/code/run_exp.py run_exp.py
chmod +x run_exp.py
for loo in $(seq 0 $nsubj)
do
    #$submittype run_exp.py $dataset $nvoxel $nTR imgpred --loo $loo ha      $niter $nvoxel --strfresh
    #$submittype run_exp.py $dataset $nvoxel $nTR imgpred --loo $loo ha_noagg $niter $nvoxel --strfresh
    #$submittype run_exp.py $dataset $nvoxel $nTR imgpred --loo $loo noalign  $niter $nvoxel --strfresh
    for nfeat in 50 100 500 #50 500 1300 
    do
        #$submittype run_exp.py $dataset $nvoxel $nTR imgpred --loo $loo ppca 1 $nfeat --strfresh
        for rand in $(seq 0 4)
        do
            #$submittype run_exp.py $dataset $nvoxel $nTR imgpred --loo $loo ha_sm_retraction $niter $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR imgpred --loo $loo ha_syn $niter $nfeat -r $rand --strfresh
            $submittype run_exp.py $dataset $nvoxel $nTR imgpred --loo $loo ha_syn_noagg $niter $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR imgpred --loo $loo pha_em $niter $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR imgpred --loo $loo pica 1 $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR imgpred --loo $loo spha_vi $niter $nfeat -r $rand #--strfresh
        done
    done
done
