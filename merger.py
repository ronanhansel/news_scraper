import glob
import pandas as pd

csv_files = glob.glob('*.csv')
df_csv_concat = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)
df_csv_concat.to_csv('CNBC_output_all.csv', sep=',', index=False, encoding='utf-8')