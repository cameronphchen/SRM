import pickle

algo_list = []

algo = {
  'name': 'SRM 50',
  'align_algo': 'ha_syn',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'SRM 100',
  'align_algo': 'ha_syn',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'SRM 200',
  'align_algo': 'ha_syn',
  'nfeature': '200',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

"""
algo = {
  'name': 'pHAc 500',
  'align_algo': 'ha_syn',
  'nfeature': '500',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 1000',
  'align_algo': 'ha_syn',
  'nfeature': '1000',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)
"""
algo = {
  'name': 'PCA 50',
  'align_algo': 'ppca_idvclas',
  'nfeature': '50',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'PCA 100',
  'align_algo': 'ppca_idvclas',
  'nfeature': '100',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'PCA 200',
  'align_algo': 'ppca_idvclas',
  'nfeature': '200',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)
"""
algo = {
  'name': 'PCA 449',
  'align_algo': 'ppca_idvclas',
  'nfeature': '449',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)
"""

algo = {
  'name': 'ICA 50',
  'align_algo': 'pica_idvclas',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'ICA 100',
  'align_algo': 'pica_idvclas',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'ICA 200',
  'align_algo': 'pica_idvclas',
  'nfeature': '200',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

# write python dict to a file
output = open('algo_list.pkl', 'wb')
pickle.dump(algo_list, output)
output.close()

# read python dict back from the file
pkl_file = open('algo_list.pkl', 'rb')
algo_list_out = pickle.load(pkl_file)
pkl_file.close()

print algo_list
