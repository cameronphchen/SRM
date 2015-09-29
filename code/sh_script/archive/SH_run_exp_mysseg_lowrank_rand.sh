#!/bin/sh
for rand in 2 #0 1 2 3 4 #5 6 7 8 9  
do
  for lw in 1300 #10 50 100 500 1000 1300
  do 
    submit_long run_exp_mysseg.py pHA_EM_lowrank_mysseg_1st 10 1300 2203 $rand $lw
#    submit_long run_exp_mysseg.py pHA_EM_lowrank_mysseg_2nd 10 1300 2203 $rand $lw
#    submit_long run_exp_mysseg.py HA_SM_Retraction_mysseg_1st 200 1300 2203 $rand $lw
#    submit_long run_exp_mysseg.py HA_SM_Retraction_mysseg_2nd 200 1300 2203 $rand $lw
#    for Q in 50 
#    do
#       submit_long run_exp_mysseg.py spHA_VI_mysseg_1st 20 1300 2203 $rand $lw RQ  #SM_Q$Q #RQ_Q$Q
#       submit_long run_exp_mysseg.py spHA_VI_mysseg_2nd 20 1300 2203 $rand $lw RQ  #SM_Q$Q #RQ_Q$Q
#    done
  done
done
