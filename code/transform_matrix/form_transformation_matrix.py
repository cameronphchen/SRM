# forming transformation matrices for non loo experiment

import numpy as np

def transform(args, workspace_lh, workspace_rh, nsubjs):

  transform_lh = np.zeros((args.nvoxel,args.nfeature,nsubjs))
  transform_rh = np.zeros((args.nvoxel,args.nfeature,nsubjs))

  if args.align_algo in ['ha','ha_syn','ha_syn_kernel','ha_syn_noagg','ha_noagg']:
    transform_lh = workspace_lh['R']
    transform_rh = workspace_rh['R']
  elif args.align_algo in ['pha_em','spha_vi', 'spha_vi_tm', 'spha_vi_decomp', 'ppca',  'pica', 'ppca2',  'pica2','ha_syn_l1']:
    bW_lh = workspace_lh['bW']
    bW_rh = workspace_rh['bW']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh[m*args.nvoxel:(m+1)*args.nvoxel,:]
      transform_rh[:,:,m] = bW_rh[m*args.nvoxel:(m+1)*args.nvoxel,:]
  elif args.align_algo in ['ppca_hor','pica_hor']:
    bW_lh = workspace_lh['R']
    bW_rh = workspace_rh['R']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh
      transform_rh[:,:,m] = bW_rh
  elif args.align_algo in ['ha_sm_retraction','ha_sm_newton']:
    bW_lh = workspace_lh['W']
    bW_rh = workspace_rh['W']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh[:,:,m]
      transform_rh[:,:,m] = bW_rh[:,:,m]
  elif args.align_algo == 'noalign' :
    for m in range(nsubjs):
      transform_lh[:,:,m] = np.identity(args.nvoxel)
      transform_rh[:,:,m] = np.identity(args.nvoxel)
  else :
    exit('alignment algo not recognized')


  return (transform_lh, transform_rh)
