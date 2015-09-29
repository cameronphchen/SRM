import numpy as np
import pyGPs

kernel = pyGPs.cov.RBFard(D=1)
T_idx  = np.arange(10)
T_idx  = T_idx[:,None] 
btheta = kernel.hyp
K = kernel.getCovMatrix(T_idx,T_idx, 'train')

