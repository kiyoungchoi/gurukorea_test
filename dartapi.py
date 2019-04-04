#coding=utf-8

from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import webbrowser
from html_table_parser import parser_functions as parser

API_KEY="dc33c48f272b1248e6aa8877e06472cd5c3ad98e"

##종목_반복필요
company_code="058610"
url = "http://dart.fss.or.kr/api/search.xml?auth="+API_KEY+"&crp_cd="+company_code+"&start_dt=19990101&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003"


resultXML=urlopen(url)
result=resultXML.read()
xmlsoup=BeautifulSoup(result,'html.parser')
data = pd.DataFrame()
te=xmlsoup.findAll("list")

for t in te:
    temp=pd.DataFrame(([[t.crp_cls.string,t.crp_nm.string,t.crp_cd.string,t.rpt_nm.string,t.rcp_no.string,t.flr_nm.string,t.rcp_dt.string,t.rmk.string]]),
        columns=["crp_cls","crp_nm","crp_cd","rpt_nm","rcp_no","flr_nm","rcp_dt","rmk"])
    data=pd.concat([data,temp])
data=data.reset_index(drop=True)

#체크
# url1="http://dart.fss.or.kr/dsaf001/main.do?rcpNo="+data['rcp_no'][0]
# webbrowser.open(url1)

url2="http://dart.fss.or.kr/report/viewer.do?rcpNo=20181114000172&dcmNo=6379378&eleId=15&offset=572516&length=68651&dtd=dart3.xsd"
#체크
# webbrowser.open(url2)

##테이블1{자산총계, 부채총계, 자본총계}, 테이블2{매출액} 을 가져오고 싶은디..

#매출액
report=urlopen(url2)
r=report.read()
xmlsoup=BeautifulSoup(r,'html.parser')
body=xmlsoup.find("body")
table=body.find_all("table")
p = parser.make2d(table[3])

# table 체크 > 0부터 시작한다. 테이블은 내가생각한 테이블이 아니고 컴퓨터의 테이블이다. 꼭 개발자모드 켜자
# print(p)

sheet=pd.DataFrame(p[2:], columns=["구분","28기3분기_3개월","28기3분기_누적","27기3분기_3개월","27기3분기_누적"])

sheet["28기3분기_3개월"]=sheet["28기3분기_3개월"].str.replace(",","")
sheet["temp"]=sheet["28기3분기_3개월"].str[0]

sheet.loc[sheet["temp"]=="(","28기분기_3개월"]=sheet["28기분기_3개월"].str.replace("(","-")
sheet["28기3분기_3개월"]=sheet["28기3분기_3개월"].str.split(")").str[0]
sheet.loc[sheet["28기3분기_3개월"]=="","28기3분기_3개월"]="0"
sheet["28기3분기_3개월"]=sheet["28기3분기_3개월"].astype(int)

sale = sheet[shee["구분"]=="매출액"].iloc[0,1]
sale_cost=sheet[shet["구분"]=="매출원가"].iloc[0,1]
sale_profit_ratio=(sale-sale_cost)/sale*100

#round 는 반올림
sale_profit_ratio=round(sale_profit_ratio,1)
print("매출총이익율은 "+str(sale_profit_ratio)+"%입니다")

print(p)
