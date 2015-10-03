#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [--loo] [--expopt] [--winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]


#run run_exp_noLR_idvclas.py greeneye_tom_noLR_thr15 5000 449 idvclas_svm --loo 1 ha_syn 10 50 -r 0 --strfresh

submittype='pni_submit -l vf=12G'
#submittype='pni_submit -q long.q -P long -l vf=24G'
#submittype='python'

exptype='idvclas_svm'
#exptype='idvclas_svm_on1st'
#exptype='idvclas_svm_no2ndSRM'

dataset='greeneye_tom_noLR_thr15'
nvoxel=5000
nTR=449
niter=11
nsubj=19

ln -s /jukebox/ramadge/pohsuan/SRM/code/run_exp_noLR_idvclas.py run_exp_noLR_idvclas.py
chmod +x run_exp_noLR_idvclas.py
for nfeat_all in 0 1 3 5 10 50 100 
do
    for nfeat_group in 50 100 200 
    do
        for loo in $(seq 0 $nsubj)
        do
            $submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo ppca_idvclas 1 $nfeat_all $nfeat_group  --strfresh
            for rand in  $(seq 0 4)
            do
                $submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo srm_noneprob $niter $nfeat_all $nfeat_group -r $rand --strfresh
                $submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo pica_idvclas 1      $nfeat_all $nfeat_group -r $rand --strfresh
                $submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo srm          $niter $nfeat_all $nfeat_group -r $rand --strfresh
            done
        done
    done
done
