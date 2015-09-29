import pickle

algo_list = []



algo = {
  'name': 'gen. 50',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'gen. 100',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'gen. 500',
  'align_algo': 'ha_syn_noagg',
  'nfeature': '500',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'analy. 50',
  'align_algo': 'ha_sm_retraction',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'analy. 100',
  'align_algo': 'ha_sm_retraction',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'anal. 500',
  'align_algo': 'ha_sm_retraction',
  'nfeature': '500',
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
