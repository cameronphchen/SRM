import pickle

algo_list = []


algo = {'name': 'MNI 152',
  'align_algo': 'noalign',
  'nfeature': '850',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {'name': 'HA (850)',
  'align_algo': 'ha_noagg',
  'nfeature': '850',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 50',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 100',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 400',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '400',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 500',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '500',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 600',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '600',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 700',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '700',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 850',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '850',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

"""
algo = {
  'name': 'pHA 50',
  'align_algo': 'pha_em',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)


algo = {
  'name': 'pHA 100',
  'align_algo': 'pha_em',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)


algo = {
  'name': 'pHA 400',
  'align_algo': 'pha_em',
  'nfeature': '400',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)
"""
algo = {
  'name': 'pHA 500',
  'align_algo': 'pha_em',
  'nfeature': '500',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHA 600',
  'align_algo': 'pha_em',
  'nfeature': '600',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHA 700',
  'align_algo': 'pha_em',
  'nfeature': '700',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)
"""
algo = {
  'name': 'pHA 850',
  'align_algo': 'pha_em',
  'nfeature': '850',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)
"""

"""
algo = {
  'name': 'PCA 100',
  'align_algo': 'ppca',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'ICA 100',
  'align_algo': 'pica',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)
"""


# write python dict to a file
output = open('algo_list.pkl', 'wb')
pickle.dump(algo_list, output)
output.close()

# read python dict back from the file
pkl_file = open('algo_list.pkl', 'rb')
algo_list_out = pickle.load(pkl_file)
pkl_file.close()

print algo_list
