%function matdata_preprocess(nvoxel_str, nTR_str)

% please put compute_voxel_ranks.m under the same directory
nTR_str = '449'
nvoxel_str = '2000'
dataset = 'greeneye_ac_noLR_thr15'

nTR = str2num(nTR_str)
nvoxel = str2num(nvoxel_str)

%load('/jukebox/ramadge/pohsuan/pHA/data/raw/greeneye_ac_noLR/greeneye_movie_ac_noLR.mat')
load([ '/jukebox/ramadge/pohsuan/pHA/data/raw/' dataset '/greeneye_movie_ac_noLR_thr15.mat'])

nsubjs = size(movie_all,1);

% computing voxel ranks for selection

movie_all
for i = 1:nsubjs
    movie_all{i,1}(all(movie_all{i,1}==0,2),:) = [];
end
movie_all

fprintf('start voxel rank \n')
data = cell(nsubjs,1);
for i = 1:nsubjs
    data(i,1) = {movie_all{i,1}'};
end
[vox_corr_ranks] = compute_voxel_ranks(data,1);
vox_ranks = vox_corr_ranks;
fprintf('end voxel rank \n')

clearvars data

% save movie data to file
movie_data = nan(nvoxel, nTR, nsubjs);

for i = 1:nsubjs
    data_temp = movie_all{i,1};
    movie_data(:,:,i) = data_temp(vox_ranks{1,1}(1:nvoxel),:);
end

assert(sum(sum(sum(isnan(movie_data)))) == 0)
assert(sum(sum(sum(~movie_data))) == 0)

output_path = ['/jukebox/ramadge/pohsuan/pHA/data/input/' dataset '/' nvoxel_str 'vx/' nTR_str 'TR/']

mkdir(output_path)
save([output_path 'movie_data.mat'],'movie_data');

