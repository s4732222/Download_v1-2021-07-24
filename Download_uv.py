import csv
from datetime import date
from os import write
import requests
import pandas as pd
import io
import time

#下載紫外線檔案
url = "https://data.epa.gov.tw/api/v1/uv_s_01?limit=1000&api_key=93304003-71f2-4da8-8416-64fc1980ef65&sort=ImportDate%20desc&format=csv"

uv=requests.get(url).content

uvdata=pd.read_csv(io.StringIO(uv.decode('utf-8')))

#print(uvdata)

#時間
seconds=time.time()
result = time.localtime(seconds)

year = result.tm_year
month = result.tm_mon
day = result.tm_mday
hour = result.tm_hour-3


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


TIME = Y+'-'+M+'-'+D+' '+H+':00'


# 把抓取的紫外線資料存在名為data1的list中




# 抓取紫外線資料的Function

data1=[]
def download(County):
    name=uvdata[(uvdata.County=="臺中市")&(uvdata.SiteName=="臺中")&(uvdata.PublishTime==TIME)]
    print(len(name))    

    County=[]
    PublishAgency=[]
    PublishTime=[]
    SiteName=[]
    UVI=[]                                                           

    for i in range(len(name)):
        County.append(name.iloc[i,0])
        PublishAgency.append(name.iloc[i,1])
        PublishTime.append(name.iloc[i,2])
        SiteName.append(name.iloc[i,3])
        UVI.append(name.iloc[i,4])
    
    dict={"County":County,"PublishAgency":PublishAgency,"PublishTime":PublishTime,"SiteName":SiteName,"UVI":UVI}
    
    df=pd.DataFrame(dict)
    df.to_csv('uv.csv',index=False, encoding='big5')

    time.sleep(1)

    file='uv.csv'

    with open(file,encoding='big5') as csvFile:
        csvReader = csv.reader(csvFile)
        datas = list(csvReader)
        print(datas)
    data1.append(datas[0][4])
    data1.append(datas[1][4])
    
    print(data1)

download("臺中市")
