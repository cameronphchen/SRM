import pickle

algo_list = []


algo = {'name': 'MNI 152',
  'align_algo': 'noalign',
  'nfeature': '1000',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)
"""
algo = {'name': 'HA (1000)',
  'align_algo': 'ha',
  'nfeature': '1000',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)
"""
algo = {'name': 'HA (1000)',
  'align_algo': 'ha_noagg',
  'nfeature': '1000',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)
"""
algo = {
  'name': 'pHAc 100',
  'align_algo': 'ha_syn',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)
"""
algo = {
  'name': 'pHAc 100',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '100',
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
  'name': 'PCA 100',
  'align_algo': 'ppca',
  'nfeature': '100',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)
"""
algo = {
  'name': 'PCA2 100',
  'align_algo': 'ppca2',
  'nfeature': '100',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)
"""

algo = {
  'name': 'ICA 100',
  'align_algo': 'pica',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)
"""
algo = {
  'name': 'ICA2 100',
  'align_algo': 'pica2',
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
