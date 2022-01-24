# telegram-googlesheets-pandas
This telegram bot can save and process your business data with visualisation
Суть работы - Данный бот предназначен для хранения, обработки и визуализации данных с помощью телеграм суть, проект был сделан для реального инстаграм-магазина с рыбной продукции.
Структура - данные хранятся в 7 зависисмых друг от друга гугл-таблиц, Продажи- остатки- касса- себестоимость. И соотвтетсвенно при произведенной продаже данные автоматически списываются из остатков и сумма выручки добавляется в кассу.
Как это работает: бот содержит ряд команд которые относятся к внесению данных, обарботке и визуализации соответсвенно
Внесение данных: 
/in - Вносим продажу следующим форматом (Вид продукции, Тип продукции (фиксированный вес упаковки, продукт наразвес), кол-во, цена продажи). Информация сохраняется в 2 гугл-таблицы одна таблица для продуктов с фиксированных весов, вторая для продукции наразвес. Это сделано для того чтобы данные были структурированные.Далее у нас формируется датафрэйм внутри программы, к нему, по виду продукции, который мы внесли подтягивается себестоимость, она фиксированно прописана в другой таблице. В итоге у нас появляется датафрейм где присутсвуют наши внесенные данные, автоматически вставленная себестоимсоть и автоматически посчитанная маржа. 
+ у нас автоматически списывается проданный товар из таблицы остатков, + Увеличивается касса на сумму продажи.
/out - Самая обширная и безграничная команда. В ней мы проваливаемся в подменю и видим список комманд. Я для примера оставил всего две /sum -покажет сумму по вырабнному показателю за выбранный период. /sum_type - она показывает сумму по показателю в группировке определенного вида продукции за выбарнную дату. 
В полной версии бота есть команды /what_if - она покзажет что если бы в выбранный период мы бы, например, увеличили цену продажи на 5% и покажет на сколько бы у нас например увеличилась маржа в следствии этого 

/cass - вызывает подсчет кассы которая у нас на текущий момент 
/garage - покажет остатки по видам продукции на текущий момент
/value - считает оборот компании на текущий день
/in_minus - внести трату для вычета из кассы.
/graphics- выодит графики по выбарнному показателю за выбранный период времени

