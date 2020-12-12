import requests
from bs4 import BeautifulSoup
import openpyxl
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/search', methods=['GET'])
def write_searching():
    # query_receive로 클라이언트가 준 query 가져오기
    query_receive = request.args.get('query_give')
    # start_day_receive로 클라이언트가 준 start_day 가져오기
    start_day_receive = request.args.get('start_day_give')
    #  last_day_receive로 클라이언트가 준  last_day 가져오기
    last_day_receive = request.args.get('last_day_give')

# html 파트에서 진행 가능하게 작업
#query = input('검색할 키워드 : ')
#start_day = input('시작날짜 : ')
#last_day = input('종료날짜 : ')

    filename = "company_data.xlsx" #파일명
    book = openpyxl.load_workbook(filename) #엑셀파일 book 변수에 저장
    sheet = book.worksheets[0]

    datas = []
    for row in sheet.rows:
        datas.append(
            row[0].value
        )

        title_count = 0
        for page in range(10):
            raw = requests.get('https://search.naver.com/search.naver?&where=news&query=' + query_receive + '&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=4&ds=' + start_day_receive + '&de=' + last_day_receive +'&docid=&nso=so:r,p:1d,a:all&mynews=0&cluster_rank=87&start=' + str(page+1) + '&refresh_start=0', headers={'User-Agent': 'Mozilla/5.0'}).text
            html = BeautifulSoup(raw, 'html.parser')

            articles = html.select('.list_news > li')

            for data in datas:
                for article in articles:
                    title = article.select_one('a.news_tit').text
                    title_count += title.count(data[0])
                    # list를 만들어내라
                    # DB에 삽입할 review 만들기
                    title_count = {
                      'count': title_count,
                    }

                    db.title_count.insert_one(title_count)
                    title_count = list(db.title_count.find({}, {'_id': 0}))
                    return jsonify({'result': 'success', 'title_count': title_count})

        #        print(title)

    #    print(title_count)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

# 'https://search.naver.com/search.naver?&where=news&query=' + query + '&sm=tab_tmr&frm=mr&nso=so:r,p:from' + start_day + 'to' + last_day +',a:all&sort=0'
# 'https://search.naver.com/search.naver?sm=tab_opt&where=nexearch&query='+query+'&oquery='+ query +'&tqi=U9M6vdprvTVssa1zHeCssssstzN-208450&nso=so%3Ar%2Cp%3Afrom'+ start_day + 'to' + last_day + '%2Ca%3Aall'

# 'https://search.naver.com/search.naver?&where=news&query=' + query + '&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=4&ds=' + start_day + '&de=' + last_day +'&docid=&nso=so:r,p:1d,a:all&mynews=0&cluster_rank=87&start=61&refresh_start=0'