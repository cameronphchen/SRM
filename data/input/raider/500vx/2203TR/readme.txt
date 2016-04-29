This dataset is first used in the following publication: Haxby, James V., J. Swaroop Guntupalli, Andrew C. Connolly, Yaroslav O. Halchenko, Bryan R. Conroy, M. Ida Gobbini, Michael Hanke, and Peter J. Ramadge. "A common, high-dimensional model of the representational space in human ventral temporal cortex." Neuron 72, no. 2 (2011): 404-416.

The paper contains both Princeton dataset and Dartmouth dataset, and the files here are only the Princeton part WITHOUT the Dartmouth part.

Task: Ventral Temporal Cortex (VT) voxels of 10 subjects watching movie "Raider of the Lost Ark" and 8 runs of 7 images categories.

File descriptions:

README.txt 

movie_data_lh.mat, movie_data_rh.mat : movie watching response. 
image_timeseries_data_lh.mat, image_timeseries_data_rh.mat : image viewing response before time averaging, primarily used for doing SRM on a less rich time series data 
image_data_lh.mat, image_data_rh.mat : image viewing response after time averaging, 7 categories x 8 runs = 56 responses per subject 
label.mat : labels for image_data_lh.mat and image_data_rh.mat
