import pandas as pd
import numpy
import numpy as np
import matplotlib.pyplot as plt 
import datetime

df = pd.read_excel('C:/Users/GaraevMaksim/Desktop/data_science/Исходящие вызовы абонента.xlsx')
df = df.drop_duplicates()
df['Дата звонка'] = pd.to_datetime(df['Дата звонка'], dayfirst = True)
df['Дата_День'] = df['Дата звонка'].dt.to_period('D')
df['Дата_М'] = df['Дата звонка'].dt.to_period('M')
df['Длительность разговора в минутах'] = np.ceil((pd.to_timedelta(df['Длительность разговора']).dt.total_seconds().astype(int))/60).astype(int)
df['Стоимость минут/Монстр общения'] = df['Длительность разговора в минутах'].apply(lambda x: x* 1.5 if x == 1 else (x-1) * 0.5 + 1.5 if 2 <= x <= 9 else 1.5 + 0.5 * 8 + 1 * (x - 9))
df['Стоимость минут/33 копейки'] = df['Длительность разговора в минутах'].apply(lambda x: x * 1 if x == 1 else (x - 1) * 0.33 + 1)

res = pd.DataFrame()

res['Звонки в день'] = df.groupby(['Дата_М','Дата_День']).count()['Дата звонка']
res['Минут в день'] = df.groupby(['Дата_М','Дата_День']).sum()['Длительность разговора в минутах']
res['Монстр общения/Стоимость в день'] = df.groupby(['Дата_М','Дата_День']).sum()['Стоимость минут/Монстр общения']
res['33 копейки/Стоимость в день'] = df.groupby(['Дата_М','Дата_День']).sum()['Стоимость минут/33 копейки']
res['Хочу сказать/Стоимость в день'] = res['Минут в день'].apply(lambda x: x * 3.95 if x <= 5 else (x - 5) * 0.4 + 5 * 3.95)
mask = df['Оператор связи вызываемого абонента'] != 'мтс'
res ['Минут в день/МТС'] = df[mask].groupby(['Дата_М','Дата_День']).sum()['Длительность разговора в минутах']
res ['Много звонков/Стоимость в день'] = res['Минут в день/МТС'].apply(lambda x: x * 0.9 if x <= 5 else (x - 30) * 0.9 + 4.5 + 25 * 0.05 if x > 30 else (x - 5) * 0.05 + 4.5)


res1 = pd.DataFrame()
res1['Звонки'] = df.groupby('Дата_М').count()['Дата звонка']
res1['Минут в месяц'] = res.groupby('Дата_М').sum()['Минут в день']
res1['Монстр общения'] = res.groupby('Дата_М').sum()['Монстр общения/Стоимость в день']
res1['33 копейки'] = res.groupby('Дата_М').sum()['33 копейки/Стоимость в день']
res1['Хочу сказать'] = res.groupby('Дата_М').sum()['Хочу сказать/Стоимость в день']
res1['Много звонков'] = res.groupby('Дата_М').sum()['Много звонков/Стоимость в день']
res1['Больше слов'] = res1['Минут в месяц'].apply(lambda x: (x - 555) * 1.95 + 555 if x > 555 else 555)
res1.loc['Итого'] = [res1['Звонки'].sum(),res1['Минут в месяц'].sum(),res1['Монстр общения'].sum(),res1['33 копейки'].sum(),res1['Хочу сказать'].sum(),res1['Много звонков'].sum(),res1['Больше слов'].sum()]


x = [2465.5, 1599.57,3712.2,3097.60,836.15]

labels = ['Монстр общения','33 копейки','Больше слов','Хочу сказать','Много звонков']
plt.figure(figsize=(14,7),dpi = 60)
plt.title('Затраты на связь в зависимости от тарифа',color = 'blue', weight = 'bold', family = 'sans-serif', size = 22)
plt.xlabel('Тариф',color = 'blue', weight = 'bold', family = 'sans-serif', fontsize = 14)
plt.ylabel('Стоимость,руб',color = 'blue', weight = 'bold', family = 'sans-serif', fontsize = 14)
plt.rc('xtick',color = 'red', labelsize = 18)
plt.grid(alpha = .4)
for i in range(len(x)):
    plt.bar(labels[i],x[i])

plt.xticks(rotation = 20)
plt.show()

