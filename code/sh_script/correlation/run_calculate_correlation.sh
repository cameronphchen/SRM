for rnd in {0..4}
do
	for smooth in {0..6}
	do
		pni_submit -l vf=12G calculate_correlation.py $smooth $rnd
	done
done