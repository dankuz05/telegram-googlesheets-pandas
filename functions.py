import pandas as pd

import Data
from datetime import date
import gspread as gs
import data2
import data_for_start

df=Data.x
df2=data2.df2

def header():
    z=Data.x
    z=z[['Вид продукции','Цена продажи','Объем']]
    return z.head(0).to_string()

def summa_non_group (date_start,date_end,factor):
    z=df[(df['Дата']>= date_start)&(df['Дата']<=date_end)]
    y=df2[(df2['Дата']>=date_start)&(df2['Дата']<=date_end)]
    new_df=z.agg({factor:'sum'})
    new_df1=y.agg({factor:'sum'})
    result= int(new_df[0])+int(new_df1[0])
    return result
#print(summa_non_group('2022-01-01','2022-12-28','Маржа'))

def summa_with_group (date_start,date_end,factor,type):
    if type=='Икра':
        z = df[(df['Дата'] >= date_start) & (df['Дата'] <= date_end)]
        new_df=z.agg({factor:'sum'})
        result=int(new_df[0])
        return result
    if type in ['Форель','Семга']:
        y = df2[(df2['Дата'] >= date_start) & (df2['Дата'] <= date_end)]
        y=y[y['Вид продукции']==type]
        new_df1=y.agg({factor:'sum'})
        result1=int(new_df1[0])
        return result1
#print(summa_with_group('2022-01-01','2022-12-28','Маржа','Форель'))

def cass_add(type,quant):
    gh=gs.service_account()
    sh = gh.open_by_key(data_for_start.sheet_cassa)
    sh.sheet1.append_row([type,quant]) #Возможно прописать интом нкжно

def store(weight,quant):
    type='Икра'
    gh=gs.service_account()
    sh=gh.open_by_key(data_for_start.sheet_garage_ikra)
    sh.sheet1.append_row([type,weight,-int(quant)])

def store_all(type,quant,weight):
    gh = gs.service_account()
    sh = gh.open_by_key(data_for_start.sheet_garage_all)
    sh.sheet1.append_row([type,-int(quant),str((-float(weight)))])

def garage_ikra():
    gh=gs.service_account()
    sh = gh.open_by_key(data_for_start.sheet_garage_ikra)
    df_ikra = pd.DataFrame(sh.sheet1.get(data_for_start.sheet_garage_ikra_size))
    headers_ikra=df_ikra.iloc[0]
    df_ikra=pd.DataFrame(df_ikra.values[1:],columns=headers_ikra)
    df_ikra['Кол-во']=df_ikra['Кол-во'].apply(pd.to_numeric)
    df_ikra=df_ikra.groupby(['Вид продукции','Вес']).agg({'Кол-во':'sum'}).reset_index().to_string()
    # df_all[['Koл-во','Вес итого']]=df_all[['Koл-во','Вес итого']].apply(pd.to_numeric)
    # df_ikra=df_ikra.groupby('Вес').agg({'Кол-во'})
    # df_all=df_all.groupby('Вид продукции').agg({'Кол-во'})
    # df_ikra=df_ikra.reset_index()
    # df_all=df_all.reset_index()
    return df_ikra
#print(garage())

def garage_all():
    gh=gs.service_account()
    sh=gh.open_by_key(data_for_start.sheet_garage_all)
    df_all=pd.DataFrame(sh.sheet1.get(data_for_start.sheet_garage_all_size))
    headers = df_all.iloc[0]
    df_all=pd.DataFrame(df_all.values[1:],columns=headers)
    df_all['Кол-во']=df_all['Кол-во'].apply(pd.to_numeric)
    f=df_all
    df_all=df_all.groupby('Вид продукции').agg({'Кол-во':'sum'}).reset_index().to_string()
    return df_all
#print(garage_all(),f'\n{garage_ikra()}')



def cassa_for_value():#Вывожу кассу числом
    gc = gs.service_account()
    sheet = gc.open_by_key(data_for_start.sheet_cassa)
    df = pd.DataFrame(sheet.sheet1.get(data_for_start.sheet_cassa_size))
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)
    df['Сумма'] = df['Сумма'].apply(pd.to_numeric)
    gq = df.agg({'Сумма': 'sum'})

    result = float(gq[0])
    return result

def sum_for_value():
    gh = gs.service_account()
    sh = gh.open_by_key(data_for_start.sheet_garage_ikra)
    df_ikra = pd.DataFrame(sh.sheet1.get(data_for_start.sheet_garage_ikra_size))
    headers_ikra = df_ikra.iloc[0]
    df_ikra = pd.DataFrame(df_ikra.values[1:], columns=headers_ikra)
    df_ikra['Кол-во'] = df_ikra['Кол-во'].apply(pd.to_numeric)
    df_ikra = df_ikra.groupby(['Вид продукции', 'Вес']).agg({'Кол-во': 'sum'}).reset_index()
    ss=xz()
    ss1=ss[ss['Вид']==120].iloc[0,2]
    ss2=ss[ss['Вид']==250].iloc[0,2]
    ss3=ss[ss['Вид']==500].iloc[0,2]
    df_1=int(df_ikra[df_ikra['Вес']=='120'].iloc[0,2])*ss1# Рассчет себестоимости всех остатков по типу
    df_2=int(df_ikra[df_ikra['Вес']=='250'].iloc[0,2])*ss2
    df_3=int(df_ikra[df_ikra['Вес']=='500'].iloc[0,2])*ss3
    result_ikra=df_1+df_2+df_3
    return result_ikra

def sum_for_value_all():
    gh=gs.service_account()
    sh=gh.open_by_key(data_for_start.sheet_garage_all)
    df_all=pd.DataFrame(sh.sheet1.get(data_for_start.sheet_garage_all_size))
    headers = df_all.iloc[0]
    df_all=pd.DataFrame(df_all.values[1:],columns=headers)
    df_all[['Кол-во','Вес итого']]=df_all[['Кол-во','Вес итого']].apply(pd.to_numeric)
    df_all=df_all.groupby('Вид продукции').agg({'Вес итого':'sum'}).reset_index()
    ss=xzz()
    ss1 = (ss[ss['Вид продукции'] == 'Форель'].iloc[0, 1])*(df_all[df_all['Вид продукции']=='Форель'].iloc[0,1])
    ss2 = (ss[ss['Вид продукции'] == 'Семга'].iloc[0, 1])*(df_all[df_all['Вид продукции']=='Семга'].iloc[0,1])
    result=ss1+ss2
    #ss3 = ss[ss['Вид продукции'] == 500].iloc[0, 2]
    return result


def xz():
    gc1 = gs.service_account()
    sh = gc1.open_by_key(data_for_start.sheets_ss_id)  # Указали ссылку на таблицу
    df = pd.DataFrame(sh.sheet1.get(data_for_start.sheets_size_ss))# Указываем ссылкой размер таблицы
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)
    df[['Себестоимость']] = df[['Себестоимость']].apply(pd.to_numeric)
    df[['Вид']] = df[['Вид']].apply(pd.to_numeric)
    return df
def xzz():
    gc1 = gs.service_account()
    sh = gc1.open_by_key(data_for_start.sheets_ss_all)
    df = pd.DataFrame(sh.sheet1.get(data_for_start.sheets_size_ss))
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)
    df[['Себестоимость']] = df[['Себестоимость']].apply(pd.to_numeric)
    return df

def oborot():
    return sum_for_value()+sum_for_value_all()+cassa_for_value()
print(oborot())