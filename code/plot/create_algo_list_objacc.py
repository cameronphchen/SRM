import pickle

algo_list = []



algo = {
  'name': 'pHAc 50',
  'align_algo': 'ha_syn',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 500',
  'align_algo': 'ha_syn',
  'nfeature': '500',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 1300',
  'align_algo': 'ha_syn',
  'nfeature': '1300',
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
