#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [-l, --loo] [-e, --expopt] [-w, --winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

#raider, forrest_pt, nature_vt, sherlock_smooth_pmc_noLR, greeneye_ac_noLR, pandora_ac_bphp37.5lp2.25, 
#500  , 1300      , 850      , 813                     , 2000            , 1000                     , 
#2203  , 3535      , 1509     , 1976                    , 449             , 1224                     , 
#10    , 18        , 12       , 16                      , 40              , 18                       , 
#6     , 9         , 9        , 9                       , 9               , 30                       , 

#dataset='raider'
#nvoxel=1300
#nTR=2203
#niter=10

#submittype='pni_submit'
submittype='pni_submit -l vf=12G'
#submittype='pni_submit -q long.q -P long -l vf=24G'
#submittype='python'
dataset='raider'
exp='run_exp_imgtrn_mysseg.py'
nvoxel=500
nTR=1536
niter=10
winsize=6
nsubj_minus_1=10 #number of subjs-1

ln -s /jukebox/ramadge/pohsuan/pHA/code/$exp $exp
chmod +x $exp

for loo in $(seq 0 $nsubj_minus_1)
do

    #$submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize noalign 1      $nvoxel --strfresh
    #$submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -w $winsize ha      $niter $nvoxel --strfresh
    #$submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize ha_noagg $niter $nvoxel --strfresh
    for nfeat in 5 10 50 100 500 #500 #100 #50 #100 500 #1000 #10 50 100 400 813 #500 #813 #50 100 500 1300
    do 
        $submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize ppca   1 $nfeat --strfresh
        for rand in  $(seq 0 4)
        do
            echo ''
            #$submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize pha_em  $niter $nfeat -r $rand --strfresh
            #$submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize spha_vi $niter $nfeat -r $rand --strfresh
            $submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize pica    1 $nfeat -r $rand --strfresh
            #$submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize ha_syn  $niter $nfeat -r $rand --strfresh
            #$submittype $exp $dataset $nvoxel $nTR imgtrn_mysseg --loo $loo -e 1st -w $winsize ha_syn_noagg  $niter $nfeat -r $rand --strfresh
        done
    done
done
