%function matdata_preprocess(nvoxel_str, nTR_str)

% please put compute_voxel_ranks.m under the same directory
nTR_str = '1224'
nvoxel_str = '1000'
dataset = 'pandora_ac_bphp37.5lp1'

nTR = str2num(nTR_str)
nvoxel = str2num(nvoxel_str)

%load /jukebox/ramadge/pohsuan/pHA/data/raw/forrest_pt/forrest_movie_pt;
%load /jukebox/ramadge/pohsuan/pHA/data/raw/forrest_pt/forrest_LRmask_all;
movie_file = ['/jukebox/ramadge/pohsuan/pHA/data/raw/' dataset '/pandora_ac.mat']
mask_file = ['/jukebox/ramadge/pohsuan/pHA/data/raw/' dataset '/pandora_LRmask_all.mat']
load(movie_file)
load(mask_file)

pandora_all

pandora_all(20) = [];
pandora_LRmask_all(20) = [];
pandora_all(5) = [];
pandora_LRmask_all(5) = [];

pandora_all

mask = pandora_LRmask_all
nsubjs = size(pandora_all,1);

% computing voxel ranks for selection
fprintf('start voxel rank \n')
vox_ranks = cell(2,1);
for h = 1:2
    data = cell(nsubjs,1);
    for i = 1:nsubjs
        data(i,1) = {pandora_all{i,1}(mask{i,1}==h,:)'};
    end 
    [vox_corr_ranks] = compute_voxel_ranks(data,1);
    vox_ranks(h,1) = {vox_corr_ranks};
end
fprintf('end voxel rank \n')

% save movie data to file
movie_data_lh = nan(nvoxel, nTR, nsubjs);
movie_data_rh = nan(nvoxel, nTR, nsubjs);
for i = 1:nsubjs
    data_temp = pandora_all{i,1}(mask{i,1}==1,:);
    % not anatomically aligned data should set to data_temp(vox_ranks{1,1}{i,1}(1:nvoxel),:)
    movie_data_lh(:,:,i) = data_temp(vox_ranks{1,1}{1,1}(1:nvoxel),:); 
    data_temp = pandora_all{i,1}(mask{i,1}==2,:);
    % not anatomically aligned data should set to data_temp(vox_ranks{1,1}{i,1}(1:nvoxel),:)
    movie_data_rh(:,:,i) = data_temp(vox_ranks{2,1}{1,1}(1:nvoxel),:);
end

assert(sum(sum(sum(isnan(movie_data_rh)))) == 0)
assert(sum(sum(sum(isnan(movie_data_lh)))) == 0)

output_path = ['/jukebox/ramadge/pohsuan/pHA/data/input/' dataset '/' nvoxel_str 'vx/' nTR_str 'TR/']

mkdir(output_path)
save([output_path 'movie_data_lh.mat'],'movie_data_lh');
save([output_path 'movie_data_rh.mat'],'movie_data_rh');

