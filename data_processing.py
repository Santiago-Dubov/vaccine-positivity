import pandas as pd
from dateutil.parser import parse
import numpy as np
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
df = pd.read_csv(url,parse_dates=True)
df = df.drop(df[df['location']=='World'].index)
df['date'] = df['date'].apply(lambda x: parse(x, fuzzy_with_tokens=True))
df['date'] = df['date'].apply(lambda x: x[0])

max_dates = df.groupby('location')['date'].max()
dates = sorted(df['date'].unique())
for loc in df['location'].unique():
  for dt in dates:
    if dt not in df[df['location'] == loc].date.unique():
      y = pd.Series([loc, '', dt, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],index=df.columns)
      x = pd.Series(0, index=df.columns)
      x['date'] = x['date'].astype(datetime.datetime)
      x['date'] = dt
      x['location'] = loc
      df = df.append(y,ignore_index=True)
df = df.sort_values(['location','date'])
df = df.reset_index()
df.drop('index', axis=1, inplace=True)


min_dates = df.groupby('location')['date'].min()
for index,row in df.iterrows():
  if row['location'] and row['date'] == min_dates[row['location']]:
    df.iloc[index] = row.fillna(0)

df['total_vaccinations'].fillna(method='ffill',inplace=True)
df['people_vaccinated'].fillna(method='ffill',inplace=True)
df['people_fully_vaccinated'].fillna(method='ffill',inplace=True)
df['people_fully_vaccinated_per_hundred'].fillna(method='ffill',inplace=True)
df['people_vaccinated_per_hundred'].fillna(method='ffill',inplace=True)
df['total_vaccinations_per_hundred'].fillna(method='ffill',inplace=True)

df.fillna(0,inplace=True)
df.to_csv('vaccinations_fixed.csv', sep=';')
