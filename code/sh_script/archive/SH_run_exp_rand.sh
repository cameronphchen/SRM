#!/bin/sh
VAR_HA=8
VAR_pHA=9

mv /fastscratch/pohsuan/pHA/data/working/2203TR/HA_rand_*     /fastscratch/pohsuan/pHA/data/working/2203TR/HA_rand/HA_rand_$VAR_HA
mv /fastscratch/pohsuan/pHA/data/working/2203TR/acc_HA_rand_* /fastscratch/pohsuan/pHA/data/working/2203TR/HA_rand/HA_rand_$VAR_HA

cp /fastscratch/pohsuan/pHA/data/working/2203TR/HA_rand/HA_rand_$VAR_HA/HA_rand_rh_1300vx_40.npz /jukebox/ramadge/pohsuan/pHA/data/output/2203TR/HA_rand/HA_rand_$VAR_HA/
cp /fastscratch/pohsuan/pHA/data/working/2203TR/HA_rand/HA_rand_$VAR_HA/HA_rand_lh_1300vx_40.npz /jukebox/ramadge/pohsuan/pHA/data/output/2203TR/HA_rand/HA_rand_$VAR_HA/

#mv /fastscratch/pohsuan/pHA/data/working/2203TR/pHA_EM_rand_*     /fastscratch/pohsuan/pHA/data/working/2203TR/pHA_EM_rand/pHA_EM_rand_$VAR_pHA
#mv /fastscratch/pohsuan/pHA/data/working/2203TR/acc_pHA_EM_rand_* /fastscratch/pohsuan/pHA/data/working/2203TR/pHA_EM_rand/pHA_EM_rand_$VAR_pHA

#cp /fastscratch/pohsuan/pHA/data/working/2203TR/pHA_EM_rand/pHA_EM_rand_$VAR_pHA/pHA_EM_rand_rh_1300vx_40.npz /jukebox/ramadge/pohsuan/pHA/data/output/2203TR/pHA_EM_rand/pHA_EM_rand_$VAR_pHA/
#cp /fastscratch/pohsuan/pHA/data/working/2203TR/pHA_EM_rand/pHA_EM_rand_$VAR_pHA/pHA_EM_rand_lh_1300vx_40.npz /jukebox/ramadge/pohsuan/pHA/data/output/2203TR/pHA_EM_rand/pHA_EM_rand_$VAR_pHA/
