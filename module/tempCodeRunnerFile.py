import urllib.request 
from bs4 import BeautifulSoup 
import requests
def getInstitutionvolumechange(code): 
    code= code.lower() 
    codee = yf.Ticker(code)
    df= codee.institutional_holders
    df.columns = ['보유기관', '주수','발표일','분기매도물량(%)','매입가치(달러)']
    df.loc[:, "주수"] = df["주수"].map('{:,d}'.format)
    df.loc[:, "매입가치(달러)"] = df["매입가치(달러)"].map('{:,d}'.format)
    df['분기매도물량(%)'] = df['분기매도물량(%)']*100 
    
    path = "C:\webdriver/chromedriver"
    driver= webdriver.Chrome(path)
    
    url= f"https://www.nasdaq.com/market-activity/stocks/{code}/institutional-holdings" 
    driver.get(url)
    
    html = driver.page_source 
    soup= BeautifulSoup(html,'html.parser')
    quarter= soup.select('table > tbody >tr>td')[25].text #기준분기 
    month=quarter[:5]
    year= quarter[6:]
    koreanymd= f"{year}/{month}"
    instownership= soup.select('table > tbody >tr>td ')[1].text #기관보유율 
    #ACTIVE 
    increasedposition= soup.select('table > tbody >tr>td ')[7].text #지분매입 기관수
    increasedposition_sharenum= soup.select('table > tbody >tr>td ')[8].text #지분매입 주수
    decreasedposition= soup.select('table > tbody >tr>td ')[10].text #지분매도 기관수 
    decreasedposition_sharenum= soup.select('table > tbody >tr>td ')[11].text #지분매도 주수
    heldposition= soup.select('table > tbody >tr>td ')[13].text #지분유지 기관수  
    heldposition_sharenum= soup.select('table > tbody >tr>td ')[14].text #지분유지 주수  
    #newandold 
    newposition=  soup.select('table > tbody >tr>td ')[19].text #새지분유치 기관 수 
    newposition_shares= soup.select('table > tbody >tr>td ')[20].text #새지분유치 주수
    soldoutposition= soup.select('table > tbody >tr>td ')[22].text #전량매도 기관 수 
    soldoutposition_shares= soup.select('table > tbody >tr>td ')[23].text #전량매도 주수 
    soldoutposition_shares
    
    total= {'기준분기':koreanymd,'전체기관보유율':instownership ,'지분매입기관수':increasedposition, "지분매입주수":increasedposition_sharenum ,
            "지분매도기관수":decreasedposition ,"지분매도주수":decreasedposition_sharenum,"지분유지기관수":heldposition, '지분유지주수':heldposition_sharenum, 
            '새지분유치기관수':newposition, '새지분유치주수':newposition_shares, '전량매도기관수':soldoutposition, '전량매도주수':soldoutposition_shares            
            } 
    
    return df, total
    
df,total= getInstitutionvolumechange('amd') 
df,total


a= int(total['지분매입기관수'].replace(',','')) 
b= int(total['지분매도기관수'].replace(',','')) 
c= int(total['지분유지기관수'].replace(',','')) 
abc= ['지분매입기관수','지분매도기관수','지분유지기관수']
data1= [a,b,c]

d= int(total['지분매입주수'].replace(',','')) 
e= int(total['지분매도주수'].replace(',','')) 
f= int(total['지분유지주수'].replace(',','')) 
deff= ['지분매입주수','지분매도주수','지분유지주수']
data2=[d,e,f]

g= int(total['새지분유치기관수'].replace(',','')) 
h= int(total['전량매도기관수'].replace(',','')) 
gh= ['새지분유치기관수','전량매도기관수']
data3= [g,h]

k= int(total['새지분유치주수'].replace(',','')) 
l= int(total['전량매도주수'].replace(',','')) 
data4= [k,l]
kl= ['새지분유치주수','전량매도주수']

fig1 = plt.figure(figsize=(8,8)) ## 캔버스 생성
fig1.set_facecolor('white') ## 캔버스 색상 하얀색
ax = fig1.add_subplot() ## 프래임 생성
ax.pie(x=data1,labels=abc,autopct=lambda p : '{:.2f}%'.format(p)) ## 파이 차트 출력
plt.title('지분변동기관', fontsize= 20)
plt.legend() 
plt.savefig('static/img/strategy3_a.png')

fig2 = plt.figure(figsize=(8,8)) ## 캔버스 생성
fig2.set_facecolor('white') ## 캔버스 색상 하얀색
ax = fig2.add_subplot() ## 프래임 생성
ax.pie(x=data2,labels=deff,autopct=lambda p : '{:.2f}%'.format(p)) ## 파이 차트 출력
plt.title('지분주식수변동추이', fontsize= 20)
plt.legend() 
plt.savefig('static/img/strategy3_b.png')

x = np.arange(2)
plt.bar(x, data3, width=0.8)
plt.xticks(x, gh)
plt.title("손바뀜기관")
plt.savefig('static/img/strategy3_c.png')
plt.show() 

y = np.arange(2)
plt.bar(y, data4, width=0.8)
plt.xticks(y, kl)
plt.title("손바뀜주수")
plt.savefig('static\img\strategy3_d.png')