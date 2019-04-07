from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import webbrowser
from html_table_parser import parser_functions as parser

API_KEY="dc33c48f272b1248e6aa8877e06472cd5c3ad98e"


##종목_반복필요
company_code="058610"

url1 = "http://dart.fss.or.kr/api/search.xml?auth="+API_KEY+"&crp_cd="+company_code+"&start_dt=19990101&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003"

url1="http://dart.fss.or.kr/dsaf001/main.do?rcpNo="+data['rcp_no'][0]
webbrowser.open(url1)
s
