#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [-l, --loo] [-e, --expopt] [-w, --winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

## experiment configuration

#raider, forrest_pt, nature_vt, greeneye_ac_noLR(_thr15), greeneye_tom_noLR_thr15
#1300  , 1300      , 850      , 2000            , 5000
#2203  , 3535      , 1509     , 449             , 449

# raider, forrest_pt: 10 50 100 500 1300
# nature_vt: 10 50 100 400 500 600 700 850
# greeneye_ac_noLR: 10 50 100 500 1000 2000
# greeneye_tom_noLR: 10 50 100 500 1000 2500 5000

#pni_submit -q bigmem.q -P bigmem -l cores=4
#submittype='pni_submit -q long.q -P long -l vf=24G'
submittype='submit -l vf=24G'
dataset='sherlock_smooth_pmc_noLR'
#dataset='greeneye_ac_noLR'
#exp='run_exp.py'
exp='run_exp_noLR.py'
nvoxel=813
nTR=1976
winsize=9
niter=10

ln -s /jukebox/ramadge/pohsuan/pHA/code/$exp $exp
chmod +x $exp

$submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize noalign $niter $nvoxel --strfresh
$submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize noalign $niter $nvoxel --strfresh
$submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ha      $niter $nvoxel --strfresh
$submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ha      $niter $nvoxel --strfresh
for nfeat in 50 100 400 813 #10 50 100 #500 1000 #1000 2000 #10 50 100 #10 50 100 500 1300
do
    #$submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ppca   $niter $nfeat --strfresh
    #$submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ppca   $niter $nfeat --strfresh
    for rand in $(seq 0 4)
    do
        #$submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize pha_em  $niter $nfeat -r $rand --strfresh
        #$submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize pha_em  $niter $nfeat -r $rand --strfresh
        #$submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize spha_vi $niter $nfeat -r $rand --strfresh
        #$submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize spha_vi $niter $nfeat -r $rand --strfresh
        #$submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize spha_vi_decomp $niter $nfeat -r $rand --strfresh
        #$submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize spha_vi_decomp $niter $nfeat -r $rand --strfresh
        #$submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize pica    $niter $nfeat -r $rand --strfresh
        #$submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize pica    $niter $nfeat -r $rand --strfresh
        $submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ha_syn  $niter $nfeat -r $rand --strfresh
        $submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ha_syn  $niter $nfeat -r $rand --strfresh
        #for sig in 0.01 0.1 #1 10 100
        #do
        #    $submittype $exp $dataset $nvoxel $nTR mysseg -e 1st -w $winsize spha_vi_decomp -s $sig $niter $nfeat -r $rand --strfresh
        #    $submittype $exp $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize spha_vi_decomp -s $sig $niter $nfeat -r $rand --strfresh
        #done
    done
done
