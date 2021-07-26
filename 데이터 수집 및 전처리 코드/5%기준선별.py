import pandas as pd
from datetime import datetime, timedelta

df = pd.read_excel('./data1.xlsx') # 등락률이 들어간 파일을 불러온다.

df['년/월/일'] = pd.to_datetime(df['년/월/일'])

df = df.astype({'등락률':float}) # 등락률의 type가 object여서 아래 코드 실행을 위해 float로 변환

updown = df.loc[(df['등락률'] > 5) | (df['등락률']  < -5)] 

updown.to_csv('updown.csv', index = False,  encoding='utf-8-sig')

df = pd.read_csv('updown.csv')

org = pd.to_datetime(df['년/월/일'])
before = org +timedelta(days=-1) #전날부터 크롤링하기 위해 등락률이 일어난 전날을 기입

df['before'] = before

# -를 . 으로 변경하기 위해 작성
df = df.astype({'년/월/일':str})
df = df.astype({'before':str})

df['년/월/일'] = df['년/월/일'].str.replace('-', '.')
df['before'] = df['before'].str.replace('-', '.')
df.to_csv('updown.csv', index=False, encoding = 'utf-8-sig')