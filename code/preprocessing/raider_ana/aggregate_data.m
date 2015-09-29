% aggreate data for matdata_preprocess input

movie_data_lh = cell(10,1)
movie_data_rh = cell(10,1)
image_data_lh = cell(10,1)
image_data_rh = cell(10,1)

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_cb_vt_lh.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_cb_vt_rh.mat
movie_data_lh(1,1) = {t_cb_vt_lh'}
movie_data_rh(1,1) = {t_cb_vt_rh'}

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_dm_vt_lh.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_dm_vt_rh.mat
movie_data_lh(2,1) = {t_dm_vt_lh'}
movie_data_rh(2,1) = {t_dm_vt_rh'}

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_hj_vt_lh.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_hj_vt_rh.mat
movie_data_lh(3,1) = {t_hj_vt_lh'}
movie_data_rh(3,1) = {t_hj_vt_rh'}

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_kd_vt_lh.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_kd_vt_rh.mat
movie_data_lh(4,1) = {t_kd_vt_lh'}
movie_data_rh(4,1) = {t_kd_vt_rh'}

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_kl_vt_lh.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_kl_vt_rh.mat
movie_data_lh(5,1) = {t_kl_vt_lh'}
movie_data_rh(5,1) = {t_kl_vt_rh'}

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_mh_vt_lh.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_mh_vt_rh.mat
movie_data_lh(6,1) = {t_mh_vt_lh'}
movie_data_rh(6,1) = {t_mh_vt_rh'}

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_ph_vt_lh.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_ph_vt_rh.mat
movie_data_lh(7,1) = {t_ph_vt_lh'}
movie_data_rh(7,1) = {t_ph_vt_rh'}

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_rb_vt_lh.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_rb_vt_rh.mat
movie_data_lh(8,1) = {t_rb_vt_lh'}
movie_data_rh(8,1) = {t_rb_vt_rh'}

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_se_vt_lh.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_se_vt_rh.mat
movie_data_lh(9,1) = {t_se_vt_lh'}
movie_data_rh(9,1) = {t_se_vt_rh'}

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_sm_vt_lh.mat
load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/t_sm_vt_rh.mat
movie_data_lh(10,1) = {t_sm_vt_lh'}
movie_data_rh(10,1) = {t_sm_vt_rh'}

output_path = ['/jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/']

mkdir(output_path)
save([output_path 'movie_data_lh.mat'],'movie_data_lh');
save([output_path 'movie_data_rh.mat'],'movie_data_rh');

load /jukebox/ramadge/pohsuan/pHA/data/raw/raider_ana/mkdg_vt_tlrc.mat
for i = 1:10
    image_data_lh(i,1) = {XLtst((i-1)*56+1:i*56,:)'}
    image_data_rh(i,1) = {XRtst((i-1)*56+1:i*56,:)'}
end

save([output_path 'image_data_lh.mat'],'image_data_lh');
save([output_path 'image_data_rh.mat'],'image_data_rh');

