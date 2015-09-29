# forming transformation matrices for non align 

import numpy as np

def transform(args, nsubjs):
  transform_lh = np.zeros((args.nvoxel,args.nfeature,nsubjs))
  transform_rh = np.zeros((args.nvoxel,args.nfeature,nsubjs))

  for m in range(nsubjs):
    transform_lh[:,:,m] = np.identity(args.nvoxel)
    transform_rh[:,:,m] = np.identity(args.nvoxel)

  return (transform_lh, transform_rh)
