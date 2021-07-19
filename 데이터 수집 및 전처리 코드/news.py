from tqdm import tqdm_notebook
import pandas as pd
from IPython.display import clear_output
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os

options = webdriver.ChromeOptions()
options.add_argument('headless')  # 크롬 브라우저 팝업 뜨는 거 안보이게 해줌 ㅎㅎ
options.add_argument('window-size=1920x1080') # 하라는데 왜 했는 지 모르겠습니다.
options.add_argument("disable-gpu") # 브라우저 띄울 때 gpu 쓰는 거 막아줘서 속도 향상
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
# headless 모드를 감지하지 못하게 함


press = {
    '매일경제' : 1009,
    '머니투데이' : 1008,
    '서울경제' : 1011,
    '아시아경제' : 1277,
    '이데일리' : 1018,
    '파이낸셜뉴스' : 1014,
    '한국경제' : 1015, 
    '헤럴드경제' : 1016
}             # 다른 언론사 코드 궁금하면 네이버 뉴스에서 언론사 하나씩 선택해보면서 url주소 checked 뒤에 있는 숫자 확인

search_keyword = input('궁금한 종목을 입력 해주세요!: ') #종목 입력 (다른거 기사 궁금하면 다른거 입력해서 해도 됨)
start_date = input('시작 날짜를 입력해주세요(yyyy.mm.dd): ')
end_date = input('종료 날짜를 입력해주세요(yyyy.mm.dd): ')


if not os.path.isdir('urls'):                                                           
    os.mkdir('urls')
if not os.path.isdir('contents'): 
    os.mkdir('contents')
# 경로 잡아주기


# url 주소를 저장할 리스트 생성
print('urls: ')
for i in tqdm_notebook(press):
    url_list = []
    for page in range(1, 11, 10):
        site = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='+search_keyword+'&sort=1&photo=0&field=0&pd=3&ds='+start_date+'&de='+end_date+'&mynews=1&office_type=1&office_section_code=3&news_office_checked='+str(press.get(i))+'&nso=so:dd,p:from'+start_date[:4]+start_date[5:7]+start_date[8:10]+'to'+end_date[:4]+end_date[5:7]+end_date[8:10]+',a:all&start='+str(page)
        driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
        driver.get(site)
        # 뉴스 url 수집하기
        things = driver.find_elements_by_link_text('네이버뉴스')  
        
        for thing in things:
            url = thing.get_attribute('href')
            url_list.append(url)

        driver.close()
    df = pd.DataFrame({"url":url_list})
    df.to_csv('urls/'+search_keyword+'_'+i+'_urls.csv')
    print(i+" 저장완료")
    
print('')
print('url 스크래핑 완료')
print('')


print('contents: ')

for t in tqdm_notebook(press):
    
    df = pd.read_csv('urls/'+search_keyword+'_'+t+'_urls.csv')
    urls=df.url[:]
    data_dict = {
    'date' : [],
    'title' : [],
    'contents' : []
}
    
    for i in range(len(urls)):
        driver = webdriver.Chrome("./chromedriver.exe", chrome_options=options)
        driver.get(df['url'][i])

        # 기사 시간 스크랩
        try:
            driver.find_element_by_css_selector('.t11').click()
            data_dict['date'].append(driver.find_element_by_css_selector('.t11').text.strip())
        except NoSuchElementException:
            pass
        
        # 기사 제목 스크랩
        try:
            driver.find_element_by_css_selector('.tts_head').click()
            data_dict['title'].append(driver.find_element_by_css_selector('.tts_head').text.strip())
        except NoSuchElementException:
            pass
        
        # 기사 내용 스크랩
        try:
            driver.find_element_by_css_selector('.tts_head').click()
            data_dict['contents'].append(driver.find_element_by_css_selector('._article_body_contents').text.strip())
        except NoSuchElementException:
            pass

        driver.close()

    df1=pd.DataFrame(data_dict)
    df1.to_csv('contents/'+search_keyword+'_'+t+'_news_contents.csv', encoding='utf-8-sig', index=False)
    print(t+" 저장완료")

print('')
print('본문 스크래핑 완료')