%function matdata_preprocess(nvoxel_str, nTR_str)

% please put compute_voxel_ranks.m under the same directory
nTR_str = '1509'
nvoxel_str = '500'
dataset = 'nature_vt'

nTR = str2num(nTR_str)
nvoxel = str2num(nvoxel_str)

load /jukebox/ramadge/pohsuan/pHA/data/raw/nature_vt/nature_movie_vt.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/nature_vt/nature_image_vt.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/nature_vt/nature_mask_vt.mat

mask = mask_all
nsubjs = size(movie_all,1);

% computing voxel ranks for selection
fprintf('start voxel rank \n')
vox_ranks = cell(2,1);
for h = 1:2
    data = cell(nsubjs,1);
    for i = 1:nsubjs
        data(i,1) = {movie_all{i,1}(mask{i,1}==h,:)'};
    end 
    [vox_corr_ranks] = compute_voxel_ranks(data,0);
    vox_ranks(h,1) = {vox_corr_ranks};
end
fprintf('end voxel rank \n')

% save movie data to file
movie_data_lh = nan(nvoxel, nTR, nsubjs);
movie_data_rh = nan(nvoxel, nTR, nsubjs);
for i = 1:nsubjs
    data_temp = movie_all{i,1}(mask{i,1}==1,:);
    movie_data_lh(:,:,i) = data_temp(vox_ranks{1,1}{i,1}(1:nvoxel),:); 
    data_temp = movie_all{i,1}(mask{i,1}==2,:);
    movie_data_rh(:,:,i) = data_temp(vox_ranks{2,1}{i,1}(1:nvoxel),:);
end

assert(sum(sum(sum(isnan(movie_data_rh)))) == 0)
assert(sum(sum(sum(isnan(movie_data_lh)))) == 0)

output_path = ['/jukebox/ramadge/pohsuan/pHA/data/input/' dataset '/' nvoxel_str 'vx/' nTR_str 'TR/']

mkdir(output_path)
save([output_path 'movie_data_lh.mat'],'movie_data_lh');
save([output_path 'movie_data_rh.mat'],'movie_data_rh');

% apply voxel selection on image watching data
image_data_lh = nan(nvoxel, 200, nsubjs);
image_data_rh = nan(nvoxel, 200, nsubjs);
for i = 1:nsubjs
    data_tmp = image_all{i,1};

    image_data_lh_tmp = data_tmp(mask{i,1}==1,:);
    image_data_rh_tmp = data_tmp(mask{i,1}==2,:);

    image_data_lh_tmp = image_data_lh_tmp(vox_ranks{1,1}{i,1}(1:nvoxel),:);
    image_data_rh_tmp = image_data_rh_tmp(vox_ranks{2,1}{i,1}(1:nvoxel),:);

    image_data_lh_tmp = zscore(image_data_lh_tmp')';
    image_data_rh_tmp = zscore(image_data_rh_tmp')';    

    image_data_lh(:,:,i) = image_data_lh_tmp; 
    image_data_rh(:,:,i) = image_data_rh_tmp;
end

assert(sum(sum(sum(isnan(image_data_lh)))) == 0)
assert(sum(sum(sum(isnan(image_data_rh)))) == 0)

save([output_path 'image_data_lh.mat'],'image_data_lh');
save([output_path 'image_data_rh.mat'],'image_data_rh');

