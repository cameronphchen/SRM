import pickle

algo_list = []


algo = {
  'name': '10',
  'align_algo': 'ppca',
  'nfeature': '10',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': '50',
  'align_algo': 'ppca',
  'nfeature': '50',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': '100',
  'align_algo': 'ppca',
  'nfeature': '100',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': '500',
  'align_algo': 'ppca',
  'nfeature': '500',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': '813',
  'align_algo': 'ppca',
  'nfeature': '813',
  'kernel': None,
  'rand': False
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
