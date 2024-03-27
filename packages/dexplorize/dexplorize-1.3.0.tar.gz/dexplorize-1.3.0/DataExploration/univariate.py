import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Entropy Based - Supervised
def compute_entropy(data):
  u_class, counts = np.unique(data, return_counts=True)
  prob = counts / len(data)
  entropy = -np.sum(prob * np.log2(prob))
  return entropy

def best_split(attr1, attr2):
  entropy = float('inf')
  splits =  None
  left_gsplit = right_gsplit = 0
  
  for value in np.unique(attr1):
    left_val = attr1 <= value
    right_val = attr1 > value
    
    left_entr = compute_entropy(attr2[left_val])
    right_entr = compute_entropy(attr2[attr1 > value])
    total_entr = (len(attr2[left_val]) / len(attr2)) * left_entr + (len(attr2[right_val]) / len(attr2)) * right_entr
    
    if total_entr < entropy:
      entropy = total_entr
      splits = value
      left_gsplit = left_entr
      right_gsplit = right_entr
      
  return splits, left_gsplit, right_gsplit
      
      

def entropy(attr1, attr2, bins):
  
  splits = []
  info_gain = []
  left_gsplit = right_gsplit = 0  
  
  for x in range(bins):
    BS, LE, RE = best_split(attr1, attr2)
    
    if BS is None:
      break
    splits.append(BS)
    info_gains = compute_entropy(attr2) - ((len(attr1[attr1 <= BS]) / len(attr1)) * LE + (len(attr1[attr1 > BS]) / len(attr1)) * RE)
    info_gain.append(info_gains)
    attr1 = np.where(attr1 <= BS, np.nan, attr1)
    
  return splits, info_gain


def entropy_based(data1, target, bins):
  splits, info_gain = entropy(data1, target, bins)
  print(f'Entropy: {compute_entropy(target):.3f}') 
  print(f'Entropy given best split: {min(info_gain):.3f}')
  print(f'Information gain: {max(info_gain):.3f}')
  print(f'Best split bins <= {min(splits):.3f} and > {max(splits):.3f}')

# Equal Width Based - Unsupervised
def equal_width(data, bins):
    width = (max(data) - min(data)) / bins
    boundaries = [min(data) + x * width for x in range(1, bins)]
    bin = np.split(np.sort(data), np.searchsorted(np.sort(data), boundaries))
    return bin
    
def ewidth_bin(data, bins):
	ew = equal_width(data, bins)
	for x, bin in enumerate(ew):
		print(f'Bin: {x+1}: {bin}')

def ewidth_plot(data):
  ew1 = [f'{x[0]} - {x[-1]}' for x in data]
  ew2 = [sum(x) for x in data]
    
  plt.bar(ew1, ew2)
  plt.xlabel('Values')
  plt.ylabel('Width')
  plt.show()
        

# Equal Frequency Based - Unsupervised
def equal_freq(data, bins):
    freq = sorted(data)
    size = len(data) // bins
    boundaries = [freq[x * size] for x in range(1, bins)]
    bin = np.split(freq, np.searchsorted(freq, boundaries))
    return bin

def efreq_bin(data, bins):
  ef = equal_freq(data, bins)
  for x, bin in enumerate(ef):
	  print(f'Bin: {x+1}: {bin}')

def  efreq_plot(data):
    ef1 = [f'{x[0]} - {x[-1]}' for x in data]
    ef2 = [sum(x) for x in data]

    plt.bar(ef1, ef2)
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.show()

# Encoding - Binary
def binary_encoding(data, values):
    encode = pd.get_dummies(data[values])
    encoded = encode.astype(int)
    return encoded

def target_encoding(data, values):
  combine = pd.concat([data, binary_encoding(data, values)], axis=1)
  return combine

# Missing Values - Imputation
def impute_values(data):
  find_missing = data.columns[data.isna().any()].tolist()
  
  for values in find_missing:
    random_values = data[values].dropna().sample(data[values].isnull().sum(), random_state=0)
    random_values.index = data[data[values].isnull()].index
    data.loc[data[values].isnull(), values] = random_values
    
  return data

