import pandas as pd
import sys, pickle

with open(sys.argv[1], 'rb') as f:
    print('anomalous dataset file opened')
    df_a = pd.DataFrame(pickle.load(f))
    print('anomalous df made')

with open(sys.argv[2], 'rb') as f:
    print('normal training dataset file opened')
    df_n = pd.DataFrame(pickle.load(f))
    print('normal training df made')

df_a['label'] = 'anomalous'
df_n['label'] = 'normal'

df = pd.concat([df_a, df_n], sort=True)

print(df.head())
print('Describe:')
print(df.describe())
print('Number of rows: %i' % len(df.index))
print(df['version'].describe())
print(df['method'].describe())
print(df['label'].describe())
print(df[''].describe())

df.fillna(0, inplace=True)
df.drop(columns="version", inplace=True)
df.drop(columns="", inplace=True)
df.drop_duplicates(keep='last', inplace=True)
print(df.head())
print('Describe:')
print(df.describe())
print('Number of rows: %i' % len(df.index))
print(df['method'].describe())
print(df['label'].describe())
print(df[df['label'] == 'normal'].describe())
