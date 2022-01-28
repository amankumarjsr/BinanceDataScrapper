from datetime import date
from unicodedata import name
from urllib import request
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import os
import zipfile
import glob


CoinName= input('Enter the coin name: ').upper()
duration= input('Enter the duration of data you want(1m,1h,2h): ').lower()
start_date= input ('Enter the date (dd-mm-yyyy): ')
end_date= input('Enter the end date (dd-mm-yyyy): ')


coin= requests.get('https://data.binance.vision/?prefix=data/spot/daily/klines/')
ucoin= bs(coin.content , 'html.parser')


start = datetime.datetime.strptime(start_date, "%d-%m-%Y")
end = datetime.datetime.strptime(end_date, "%d-%m-%Y")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

date_list=[]

for date in date_generated:
    x=date.strftime("%Y-%m-%d")
    date_list.append(x)

file_name_list= []
cols=['opening time', 'opening price','highest price','lowest price','closing price','volume','closing time','turnover','number of transactions','active buy volume','NA','NAN']

for item in date_list:
    try:
        file_name=(f'{CoinName}-{duration}-{item}.zip')
        download_mainurl= (f'https://data.binance.vision/data/spot/daily/klines/{CoinName}/{duration}/{CoinName}-{duration}-{item}.zip')
        download= requests.get(download_mainurl, allow_redirects= True)
        print(f'Scrapping data of {item} ')
        with open(file_name, 'wb') as f:
            f.write(download.content)

        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall('C:/Users/rocka/Desktop/Practice python/Binance data scrapper/data')

        file_name_list.append(file_name+'.csv')

        os.remove(file_name) 

    except:
        print('skipped')
        continue


master_df= pd.DataFrame()

for file in os.listdir('C:/Users/rocka/Desktop/Practice python/Binance data scrapper/data'):
    if file.endswith('.csv'):
        master_df= master_df.append(pd.read_csv('C:/Users/rocka/Desktop/Practice python/Binance data scrapper/data/'+file, names= cols))
master_df.to_csv(f'{CoinName}-{duration}-master file.csv', index=False)

for file in os.listdir('C:/Users/rocka/Desktop/Practice python/Binance data scrapper/data'):
    if file.endswith('.csv'):
        os.remove('C:/Users/rocka/Desktop/Practice python/Binance data scrapper/data/'+file)



print('Data Scrapped sucessfully!!!')

