%function matdata_preprocess(nvoxel_str, nTR_str)

% please put compute_voxel_ranks.m under the same directory
nTR_str = '1509'
nvoxel_str = '1000'
dataset = 'nature_vt_noLR'

nTR = str2num(nTR_str)
nvoxel = str2num(nvoxel_str)

load /jukebox/ramadge/pohsuan/pHA/data/raw/nature_vt_noLR/nature_movie_vt.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/nature_vt_noLR/nature_image_vt.mat


nsubjs = size(movie_all,1);

% computing voxel ranks for selection
fprintf('start voxel rank \n')
data = cell(nsubjs,1);
for i = 1:nsubjs
    data(i,1) = {movie_all{i,1}'};
end 
[vox_corr_ranks] = compute_voxel_ranks(data,0);
vox_ranks = vox_corr_ranks;
fprintf('end voxel rank \n')


% save movie data to file
movie_data = nan(nvoxel, nTR, nsubjs);
for i = 1:nsubjs
    data_temp = movie_all{i,1};
    movie_data(:,:,i) = data_temp(vox_ranks{i,1}(1:nvoxel),:);
end

assert(sum(sum(sum(isnan(movie_data)))) == 0)

output_path = ['/jukebox/ramadge/pohsuan/pHA/data/input/' dataset '/' nvoxel_str 'vx/' nTR_str 'TR/']

mkdir(output_path)
save([output_path 'movie_data.mat'],'movie_data');


% apply voxel selection on image watching data
image_data = nan(1000, 200, nsubjs);
for i = 1:nsubjs

    img_data_tmp = image_all{i,1}(vox_ranks{i,1}(1:nvoxel),:);

    image_data(:,:,i) = zscore(img_data_tmp')';
end

assert(sum(sum(sum(isnan(image_data)))) == 0)
save([output_path 'image_data.mat'],'image_data');

