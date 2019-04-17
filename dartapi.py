#coding=utf-8

from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import webbrowser
from html_table_parser import parser_functions as parser

API_KEY="dc33c48f272b1248e6aa8877e06472cd5c3ad98e"


##종목_반복필요
company_code="042110"
# company_code="058610"
def make_report(company_code):


    url = "http://dart.fss.or.kr/api/search.xml?auth="+API_KEY+"&crp_cd="+company_code+"&start_dt=19990101&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003"
    #체크
    # url1="http://dart.fss.or.kr/dsaf001/main.do?rcpNo="+data['rcp_no'][0]
    webbrowser.open(url)

    # resultXML=urlopen(url.encode("UTF-8").decode("ASCII"))
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
    # 하기 에스피지 주소
    # url2="http://dart.fss.or.kr/report/viewer.do?rcpNo=20181114000172&dcmNo=6379378&eleId=15&offset=572516&length=68651&dtd=dart3.xsd"
    url2="http://dart.fss.or.kr/report/viewer.do?rcpNo=20190401000041&dcmNo=6595755&eleId=15&offset=624483&length=101382&dtd=dart3.xsd"
    #체크
    # webbrowser.open(url2)
    return url2,data['rcp_no'][0]
    ##리스트해서 전체 분기별,반기별,etc 전체 보고서 긁어오기




# table 체크 > 0부터 시작한다. 테이블은 내가생각한 테이블이 아니고 컴퓨터의 테이블이다. 꼭 개발자모드 켜자
# print(p)

##테이블1{자산총계, 부채총계, 자본총계}, 테이블2{매출액} 을 가져오고 싶은디..

def find_table(url2,rcpno):
    temp=urlopen(url2)
    r=temp.read()
    xmlsoup=BeautifulSoup(r,'html.parser')
    temp=xmlsoup.find_all("script",attrs={"type":"text/javascript"})
    txt=temp[7]
    a=txt.text

    b=str.find(a,"4. 재무제표")
    c=a[b:b+200]
    d=c.split(",")[4]
    e=d.replace("\"","")
    e=e.replace("\'","")
    dcmo=int(e)

    # 매출 정보 등을 가져오기

# 아래 함수로 변경 line85-
# url2 = make_report(company_code)
# print(url2)
# print("here")
# #매출액
# report=urlopen(url2)
# r=report.read()
# xmlsoup=BeautifulSoup(r,'html.parser')
# body=xmlsoup.find("body")
# table=body.find_all("table")
# p = parser.make2d(table[3])
    url3="http://dart.fss.or.kr/report/viewer.do?rcpNo="+rcpno+"&dcmNo="+str(dcmo)+"&eleId=15&offset=297450&length=378975&dtd=dart3.xsd"

    # http://dart.fss.or.kr/report/viewer.do?rcpNo=20170811001153&dcmNo=5746981&eleId=15

    report=urlopen(url3)
    r=report.read()
    xmlsoup=BeautifulSoup(r,'html.parser')
    body=xmlsoup.find("body")
    table=body.find_all("table")
    p = parser.make2d(table[3])

    name_list=list()
    value_list=list()

    name_list.append("구분")

    for i in range(1,len(p[0])):
        name=p[0][i]+"_"+p[1][i]
        name=name.replace(" ","")
        name_list.append(name)
        value_list.append(name)

    sheet=pd.DataFrame(p[2:], colums=name_list)
    sheet.loc[sheet["구분"]=="수익(매출액)",["구분"]]="매출액"
    return sheet, name_list, value_list

# table 체크 > 0부터 시작한다. 테이블은 내가생각한 테이블이 아니고 컴퓨터의 테이블이다. 꼭 개발자모드 켜자
# print(p)

# sheet=pd.DataFrame(p[2:], columns=["구분","28기3분기_3개월","28기3분기_누적","27기3분기_3개월","27기3분기_누적"])
#
# sheet["28기3분기_3개월"]=sheet["28기3분기_3개월"].str.replace(",","")
# sheet["temp"]=sheet["28기3분기_3개월"].str[0]
#
# sheet.loc[sheet["temp"]=="(","28기3분기_3개월"]=sheet["28기3분기_3개월"].str.replace("(","-")
# sheet["28기3분기_3개월"]=sheet["28기3분기_3개월"].str.split(")").str[0]
# sheet.loc[sheet["28기3분기_3개월"]=="","28기3분기_3개월"]="0"
# sheet["28기3분기_3개월"]=sheet["28기3분기_3개월"].astype(int)
#
#
# print(sheet["28기3분기_3개월"].iloc[0])

def make_profit(sheet,name_list,value_list):
    # 매출총이익률 = 매출총이익 / 매출액*100
    # 매출총이익 = 매출액 - 매출원가

    #숫자로 바꾸기
    for time in value_list:
        sheet[time]=sheet[time].str.replace(",","")
        sheet["temp"]=sheet[time].str[0]

        sheet.loc[sheet["temp"]=="(",time]=sheet[time].str.replace("(","-")
        sheet[time]=sheet[time].str.split(")").str[0]
        sheet.loc[sheet[time]=="",time]="0"
        sheet[time]=sheet[time].astype(int)

    temp_list=list()
    temp_list.append("매출총이익률")

    for time in range(len(value_list)):
        sale = sheet[sheet["구분"]=="매출액"].iloc[0,time+1]
        sale_cost = sheet[sheet["구분"]=="매출원가"].iloc[0,time+1]
        sale_profit_ratio=(sale-sale_cost)/sale*100
        sale_profit_ratio = round(sale_profit_ratio, 1)
        temp_list.append(sale_profit_ratio)

    ouput=pd.DataFrame([temp_list],columns=name_list)
    return output
#데이터 프레임 잘 불러왔는지 확인 empty 면 데이터 안 긁힌것.??

# sale = sheet[sheet["구분"]=="매출액"].iloc[0,1]
# sale_cost = sheet[sheet["구분"]=="매출원가"].iloc[0,1]
# sale_profit_ratio=(sale-sale_cost)/sale*100
#
# #round는 반올림
# sale_profit_ratio=round(sale_profit_ratio,1)
# print("매출총이익율은 "+str(sale_profit_ratio)+"% 입니다")
#
# print(p)


#이걸 다긁어와야하는데. 으잉?!
company_list=list(["000400","004990","005930","014680","214370","271560","217270","280360"])
company_name=list(["롯데손해보험","롯데지주","삼성전자","한솔케미칼","케어젠","오리온","넵튠","롯데제과"])

output_last=pd.DataFrame(columns=["구분", "최근_분기", "최근_분기_누적","이전_분기","이전_분기_누적"])



for i in range(len(company_list)):
    try:
        url2, rcpno=make_report(company_list[i])
        sheet, name_list, value_list = find_table(url2, rcpno)
        output = make_profit(sheet, name_list, value_list)

        if len(output.columns)==3:
            output.columns = ["구분", "최근_분기", "최근_분기_누적"]
        elif len(output.columns)==5:
            output.columns = ["구분", "최근_분기", "최근_분기_누적","이전_분기","이전_분기_누적"]

        output["company_code"]=company_list[i]
        output["company_name"] = company_name[i]
        output["url"] = url2

        output_last=pd.concat([output_last,output])
    except Exception as e:
        print(company_name[i]+" is error")
        print(e)

    output_last.to_csv("output_last.csv")
