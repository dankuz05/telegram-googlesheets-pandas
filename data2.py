import gspread
import pandas as pd
import data_for_start
gc = gspread.service_account()

sh1=gc.open_by_key(data_for_start.sheets_id_other)
df1=pd.DataFrame(sh1.sheet1.get(data_for_start.sheets_size))
headers1=df1.iloc[0]
df1=pd.DataFrame(df1.values[1:],columns=headers1)
df1['Дата']=pd.to_datetime(df1['Дата'])
df1[['Вес','Объем','Цена продажи','Себестоимоcть']]=df1[['Вес','Объем','Цена продажи','Себестоимость']].apply(pd.to_numeric)
df1['Выручка']=df1['Цена продажи']*df1['Вес']
df1['Маржа']=df1['Выручка']-df1['Себестоимоcть']*df1['Вес']
df2=df1

