from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}




## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():

    memos = list(db.aloneMemo.find({},{'_id':False}))
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    print(memos)
    return jsonify({'memos':memos})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():

    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    # url_receive = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=171539'
    data = requests.get(url_receive,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one("meta[property='og:title']")['content']
    img = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    url = soup.select_one('meta[property="og:url"]')['content']
    
    #  DB SAVE
    doc = {
      'title':title,
      'img':img,
      'desc':desc,
      'url':url,
      'comment':comment_receive
    }
    db.aloneMemo.insert_one(doc)
    
    
    return jsonify({'title':title, 'img':img, 'desc':desc, 'url':url})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)