#!/bin/sh

input_path='/jukebox/fastscratch/janice/sherlock_movie/nosmooth/'
const=2.3548 

for width in $1 #1 2 3 4 5 6
do
	output_path="/jukebox/fastscratch/pohsuan/sherlock_movie/smooth${width}/"
        mkdir -p $output_path
	for subj in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
	do
		in_fname="nosmooth_sherlock_movie_s${subj}.nii.gz"
		out_fname="smooth_sherlock_movie_s${subj}.nii.gz"
                RESULT=$( echo " $width / $const" | bc -l )
		echo "$input_path$in_fname -kernel gauss $RESULT -fmean $output_path$out_fname"
		fslmaths $input_path$in_fname -kernel gauss $RESULT -fmean $output_path$out_fname
	done
done
