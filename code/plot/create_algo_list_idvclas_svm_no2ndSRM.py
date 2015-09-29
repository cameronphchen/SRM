import pickle

algo_list = []

algo = {
  'name': 'SRM',
  'align_algo': 'ha_syn',
  'nfeature': '0',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'PCA',
  'align_algo': 'ppca_idvclas',
  'nfeature': '0',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'ICA',
  'align_algo': 'pica_idvclas',
  'nfeature': '0',
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
