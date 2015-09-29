#!/bin/sh
for i in 0 1 2 3 4 #5 6 7 8 9  
do
submit_long run_exp_loo.py HA_rand_loo0 10 1300 2203 $i
submit_long run_exp_loo.py HA_rand_loo1 10 1300 2203 $i
submit_long run_exp_loo.py HA_rand_loo2 10 1300 2203 $i
submit_long run_exp_loo.py HA_rand_loo3 10 1300 2203 $i
submit_long run_exp_loo.py HA_rand_loo4 10 1300 2203 $i
submit_long run_exp_loo.py HA_rand_loo5 10 1300 2203 $i
submit_long run_exp_loo.py HA_rand_loo6 10 1300 2203 $i 
submit_long run_exp_loo.py HA_rand_loo7 10 1300 2203 $i
submit_long run_exp_loo.py HA_rand_loo8 10 1300 2203 $i
submit_long run_exp_loo.py HA_rand_loo9 10 1300 2203 $i


submit_long run_exp_loo.py pHA_EM_rand_loo0 10 1300 2203 $i
submit_long run_exp_loo.py pHA_EM_rand_loo1 10 1300 2203 $i
submit_long run_exp_loo.py pHA_EM_rand_loo2 10 1300 2203 $i 
submit_long run_exp_loo.py pHA_EM_rand_loo3 10 1300 2203 $i
submit_long run_exp_loo.py pHA_EM_rand_loo4 10 1300 2203 $i
submit_long run_exp_loo.py pHA_EM_rand_loo5 10 1300 2203 $i
submit_long run_exp_loo.py pHA_EM_rand_loo6 10 1300 2203 $i
submit_long run_exp_loo.py pHA_EM_rand_loo7 10 1300 2203 $i
submit_long run_exp_loo.py pHA_EM_rand_loo8 10 1300 2203 $i
submit_long run_exp_loo.py pHA_EM_rand_loo9 10 1300 2203 $i
done
