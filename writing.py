import time
from pymongo import MongoClient
import certifi
from flask import Flask, render_template, request, jsonify, g, Blueprint, redirect, url_for

app = Flask(__name__)

writing_api = Blueprint('writing_api', __name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.ldbjw.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@writing_api.route('/writing')
def writing():
    writing_list = list(db.writing.find({}, {'_id': False}))
    return render_template('writing.html', writing_list=writing_list)

def getGCount():
    if not hasattr(g, 'count'):
        g.count = 0
        writing_list = list(db.writing.find({}, {'_id': False}))
        for i in writing_list:
            g.count = g.count if g.count > i['id'] else i['id']
    return g.count

@writing_api.route("/writing", methods=["POST"])
def writing_post():
    # db 저장
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    category_receive = request.form['category_give']
    writing_list = list(db.writing.find({}, {'_id': False}))

    g.count = getGCount()
    g.count += 1
    doc = {
        'id': getattr(g, "count", 0),
        'title': title_receive,
        'content': content_receive,
        'category': category_receive,
        'date': time.strftime('%m-%d %H:%M'),
        'nickname': 'nickname'
    }
    db.writing.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '등록되었습니다.'})


@writing_api.route("/writing/get", methods=["GET"])
def writing_get():
    # db 가져오기
    search = request.args.get("search")
    writing_list = list(db.writing.find({}, {'_id': False}))
    # 필터 기능
    if search:
        print(search)
        if search == "html":
            writing_list = list(db.writing.find({"category": "html"}, {'_id': False}))
        elif search == "javascript":
            writing_list = list(db.writing.find({"category": "javascript"}, {'_id': False}))
        elif search == "flask":
            writing_list = list(db.writing.find({"category": "flask"}, {'_id': False}))
        elif search == "mongodb":
            writing_list = list(db.writing.find({"category": "mongodb"}, {'_id': False}))
    print(writing_list)

    return jsonify({'writing':writing_list})

@writing_api.route("/writing/get/<id>", methods=["GET"])
def writing_get_one(id):
    writingOne = db.writing.find_one({'id': int(id)}, {'_id': False})
    return jsonify({'writing': writingOne})


@writing_api.route("/writing/delete", methods=["POST"])
def writing_delete():
    id_receive = request.form['id_give']
    db.writing.delete_one({'id': int(id_receive)})
    return redirect("/")

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)