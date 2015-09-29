#!/bin/sh
for lw in 10 50 100 500 1000 1300
do 
  submit_long run_exp_mysseg.py pHA_EM_shift_lowrank_mysseg_1st 10 1300 2203 $lw 
  submit_long run_exp_mysseg.py pHA_EM_shift_lowrank_mysseg_2nd 10 1300 2203 $lw
done
