from flask import Flask, render_template,url_for,request,session,redirect, make_response,session
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://rohit:rohit@owner-shard-00-00-gwlya.mongodb.net:27017,owner-shard-00-01-gwlya.mongodb.net:27017,owner-shard-00-02-gwlya.mongodb.net:27017/owner?ssl=true&replicaSet=owner-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.owner

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

us='admin'
ps='admin'

@app.route('/')
@app.route("/index")
def index():
    return render_template("index_image.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user = request.form['user']
        pw = request.form['pw']
        if(user==us and pw==ps):
            return redirect('/image')
        return render_template('login.html',msg="Incorrect Username or Password")

@app.route('/image', methods=['GET','POST'])
def image():
    if(request.method=='GET'):
        return render_template('image.html',loggedin=True)
    if(request.method=='POST'):
        src=request.form['src']
        dest=request.form['dest']
        img_url=request.form['img_url']
        a=db.indoor.insert({'src':src,'dest':dest,'img_url':img_url})
        print(a)
        return render_template('image.html',loggedin=True)

@app.route('/logout')
def logout():
    return redirect('/index' )

if __name__=='__main__':
    app.run(debug=True, host='127.0.0.1', port='5001')