This dataset is first used in the following publication:
Haxby, James V., J. Swaroop Guntupalli, Andrew C. Connolly, Yaroslav O.
Halchenko, Bryan R. Conroy, M. Ida Gobbini, Michael Hanke, and Peter J.
Ramadge. "A common, high-dimensional model of the representational space in
human ventral temporal cortex." Neuron 72, no. 2 (2011): 404-416.

The paper contains both Princeton dataset and Dartmouth dataset, and the files
here are only the Princeton part WITHOUT the Dartmouth part.

Task:
Ventral Temporal Cortex (VT) voxels of 10 subjects watching movie "Raider of
the Lost Ark" and 8 runs of 7 images categories.

File descriptions:

README.txt
block_labels.txt : block design labels
movie_data_princeton.mat : movie watching response.
monkeydog_raw_data.mat : image viewing response before time averaging,
primarily used for doing hyperalignment/shared response model on a less rich
time series data
monkeydog_timeaveraged_data.mat : image viewing response after time averaging,
7 categories x 8 runs = 56 responses per subject
subjall_picall_label.mat : image category labels for image watching data
(monkeydog)
vt_masks_lhrh.mat : mask for differentiating left VT and right VT. Left
hemisphere is 1 and right hemisphere is 2.
