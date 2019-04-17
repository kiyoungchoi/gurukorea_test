import requests
from bs4 import BeautifulSoup

# 종목코드만 변경 code= 뒤에 붙이면됨  "https://finance.naver.com/item/main.nhn?code=""
URL = "https://finance.naver.com/item/main.nhn?code=005930"

samsung_electronic = request.get(URL)
html = samsung_electronic.text

soup = BeautifulSoup(html, 'html.parser')

# PBR 을 위한 발행주식수, BPS  > 네이버를 긁어오면? 네이버가 느리면 늦겠지. dart에서 직접긁어야 하지.
#  > naver에서는 발행주식수 만  >> 주식의 총수 라는 dart에서 긁어올 수 있음., 나머지는 dart : 자본총계, 당기순이익, 12개월간 매출액 // > PSR, PBR 구할 수 있음.
#  발행 할(!?) 주식의 총수는.. 뭐 지 ??  // 네이버에서 나오는 PER, PBR 수치가 미세하게 다른데. 이유는?? > 주목 할 정도는 아닌건가??
