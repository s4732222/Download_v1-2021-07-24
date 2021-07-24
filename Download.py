import csv
from datetime import date
from os import name, write
import requests
import pandas as pd
import io
import time
import Day_accumulate
import Calculation

'''
#導入Calculation，處理公式
Calculation.Mechanical_mixing_height()
Calculation.td()
'''
# 導入套件：day_accumulate ->處理日累積量問題

DayAccumulate=Day_accumulate.Day_Accumulate()

DayAccumulate=str(DayAccumulate)

# 抓取資料，下載csv檔
 
url = 'https://data.epa.gov.tw/api/v1/aqx_p_142?limit=1000&api_key=93304003-71f2-4da8-8416-64fc1980ef65&sort=ImportDate%20desc&format=csv'

s=requests.get(url).content

df_train=pd.read_csv(io.StringIO(s.decode('utf-8')))

# 時間

seconds=time.time()
result = time.localtime(seconds)

year = result.tm_year
month = result.tm_mon
day = result.tm_mday
hour = result.tm_hour-12

year_txt=year-2000
year_txt=str(year_txt)


if (hour<0):
    hour=hour+24

Y = str(year)


if (month<10):
    M = str(month)
    M = '0'+M
    month_txt=str(month)
    month_txt=' '+month_txt
else:
    M = str(month)
    month_txt=str(month)


if (day<10):
    D = str(day)
    D = '0'+D
    day_txt=str(day)
    day_txt=' '+str(day)
else:
    D = str(day)
    day_txt=str(day)


if (hour<10):
    H = str(hour)
    H = '0'+H
    hour_txt=str(hour)
    hour_txt=' '+str(hour)
else:
    H = str(hour)
    hour_txt=str(hour)



TIME = Y+'-'+M+'-'+D+' '+H+':00:00'



# 把抓取的溫度，濕度，雨量，風速，風向資料存在名為data的list中
data=[]

# 抓取溫度，濕度，雨量，風速，風向資料的Function

def download(itemid,name):
    name=df_train[(df_train.SiteName=="大里")&(df_train.ItemId==itemid)&(df_train.MonitorDate==TIME)]
    print(len(name))                                                                           

    SiteId=[]
    SiteName=[]
    County=[]
    ItemId=[]
    ItemName=[]
    ItemEngName=[]
    ItemUnit=[]
    MonitorDate=[]
    Concentration=[]

    for i in range(len(name)):
        SiteId.append(name.iloc[i,0])
        SiteName.append(name.iloc[i,1])
        County.append(name.iloc[i,2])
        ItemId.append(name.iloc[i,3])
        ItemName.append(name.iloc[i,4])
        ItemEngName.append(name.iloc[i,5])
        ItemUnit.append(name.iloc[i,6])
        MonitorDate.append(name.iloc[i,7])
        Concentration.append(name.iloc[i,8])
    
    dict={"SiteId":SiteId,"SiteName":SiteName,"County":County,"ItemId":ItemId,"ItemName":ItemName,"ItemEngName":ItemEngName,"ItemUnit":ItemUnit,"MonitorDate":MonitorDate,"Concentration":Concentration}
    
    df=pd.DataFrame(dict)
    df.to_csv('Information.csv',index=False, encoding='big5')

    time.sleep(1)

    file='Information.csv'

    with open(file,encoding='big5') as csvFile:
        csvReader = csv.reader(csvFile)
        datas = list(csvReader)
    data.append(datas[1][5])
    data.append(datas[1][8])
    print(datas)
    print(data)

# 執行Function

download(10,'WIND_SPEED')
download(14,'AMB_TEMP')
download(11,'WIND_DIREC')
download(23,'RAINFALL')
download(38,'RH')



Uz=float(data[1])
T=float(data[3])
RH=float(data[9])
P=3
Z=10
Z0=0.2

#引入Calculation.py內容
Td=Calculation.td(T,RH)
A=Calculation.Mechanical_mixing_height(T,Td,P,Uz,Z,Z0)



# 修改成能符合SFC檔的格式
windspeed = data[1]+'0'
winddirec = data[5]
ambtemp = str(float(data[3])+273)
temp = data[3]
temp_pfl = data[3]+'0'
rainfall = data[7]+'0'
rh = str(data[9])
RH = rh[:-1]
A_txt=str(round(A))+'.'


# 寫入OutPut.SFC中
R=open('OutPut.SFC','w')
R.write('   24.145N  120.684E          UA_ID:   466920  SF_ID:   467490  OS_ID:              VERSION: 21112  BULKRN  CCVR_Sub TEMP_Sub\n')
R.write(year_txt+'{:>3}'.format(month_txt)+'{:>3}'.format(day_txt)+'{:>4}'.format(DayAccumulate)+'{:>3}'.format(hour_txt)+'{:>7}'.format('32.7')+'{:>7}'.format('0.278')+'{:>7}'.format('-9.000')+'{:>7}'.format('-9.000')+'{:>6}'.format('-999.')+'{:>6}'.format(A_txt)+'{:>9}'.format('-58.4')+'{:>8}'.format('1.2000')+'{:>7}'.format('0.80')+'{:>7}'.format('1.00')+'{:>8}'.format(windspeed)+'{:>7}'.format(winddirec)+'{:>7}'.format('10.0')+'{:>7}'.format(ambtemp)+'{:>7}'.format('2.0')+'{:>6}'.format('0')+'{:>7}'.format(rainfall)+'{:>7}'.format(RH)+'{:>7}'.format('1010.')+'{:>6}'.format('0')+'{:>15}'.format('NAD-SFC NoSubs'))
R.close()

#寫入OutPut.PLF
R2=open('OutPut.PFL','w')
R2.write(year_txt+'{:>3}'.format(month_txt)+'{:>3}'.format(day_txt)+'{:>3}'.format(hour_txt)+'{:>8}'.format('14.0')+'{:>2}'.format('1')+'{:>8}'.format(winddirec)+'{:>9}'.format(windspeed)+'{:>9}'.format(temp_pfl, '.2f')+'{:>9}'.format('99.00')+'{:>9}'.format('99.00'))
R2.close()
