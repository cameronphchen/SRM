#!/bin/sh
for i in 0 1 2 3 4 #5 6 7 8 9  
do
submit_long run_exp_mysseg.py HA_rand_mysseg_1st 10 1300 2203 $i
submit_long run_exp_mysseg.py HA_rand_mysseg_2nd 10 1300 2203 $i
submit_long run_exp_mysseg.py pHA_EM_rand_mysseg_1st 10 1300 2203 $i
submit_long run_exp_mysseg.py pHA_EM_rand_mysseg_2nd 10 1300 2203 $i
done
