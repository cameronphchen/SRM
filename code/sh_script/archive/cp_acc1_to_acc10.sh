
#exp='/jukebox/fastscratch/pohsuan/pHA/data/working/raider/1300vx/2203TR/mysseg_2nd_winsize9'
#exp='/jukebox/fastscratch/pohsuan/pHA/data/working/raider/500vx/56TR/imgtrn_mysseg_1st_winsize6'

#for nfeat in 5 10 50 100 500 
#do 
#	for rand in $(seq 0 4)
#	do
#		cp -i $exp/pica/${nfeat}feat/rand$rand/all/pica_acc_10.npz  \
#                      $exp/pica/${nfeat}feat/rand$rand/all/pica_acc_1.npz
#                for loo in $(seq 0 9)
#                do
#	        	cp -i $exp/pica/${nfeat}feat/rand$rand/loo$loo/pica_acc_10.npz  \
#                              $exp/pica/${nfeat}feat/rand$rand/loo$loo/pica_acc_1.npz
#                done
#        done
#        cp  -i $exp/ppca/${nfeat}feat/identity/all/ppca_acc_10.npz  \
#               $exp/ppca/${nfeat}feat/identity/all/ppca_acc_1.npz
#        for loo in $(seq 0 9)
#        do
#            cp  -i $exp/ppca/${nfeat}feat/identity/loo$loo/ppca_acc_10.npz  \
#                   $exp/ppca/${nfeat}feat/identity/loo$loo/ppca_acc_1.npz
#        done
#done

exp='/fastscratch/pohsuan/pHA/data/working/greeneye_tom_noLR_thr15/5000vx/449TR/idvclas_svm'

for allfeat in 1 3 5 10 50 100
do
  for groupfeat in 50 100 200  
  do
    for loo in $(seq 0 19)
    do 
      #cp  -i $exp/ppca_idvclas/all${allfeat}feat/group${groupfeat}feat/identity/loo${loo}/ppca_idvclas_acc_0.npz \
      #      $exp/ppca_idvclas/all${allfeat}feat/group${groupfeat}feat/identity/loo${loo}/ppca_idvclas_acc_10.npz
      for rand in $(seq 0 4)
      do
        #cp  -i $exp/pica_idvclas/all${allfeat}feat/group${groupfeat}feat/rand${rand}/loo${loo}/pica_idvclas_acc_0.npz \
        #    $exp/pica_idvclas/all${allfeat}feat/group${groupfeat}feat/rand${rand}/loo${loo}/pica_idvclas_acc_10.npz
        cp  -i $exp/ha_syn/all${allfeat}feat/group${groupfeat}feat/rand${rand}/loo${loo}/ha_syn_acc_9.npz \
            $exp/ha_syn/all${allfeat}feat/group${groupfeat}feat/rand${rand}/loo${loo}/ha_syn_acc_10.npz
      done
    done
  done
done
