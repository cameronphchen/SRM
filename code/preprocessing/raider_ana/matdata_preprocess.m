%function matdata_preprocess(nvoxel_str, nTR_str)

% please put compute_voxel_ranks.m under the same directory
nTR_str = '2203'
nvoxel_str = '500'
dataset = 'raider_ana'

nTR = str2num(nTR_str)
nvoxel = str2num(nvoxel_str)

lrh = 'rh'

if lrh == 'lh'
    load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/movie_data_lh.mat;
    movie_data_raw = movie_data_lh
else 
    load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/movie_data_rh.mat;
    movie_data_raw = movie_data_rh
end

for subj_index = 1:size(movie_data_raw,1)
    mv_data = movie_data_raw{subj_index,1};
    if nTR == 2203
      mv_data = [mv_data(:,5:1101), mv_data(:,1102+5:2212)];
    else
      mv_data = [mv_data(:,5:nTR+4)];
    end
    movie_data_raw(subj_index,1) = {mv_data};
end

nsubjs = size(movie_data_raw,1);

% computing voxel ranks for selection
fprintf('start voxel rank \n')
data = cell(nsubjs,1);
for i = 1:nsubjs
   data(i,1) = {movie_data_raw{i,1}'};
end 
[vox_corr_ranks] = compute_voxel_ranks(data,1);
vox_ranks(1,1) = {vox_corr_ranks};
fprintf('end voxel rank \n')


% save movie data to file
movie_data_out = nan(nvoxel, nTR, nsubjs);
for i = 1:nsubjs
    data_temp = movie_data_raw{i,1};
    movie_data_out(:,:,i) = data_temp(vox_ranks{1,1}{1,1}(1:nvoxel),:);
end

assert(sum(sum(sum(isnan(movie_data_out)))) == 0)

output_path = ['/jukebox/ramadge/pohsuan/pHA/data/input/' dataset '/' nvoxel_str 'vx/' nTR_str 'TR/']

mkdir(output_path)

if lrh == 'lh'
    movie_data_lh = movie_data_out;
    [output_path 'movie_data_lh.mat']
    save([output_path 'movie_data_lh.mat'],'movie_data_lh');
else
    movie_data_rh = movie_data_out
    [output_path 'movie_data_rh.mat']
    save([output_path 'movie_data_rh.mat'],'movie_data_rh');
end



