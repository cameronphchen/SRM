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

#run run_exp_noLR_idvclas.py greeneye_tom_noLR_thr15 5000 449 idvclas_svm --loo 1 ha_syn 10 50 -r 0 --strfresh

#submittype='pni_submit -l vf=12G'
#submittype='pni_submit -q long.q -P long -l vf=24G'
submittype='python'
dataset='greeneye_tom_noLR_thr15'
exptype='idvclas_svm'
#exptype='idvclas_svm_on1st'
#exptype='idvclas_svm_no2ndSRM'
nvoxel=5000
nTR=449
niter=11
nsubj=19

ln -s /jukebox/ramadge/pohsuan/pHA/code/run_exp_noLR_idvclas.py run_exp_noLR_idvclas.py
chmod +x run_exp_noLR_idvclas.py
for nfeat_all in 0 #1 3 5 10 #50 #100 #25
do
    for nfeat_group in 50 #100 200 #100 200 #100 #100 200 #500 1000
    do
        for loo in $(seq 0 $nsubj)
        do
            #$submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo ppca_idvclas 1 $nfeat_all $nfeat_group  --strfresh
            for rand in $(seq 0 4)
            do
                $submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo ha_syn $niter $nfeat_all $nfeat_group -r $rand --strfresh
                #$submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo pica_idvclas 1 $nfeat_all $nfeat_group -r $rand --strfresh
                #$submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo ha_syn_noagg $niter $nfeat_all $nfeat_group -r $rand --strfresh
                #$submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo pha_em $niter $nfeat_all $nfeat_group -r $rand --strfresh
                #$submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo pha_em $niter $nfeat_all $nfeat_group -r $rand --strfresh
            done
        done
    done
done
