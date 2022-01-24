import telebot
import data_for_start
from datetime import date
import gspread
import pandas as pd
import functions
bot= telebot.TeleBot(data_for_start.bot_token)
google = gspread.service_account()
running=True
@bot.message_handler(commands=['start','help'])
def send_welcome (message):
    bot.reply_to(message,"Здравстуйте!" 
                         "\n📝/in - Внести данные"
                         "\n📊/out - Анализ данных"
                         "\n/change - Изменить себестоимость"
                         "\n/cass - Касса"
                         "\n/garage - Остатки"
                         "\n/value - Оборот"
                         "\n📈/graphics - Графики"
                         "\n/in_minus - Учесть трату")
@bot.message_handler(func= lambda m: True)
def echo_all(message): # СТАРТОВОЕ МЕНЮ
    if message.text == '/in':
        bot.send_message(message.from_user.id,'Введите данные следующим образом'
                                              '\nВид продукции,вес,Кол-во, Цена продажи (для рыбы цена за кг)')
        bot.register_next_step_handler(message,inner)
    if message.text=='/out':
        bot.send_message(message.from_user.id,'Меню анализа данных'
                                              "\n/sum- Покажет сумму по показателю за выбранный период"
                                              "\n/sum_type- Покажет сумму по показателю за выбранный период по опр. виду продукции")
        bot.register_next_step_handler(message,outer)
    if message.text=='/cass':
        gc=gspread.service_account()
        sheet= gc.open_by_key(data_for_start.sheet_cassa)
        df= pd.DataFrame(sheet.sheet1.get(data_for_start.sheet_cassa_size))
        headers= df.iloc[0]
        df=pd.DataFrame(df.values[1:],columns=headers)
        df['Сумма']=df['Сумма'].apply(pd.to_numeric)
        gq=df.agg({'Сумма':'sum'})
        gq=gq[0]
        bot.send_message(message.from_user.id,f'Касса составляет {gq}')

    if message.text=='/change':
        bot.send_message(message.from_user.id,'Здесь вы можете изменить себестоимость продукции')

    if message.text=='/garage':
        bot.send_message(message.from_user.id,f'Остатки на текущий день:'
                                              f'\nПОРЦИОННЫЕ:'
                                              f'\n {functions.garage_ikra()}'
                                              f'\nРАЗВЕСНЫЕ:'
                                              f'\n'
                                              f'{functions.garage_all()}')

    if message.text=='/value':
        bot.send_message(message.from_user.id,'Оборот на текущий день'
                                              f'\nсоставляет {functions.oborot()}')
    if message.text=='/in_minus':
        bot.send_message(message.from_user.id,'Внесите затрату следующим образом'
                                              '\nСтатья трат,Сумма')
        bot.register_next_step_handler(message, outer_minus) # Функция добаляет трату
# БЛОК /IN
def inner(message):

        today = date.today().strftime("%d.%m.%Y")
        gc1 = gspread.service_account()
        sh = gc1.open_by_key(data_for_start.sheets_ss_id)  # Указали ссылку на таблицу
        df = pd.DataFrame(sh.sheet1.get(data_for_start.sheets_size_ss))  # Указываем ссылкой размер таблицы
        headers = df.iloc[0]
        df = pd.DataFrame(df.values[1:], columns=headers)
        df[['Себестоимость']] = df[['Себестоимость']].apply(pd.to_numeric)
        df[['Вид']] = df[['Вид']].apply(pd.to_numeric)

        type_product,weight,quant,price = message.text.split(",", 4)
        first_message = f"Добавляю новые данные✅ " \
                        f"\nВид продукции - {type_product}  " \
                        f"\nЦена продажи - {price}" \
                        f"\nОбъем - {quant}"

        bot.send_message(message.from_user.id, first_message)
        #selfprice = int(selfprice[0])
        # Запись в гугл таблицу
        if type_product =='Икра':
            if weight in ['120','250','500']:
                selfprice= df[df['Вид']==int(weight)]
                selfprice=selfprice.agg({'Себестоимость':'sum'})
                selfprice=int(selfprice[0])
                sheet = google.open_by_key(data_for_start.sheets_id)
                sheet.sheet1.append_row([today, type_product,weight, quant,price,selfprice])
                bot.send_message(message.from_user.id,'Данные внесены!')
                z=int(quant)*int(price)
                functions.cass_add(type_product,z)
                functions.store(weight,quant)
            else:
                bot.send_message(message.from_user.id,f'Банки в {weight} граммов не существует,попробуйте еще раз')
        if type_product in ['Форель','Семга']:
            sh = gc1.open_by_key(data_for_start.sheets_ss_all)
            df = pd.DataFrame(sh.sheet1.get(data_for_start.sheets_size_ss))
            headers = df.iloc[0]
            df = pd.DataFrame(df.values[1:], columns=headers)
            df[['Себестоимость']] = df[['Себестоимость']].apply(pd.to_numeric)
            #df[['Вид продукции']] = df[['Вид продукции']].apply(pd.to_numeric)
            selfprice = df[df['Вид продукции'] == type_product]
            selfprice = selfprice.agg({'Себестоимость': 'sum'})
            selfprice = int(selfprice[0])
            sheet=google.open_by_key(data_for_start.sheets_id_other)
            sheet.sheet1.append_row([today,type_product,weight,quant,price,selfprice])
            functions.store_all(type_product,quant,weight)
            bot.send_message(message.from_user.id, 'Данные внесены!')
        if type_product not in ['Икра','Форель','Семга']:
            bot.send_message(message.from_user.id,f'На {type_product} отсуствует себестоимость')
    #except:
     #   bot.send_message(message.from_user.id, 'Неправильный формат данных')



#Блок /OUT

def outer(message):
    if message.text=='/sum':
        bot.send_message(message.from_user.id,"Введите через запятую данные следующим образом"
                                              "\nДата начала периода, Дата окончания периода, Показатель"
                                              "\nПример прикреплю ниже")
        bot.send_message(message.from_user.id,'2022-01-01,2022-12-28,Маржа')
        bot.register_next_step_handler(message,summer)
    if message.text=='/sum_type':
        bot.send_message(message.from_user.id,"Введите через запятую данные следующим образом"
                                              "\nДата начала периода, Дата окончания периода, Показатель, Тип продукции"
                                              "\nПример прикреплю ниже")
        bot.send_message(message.from_user.id,"2022-01-01,2022-12-28,Маржа,Икра")
        bot.register_next_step_handler(message,summer_type)
def summer(message):
    date_start,date_end,value=message.text.split(",",2)
    bot.send_message(message.from_user.id,f"{value} с {date_start} по {date_end}"
                                          f'\n---{functions.summa_non_group(date_start,date_end,value)}')

def summer_type(message):
    date_start, date_end, value, type = message.text.split(",", 3)
    bot.send_message(message.from_user.id,f"{value} c {date_start} по {date_end} "
                                          f"\nс видом продукции {type}"
                                          f"\n---{functions.summa_with_group(date_start,date_end,value,type)}---")

def outer_minus(message):
    value,count=message.text.split(',',2)
    functions.cass_add(value,-int(count))



while running:
# if __name__ == '__main__':
    bot.polling(none_stop=True)
