import pickle

algo_list = []


#algo = {'name': 'MNI',
#  'align_algo': 'noalign',
#  'nfeature': '500',
#  'kernel': None,
#  'rand': False
#}
#algo_list.append(algo)

algo = {
  'name': 'PCA\nk=50',
  'align_algo': 'ppca',
  'nfeature': '50',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'ICA\nk=50',
  'align_algo': 'pica',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {'name': 'HA\nv=500',
  'align_algo': 'ha', #'align_algo': 'ha_noagg',
  'nfeature': '500',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'SRM\nk=50',
  'align_algo': 'srm',
  'nfeature': '50',
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
