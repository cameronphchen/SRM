#!/bin/sh

# loo
#tag="paper_nfeat_ica"
#tag="paper_nfeat_pca"
#tag="paper_nfeat"
tag="paper"
#tag="all"
#plot_code="plot_bar_mysseg.py"
plot_code="plot_bar_mysseg_loo.py"

## bar chars for experiment 2 time segment matching
#python $plot_code $tag raider 500 2203 10 6 10 5
#python $plot_code $tag forrest_pt 1300 3535 18 9 10 5
python $plot_code $tag sherlock_smooth_pmc_noLR 813 1976 16 9 10 5


#for iter in  10 
#do 
	#python $plot_code $tag raider 500 2203 10 6 $iter 5
	#python $plot_code $tag forrest_pt 1300 3535 18 9 $iter 5
	#python $plot_code $tag sherlock_smooth_pmc_noLR 813 1976 16 9 $iter 5
	#python $plot_code $tag pandora_ac_bphp37.5lp2.25 1000 1224 18 30 $iter 5
	#python $plot_code greeneye_ac_noLR 2000 449 40 9 10 5
	#python $plot_code greeneye_tom_noLR_thr15 5000 449 40 9 10 5
#	python plot_bar_imgtrn_mysseg_loo.py paper raider 500 1536 10 6 1 5
#	python plot_bar_imgtrn_mysseg.py paper raider 500 1536 10 6 1 5
#done

#for nfeat in 0 1 3 5 10 50 100
#do 
	#python plot_bar_idvclas.py idvclas_svm          greeneye_tom_noLR_thr15 5000 449 20 10 5 $nfeat
	#python plot_bar_idvclas.py idvclas_svm_on1st    greeneye_tom_noLR_thr15 5000 449 20 10 5 $nfeat
	#python plot_bar_idvclas.py idvclas_svm_no2ndSRM greeneye_tom_noLR_thr15 5000 449 20 10 5 $nfeat
#done
#python plot_bar_imgpred_loo.py paper raider 500 2203 10 10 5
