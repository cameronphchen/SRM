find . -type d -print|while read DIR
do
	cd ${DIR}
	if [ -f noalign_acc_1.npz ]
	then
		echo ${DIR}
	fi
done
