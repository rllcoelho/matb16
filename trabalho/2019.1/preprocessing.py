import pandas as pd
import sys, pickle
from random import sample

def drop_unique_value_col(df):
    for col in df.columns:
        if len(df[col].unique()) == 1:
            df.drop(col,inplace=True,axis=1)

with open(sys.argv[1], 'rb') as f:
    print('anomalous dataset file opened')
    df_a = pd.DataFrame(pickle.load(f))
    print('anomalous df made')
    
with open(sys.argv[2], 'rb') as f:
    print('normal training dataset file opened')
    df_n = pd.DataFrame(pickle.load(f))
    print('normal training df made')

df_a['label'] = 'anomalous'
df_a.drop_duplicates(keep='last', inplace=True)
print('Duplicates removed from anomalous dataset')
len_df_a = len(df_a.index)
print('Number of rows in anomalous dataset: %i' % len_df_a)

df_n['label'] = 'normal'
df_n.drop_duplicates(keep='last', inplace=True)
print('Duplicates removed from normal dataset')
len_df_n = len(df_n.index)
print('Number of rows in normal dataset: %i' % len_df_n)

if(len_df_a > len_df_n):
    print('After duplicates removal, anomalous dataset became greater than normal dataset. It will be downsampled.')
    df_a = df_a.sample(n=len_df_n, random_state=1)
elif(len_df_n > len_df_a):
    print('After duplicates removal, normal dataset became greater than anomalous dataset. It will be downsampled.')
    df_n = len_df_n.sample(n=len_df_a, random_state=1)

df = pd.concat([df_a, df_n], sort=True)
print('Anomalous and normal dataset concatenated')

print('#'*200)
print('DATASET BEFORE PRE-PROCESSING')
print('#'*200)

print('HEAD')
print(df.head())
print('-'*50)
print('Describe:')
print(df.describe())
print('-'*50)
print('Number of rows: %i' % len(df.index))
print('-'*50)
print(df['version'].describe())
print('-'*50)
print(df['method'].describe())
print('-'*50)
print(df['label'].describe())
print('-'*50)
print(df[''].describe())

print('#'*200)
print('PRE-PROCESSING')
print('#'*200)

print("Replacing NaN with 0's")
df.fillna(0, inplace=True)
print("Droping '' column. It represents the empty string before or after the '/' in the paths and seens not to be meaningful.")
df.drop(columns="", inplace=True)
print("Droping columns with unique value. e.g.: 'version'")
drop_unique_value_col(df)

print('#'*200)
print('DATASET AFTER PRE-PROCESSING')
print('#'*200)

print(df.head())
print('-'*50)
print('Describe:')
print(df.describe())
print('-'*50)
print('Number of rows: %i' % len(df.index))
print('-'*50)
print(df['method'].describe())
print('-'*50)
print(df['label'].describe())
print('-'*50)

df.to_csv('csic_dataset/preprocessed_df_1.csv')
