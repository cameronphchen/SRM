#!/bin/sh

for rand in 0 1 2 3 4 #5 6 7 8 9  
do
  for lw in 100 #1300 #10 20 30 40 #50 100 500 1000 1300 
  do 
    submit_long run_exp.py spHA_VI 10 1300 2203 $rand $lw
  done
done
