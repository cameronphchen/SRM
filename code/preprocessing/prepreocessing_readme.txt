Preprocessing of fMRI data by Cameron Chen

There are multiple formats that neuroscienctist for fMRI data. I would recommend
getting data from our collaborators in nifti files (.nii). It's the easiest format
to work with, and it's also really popular among neuroscience community. 

We need two files, nifti data file and nifti mask file. 

We can also get mask file from neurosynth.org. 

Nifti data file is basically the data. Nifti mask file specify the region that 
we are interested. There's no difference in the format, it's just how we use the 
file. 

There are two different space neuroscientists used to use. MNI space and Talarach 
space. There are multiple MNI space, and MNI 152 is the most common one. Try to get
the data in MNI152 space, it can be with different size of voxels (1mm,2mm,3mm are
the common one. 

We can use pymvpa fmri_dataset function to read the data from nifti file into matrix. 


After getting the data in matrix form, we use matdata_preprocess.m for voxel 
selection.
