import pickle

algo_list = []

"""
algo = {'name': 'MNI 152',
  'align_algo': 'noalign',
  'nfeature': '813',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)
"""

algo = {'name': 'HA (813)',
  'align_algo': 'ha',
  'nfeature': '813',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 10',
  'align_algo': 'ha_syn',
  'nfeature': '10',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 50',
  'align_algo': 'ha_syn',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 100',
  'align_algo': 'ha_syn',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 400',
  'align_algo': 'ha_syn',
  'nfeature': '400',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 813',
  'align_algo': 'ha_syn',
  'nfeature': '813',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)



algo = {
  'name': 'pHA 10',
  'align_algo': 'pha_em',
  'nfeature': '10',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)


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

algo = {
  'name': 'pHA 813',
  'align_algo': 'pha_em',
  'nfeature': '813',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

"""
algo = {
  'name': 'PCA 400',
  'align_algo': 'ppca',
  'nfeature': '400',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)


algo = {
  'name': 'ICA 400',
  'align_algo': 'pica',
  'nfeature': '400',
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
