%takes the FSL nifti files and create a matrix of VOI*subj*TRs for
%"greenEyes1_comprehension","greenEyes2_comprehension". It is
%not cropped. 
%make a matrix out of the cell?
%Crop it to the right values ('subject_new')

path(path,'/jukebox/ramadge/pohsuan/NeuroElf/NeuroElf_v10_5062/');

datapath = '/jukebox/ramadge/RAW_DATA/green_eye/niftis/';
outputpath = '/fastscratch/pohsuan/pHA/data/raw/greeneye/';
subj_greenEyes1 = [1:14,29:34];
subj_greenEyes2 = [15:28,35:40];
pre = 'subj';
suffix = '_trans_filtered_func_data.nii';
greenEyes1_comprehension = cell(1,length(subj_greenEyes1));
greenEyes2_comprehension = cell(1,length(subj_greenEyes2));
voiComprehension = cell(1,length(subj_greenEyes1));

for i = 1:length(subj_greenEyes1)
filename = fullfile(datapath,[pre,int2str(subj_greenEyes1(i)), suffix]);
nii_temp = xff(filename);
voi_comprehension = xff('/jukebox/ramadge/RAW_DATA/green_eye/comprehension_forward_t6_cluster50.voi');
msk = voi_comprehension.CreateMSK(nii_temp.BoundingBox)
[greenEyes1_comprehension{i}, voiComprehension{i}]=nii_temp.VOITimeCourse(voi_comprehension);
end

for i = 1:length(subj_greenEyes2)
filename = fullfile(datapath,[pre,int2str(subj_greenEyes2(i)), suffix]);
nii_temp = xff(filename);
voi_comprehension = xff('/jukebox/ramadge/RAW_DATA/green_eye/comprehension_forward_t6_cluster50.voi');
[greenEyes2_comprehension{i}, voiComprehension{i}]=nii_temp.VOITimeCourse(voi_comprehension);
end

%save([outputpath 'comprehension_t5_cluster50'], 'comprehension_t5_cluster50');
%save([outputpath 'greenEyes1_comprehension'], 'greenEyes1_comprehension');
%save([outputpath 'greenEyes2_comprehension'], 'greenEyes2_comprehension');

%crop
for i = 1:20
greenEyes1_comprehension_cropped{i} = greenEyes1_comprehension{i}((G1_from(i):G1_to(i)),:);
end

for i = 1:20
greenEyes2_comprehension_cropped{i} = greenEyes2_comprehension{i}((G2_from(i):G2_to(i)),:);
end

for i =1:20
greenEyes1_comprehension_cropped{i} = greenEyes1_comprehension_cropped{i}';
greenEyes2_comprehension_cropped{i} = greenEyes2_comprehension_cropped{i}';
end

greenEyes1_comprehension_cropped = greenEyes1_comprehension_cropped';
greenEyes2_comprehension_cropped = greenEyes2_comprehension_cropped';


save([outputpath 'comprehension_t5_cluster50_cropped'], 'comprehension_t5_cluster50_cropped');
save([outputpath 'greenEyes1_comprehension_cropped'], 'greenEyes1_comprehension_cropped');
save([outputpath 'greenEyes2_comprehension_cropped'], 'greenEyes2_comprehension_cropped');

%change into mat
[greenEyes1_comprehension_cropped_mat,greenEyes2_comprehension_cropped_mat] = cell2mat(greenEyes1_comprehension_cropped,greenEyes2_comprehension_cropped);%creates a matrix of (voxels x subject x TRs) from the cell matrixes
save([outputpath 'comprehension_forward_t6_cluster50_cropped_mat'], 'comprehension_forward_t6_cluster50_cropped_mat');
save([outputpath 'greenEyes1_comprehension_cropped_mat'], 'greenEyes1_comprehension_cropped_mat');
save([outputpath 'greenEyes2_comprehension_cropped_mat'], 'greenEyes2_comprehension_cropped_mat');





