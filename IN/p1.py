
from flask import Flask, render_template,url_for,request,session,redirect, make_response,session
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/owner"
#app.config["MONGO_URI"] = "uri"
mongo = PyMongo(app)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
#sess = Session()

data={}
items={}


@app.route('/')
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if(request.method=='GET'):
        return render_template('register.html')
    if(request.method=='POST'):
        email=request.form['email']
        mobile=request.form['mobile']
        bid=request.form['bid']
        sname=request.form['sname']
        uname=request.form['uname']
        pw=request.form['password']
        a=mongo.db.owner.users.find({'uname':uname})
        if(a.count()!=0):
            return render_template('register.html', msg="Username already exists try another")
        users={"email":email,"mobile":mobile,"bid":bid,"sname":sname,"uname":uname ,"pass":pw}
        mongo.db.owner.users.insert(users)
        return redirect('/index')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user = request.form['user']
        pw = request.form['pw']
        a=mongo.db.owner.users.find({'uname':user , 'pass':pw})
        #print(a.count())
        if (a.count()!=0):
            session['my_var'] = user
            return redirect(url_for('decide'))
        return render_template('login.html',msg="Incorrect Username or Password")

@app.route('/decide')
def decide():
    return render_template('decide.html',loggedin=True)

@app.route('/store_data' ,methods=['GET','POST'])
def store_data():
    #print()
    if request.method == 'GET':
        return render_template('store_data.html' , loggedin=True)
    if request.method == 'POST':
        user = session.get('my_var', None)
        #print(user)
        det=mongo.db.owner.users.find({'uname':user})
        #print(det[0]['sname'])
        sname=det[0]['sname']
        bid=det[0]['bid']
        #print('cpn' in request.form.keys())
        cpn = request.form['cpn']
        cpn_des = request.form['cpn_des']
        adv=request.form['adv']
        data['bid']=bid
        data['ads']=adv
        data['cpn']=cpn
        data['cpn_des']=cpn_des
        data['sname']=sname
        print(data)
        return render_template('item.html',loggedin=True)

@app.route('/item', methods=['GET','POST'])
def item():
    if request.method == 'GET':
        return render_template('item.html')
    if request.method == 'POST':
        item = request.form['item']
        cat = request.form['cat']
        price = request.form['price']
        qty=request.form['qty']
        rating=5
        if(cat in items.keys()):
            items[cat][item]={ 'price' : price , 'quantity': qty , 'rating' : rating}
        else:
            items[cat] = {item:{ 'price' : price , 'quantity': qty , 'rating' : rating} }
        #data['comm']=items
        print(items)
        print(data)
        return render_template('item.html' ,loggedin=True)

@app.route('/add_to_db')
def add_to_db():
    data['comm']=items
    print(data)
    mongo.db.owner.itm.insert(data)
    data.clear()
    items.clear()
    return render_template('decide.html', loggedin=True)

@app.route('/add_updated_item', methods=['GET','POST'])
def add_updated_item():
    if request.method == 'GET':
        return render_template('update.html',loggedin=True)
    if request.method == 'POST':
        item = request.form['item']
        cat = request.form['cat']
        price = request.form['price']
        qty=request.form['qty']
        rating=5
        
        #session['cat'] = cat
        #session['item'] = item
        if (cat in items.keys()):
            items[cat][item] = {'price': price, 'quantity': qty, 'rating': rating}
        else:
            items[cat] = {item: {'price': price, 'quantity': qty, 'rating': rating}}
        print(items)
        #print(data)
        return render_template('update.html' , loggedin=True)

@app.route('/update_itm')
def update_itm():
    mongo.db.owner.itm.find()
    print("i am into updattte items")
    user = session.get('my_var', None)
    #cat = session.get('cat', None)
    #item = session.get('item', None)
    cat=[]
    item=[]
    for j in items.keys():
        cat.append(j)
    for j in cat:
        for k in items[j].keys():
            item.append(k)
    print('cat= ',cat)
    print('items= ',item)
    print(user)
    get_bid=mongo.db.owner.users.find({'uname':user})
    bid=get_bid[0]['bid']
    det=mongo.db.owner.itm.find({'bid':bid})
    copy_comm=det[0]['comm']
    print(det)
    print(copy_comm)
    print(data)
    print(items)
    for j in cat:
        for k in item:
            if (j in copy_comm.keys()):
                if(k in items[j].keys()):
                    copy_comm[j][k] = items[j][k]
            else:
                copy_comm[j]=items[j]
    print(copy_comm)
    mongo.db.owner.itm.update({'bid':bid} ,{'$set':{'comm':copy_comm}})
    cat.clear()
    item.clear()
    data.clear()
    items.clear()
    return render_template('decide.html', loggedin=True)

@app.route('/delete' ,methods=['GET','POST'])
def delete():
    if(request.method=='GET'):
        return render_template('delete.html',loggedin=True)
    if(request.method=='POST'):
        cat=request.form['cat']
        itm=request.form['item']
        user = session.get('my_var', None)
        get_bid = mongo.db.owner.users.find({'uname': user})
        bid = get_bid[0]['bid']
        det = mongo.db.owner.itm.find({'bid': bid})

        det2=det[0]
        print(det[0])
        if(cat in det[0]['comm'].keys()):
            if(itm in det[0]['comm'][cat].keys()):
                det1 = det[0]['comm'][cat]
                det1.pop(itm)
                print(det1)
                det2['comm'][cat]=det1
                print(det2)
                mongo.db.owner.itm.update({'bid':bid},{'$set':{'comm':det2['comm']}})
                msg='Deleted item : '+itm+' category : '+cat
            else:
                msg='item not found'
        else:
            msg='category not found'

        #print(det1)
        #a=mongo.db.owner.itm.deleteOne({'bid':bid} , {'comm':{cat:{itm:det1}}})
        #print(a)
        print(cat,itm)
        
        return render_template('delete.html',loggedin=True,msg=msg)

@app.route('/logout')
def logout():
    return redirect('/index' )

#def data_store():
    #mongo.db.owner.insert(data)


if __name__=="__main__":
    app.run(debug=True, host='127.0.0.1')
