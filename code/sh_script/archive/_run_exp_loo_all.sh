VAR=3

mv /fastscratch/pohsuan/pHA/data/working/2203TR/HA_rand_loo* /fastscratch/pohsuan/pHA/data/working/2203TR/HA_rand_loo/rand$VAR
mv /fastscratch/pohsuan/pHA/data/working/2203TR/acc_HA_rand_loo* /fastscratch/pohsuan/pHA/data/working/2203TR/HA_rand_loo/rand$VAR

mv /fastscratch/pohsuan/pHA/data/working/2203TR/pHA_EM_rand_loo* /fastscratch/pohsuan/pHA/data/working/2203TR/pHA_EM_rand_loo/pHA_EM_rand$VAR
mv /fastscratch/pohsuan/pHA/data/working/2203TR/acc_pHA_EM_rand_loo* /fastscratch/pohsuan/pHA/data/working/2203TR/pHA_EM_rand_loo/pHA_EM_rand$VAR

submit_long run_exp_loo.py HA_rand_loo0 10 1300 2203
submit_long run_exp_loo.py HA_rand_loo1 10 1300 2203
submit_long run_exp_loo.py HA_rand_loo2 10 1300 2203
submit_long run_exp_loo.py HA_rand_loo3 10 1300 2203
submit_long run_exp_loo.py HA_rand_loo4 10 1300 2203
submit_long run_exp_loo.py HA_rand_loo5 10 1300 2203
submit_long run_exp_loo.py HA_rand_loo6 10 1300 2203
submit_long run_exp_loo.py HA_rand_loo7 10 1300 2203
submit_long run_exp_loo.py HA_rand_loo8 10 1300 2203
submit_long run_exp_loo.py HA_rand_loo9 10 1300 2203


submit_long run_exp_loo.py pHA_EM_rand_loo0 10 1300 2203
submit_long run_exp_loo.py pHA_EM_rand_loo1 10 1300 2203
submit_long run_exp_loo.py pHA_EM_rand_loo2 10 1300 2203
submit_long run_exp_loo.py pHA_EM_rand_loo3 10 1300 2203
submit_long run_exp_loo.py pHA_EM_rand_loo4 10 1300 2203
submit_long run_exp_loo.py pHA_EM_rand_loo5 10 1300 2203
submit_long run_exp_loo.py pHA_EM_rand_loo6 10 1300 2203
submit_long run_exp_loo.py pHA_EM_rand_loo7 10 1300 2203
submit_long run_exp_loo.py pHA_EM_rand_loo8 10 1300 2203
submit_long run_exp_loo.py pHA_EM_rand_loo9 10 1300 2203
