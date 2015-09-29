#!/bin/sh

for lw in 1300 #10 20 30 40 #50 100 500 1000 1300 
do 
  submit_long run_exp.py pHA_EM_shift_lowrank 10 1300 2203 $lw
done
