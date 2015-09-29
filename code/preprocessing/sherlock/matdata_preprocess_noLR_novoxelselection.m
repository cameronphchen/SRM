function matdata_preprocess_noLR_novoxelselection(smooth_num,group_num, rnd_num)

% please put compute_voxel_ranks.m under the same directory
dataset = ['sherlock_pmc_smooth' int2str(smooth_num)]
group   = ['g' int2str(group_num)]
rnd = ['rnd' int2str(rnd_num)]
load(['/jukebox/ramadge/pohsuan/pHA/data/raw/' dataset '_' rnd '_' group '/sherlock_pmc.mat'])

nsubjs = size(movie_all,1);
nvoxel = size(movie_all{1,1},1);
nTR    = size(movie_all{1,1},2);

movie_all
for i = 1:nsubjs
    movie_all{i,1}(all(movie_all{i,1}==0,2),:) = [];
end
movie_all

% computing voxel ranks for selection
movie_data = nan(nvoxel, nTR, nsubjs);
for i = 1:nsubjs
    movie_data(:,:,i) = movie_all{i,1};
end

assert(sum(sum(sum(isnan(movie_data)))) == 0)
%assert(sum(sum(sum(~movie_data))) == 0)

output_path = ['/jukebox/ramadge/pohsuan/pHA/data/input/'  dataset '_' rnd '_noLR_' group '/' int2str(nvoxel) 'vx/' int2str(nTR) 'TR/']

mkdir(output_path)
save([output_path 'movie_data.mat'],'movie_data');

