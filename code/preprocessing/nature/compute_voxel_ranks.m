function [voxel_corr_ranks] = compute_voxel_ranks(data, in_tlrc )
% Computes voxel ranks based on between subject correlation of each voxel
% with any voxel in diff. subject
% If in_tlrc is set to true or 1, then ranks are common to all subjects
% Data should be array of cells of timeseriesXvoxels for each subject

% Calculate individual voxel timeseries correlations with voxels within
% and across subjects using the movie data
nsubjs = size(data,1);
N = size(data{1,1},1);

vox_corr=cell(nsubjs,nsubjs);

disp('Computing between subject voxel correlations...');
for subj_index = 1:nsubjs
    A = zscore(double(data{subj_index,1}));
    A = A - repmat(sum(A)/N, N, 1);
    A = A./repmat(sqrt(sum(A.^2)), N, 1);
    for subj2 = subj_index+1:nsubjs
        B = zscore(double(data{subj2,1}));
        B = B - repmat(sum(B)/N,N,1);
        B = B./repmat(sqrt(sum(B.^2)), N, 1);
        vox_corr(subj_index,subj2) = {A'*B};
    end
end

% Ranking voxels
disp('Ranking voxels...');

if in_tlrc
    
    voxel_corr_ranks = cell(1,1);
    % Computing the sum of max. corr. for each voxel in each subj_src
    voxel_score = zeros( size(data{subj_index,1},2), 1 );
    for subj_index = 1:nsubjs
        % looping over all other subjects
        for subj2 = 1:nsubjs
            if(subj2~=subj_index)
                if ( subj_index < subj2 )
                    vox_corr_temp = vox_corr{subj_index,subj2};
                    % Add the max. of the corr. of each voxel in src subj to
                    % with any voxel in other subj in the same hemisphere
                    voxel_score = voxel_score + max( vox_corr_temp,[],2);
                else
                    vox_corr_temp = vox_corr{subj2,subj_index};
                    voxel_score = voxel_score + max( vox_corr_temp,[],1)';
                end
            end
        end
    end
    
    % order the voxels based on their ranks and store them
    [scores, voxel_rank] = sort(voxel_score,'descend');
    voxel_corr_ranks(1,1) = {voxel_rank};
    
else
    
    voxel_corr_ranks = cell(nsubjs,1);
    % Computing the sum of max. corr. for each voxel in each subj_src
    for subj_index = 1:nsubjs
        voxel_score = zeros( size(data{subj_index,1},2), 1 );
        % looping over all other subjects
        for subj2 = 1:nsubjs
            if(subj2~=subj_index)
                if ( subj_index < subj2 )
                    vox_corr_temp = vox_corr{subj_index,subj2};
                    % Add the max. of the corr. of each voxel in src subj to
                    % with any voxel in other subj in the same hemisphere
                    voxel_score = voxel_score + max( vox_corr_temp,[],2);
                else
                    vox_corr_temp = vox_corr{subj2,subj_index};
                    voxel_score = voxel_score + max( vox_corr_temp,[],1)';
                end
            end
        end
        % order the voxels based on their ranks and store them
        [scores, voxel_rank] = sort(voxel_score,'descend');
        voxel_corr_ranks(subj_index,1) = {voxel_rank};
    end
    
end
