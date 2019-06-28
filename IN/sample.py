from flask import Flask, render_template, url_for, request, session, redirect, make_response, session
from flask_pymongo import PyMongo
import pymongo
import datetime
from datetime import date

app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/owner"

#mongo = PyMongo(app)


client = pymongo.MongoClient("mongodb uri ")
db = client.owner




app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
# sess = Session()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/index")
def index():
    lgin = False
    session['login'] = lgin
    data={}
    items={}
    session['data'] = data
    session['items'] = items
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == 'GET'):
        return render_template('register.html')
    if (request.method == 'POST'):
        email = request.form['email']
        mobile = request.form['mobile']
        bid = request.form['bid']
        sname = request.form['sname']
        uname = request.form['uname']
        pw = request.form['password']
        a = db.users.find({'uname': uname})
        if (a.count() != 0):
            return render_template('register.html', msg="Username already exists try another")
        users = {"email": email, "mobile": mobile, "bid": bid, "sname": sname, "uname": uname, "pass": pw}
        db.users.insert(users)
        return redirect('/index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',alert=False)
    if request.method == 'POST':
        user = request.form['user']
        pw = request.form['pw']
        a = db.users.find({'uname': user, 'pass': pw})
        # print(a.count())
        if (a.count() != 0):
            session['my_var'] = user
            lgin=session.get('login', None)
            lgin=True
            session['login'] = lgin
            det = db.users.find({'uname': user})
            # print(det[0]['sname'])
            #sname = det[0]['sname']
            bid = det[0]['bid']
            det1 = db.itm.find({'bid': bid})
            if(det1.count()!=0):
                return redirect(url_for('decide'))
            return redirect(url_for('store_data'))
        return render_template('login.html', msg="Incorrect Username or Password",alert=True)


@app.route('/decide')
def decide():
    lgin = session.get('login', None)
    if(lgin==True):
        return render_template('decide.html', loggedin=True)
    return render_template('login.html')


@app.route('/store_data', methods=['GET', 'POST'])
def store_data():
    # print()
    if request.method == 'GET':
        lgin = session.get('login', None)
        if (lgin == True):
            return render_template('store_data.html', loggedin=True)
        return render_template('login.html')
    if request.method == 'POST':
        user = session.get('my_var', None)
        # print(user)
        data = session.get('data', None)
        det = db.users.find({'uname': user})
        # print(det[0]['sname'])
        sname = det[0]['sname']
        bid = det[0]['bid']
        # print('cpn' in request.form.keys())
        cpn = request.form['cpn']
        cpn_des = request.form['cpn_des']
        adv = request.form['adv']
        data['bid'] = bid
        data['ads'] = adv
        data['cpn'] = cpn
        data['cpn_des'] = cpn_des
        data['sname'] = sname
        session['data'] = data
        print(data)
        return render_template('item.html', loggedin=True)


@app.route('/item', methods=['GET', 'POST'])
def item():
    if request.method == 'GET':
        lgin = session.get('login', None)
        if (lgin == True):
            return render_template('item.html')
        return render_template('login.html')
    if request.method == 'POST':
        items = session.get('items', None)
        data = session.get('data', None)
        item = request.form['item']
        cat = request.form['cat']
        price = request.form['price']
        qty = request.form['qty']
        rating = 5
        if (cat in items.keys()):
            items[cat][item] = {'price': price, 'quantity': qty, 'rating': rating}
        else:
            items[cat] = {item: {'price': price, 'quantity': qty, 'rating': rating}}
        # data['comm']=items
        session['data'] = data
        session['items'] = items
        print(items)
        print(data)
        return render_template('item.html', loggedin=True)


@app.route('/add_to_db')
def add_to_db():
    items = session.get('items', None)
    data = session.get('data', None)
    data['comm'] = items
    print(data)
    db.itm.insert(data)
    data.clear()
    items.clear()
    session['data'] = data
    session['items'] = items
    return render_template('decide.html', loggedin=True)


@app.route('/add_updated_item', methods=['GET', 'POST'])
def add_updated_item():
    if request.method == 'GET':
        lgin = session.get('login', None)
        if (lgin == True):
            return render_template('update.html', loggedin=True)
        return render_template('login.html')
    if request.method == 'POST':
        items = session.get('items', None)
        data = session.get('data', None)
        item = request.form['item']
        cat = request.form['cat']
        price = request.form['price']
        qty = request.form['qty']
        rating = 5

        # session['cat'] = cat
        # session['item'] = item
        if (cat in items.keys()):
            items[cat][item] = {'price': price, 'quantity': qty, 'rating': rating}
        else:
            items[cat] = {item: {'price': price, 'quantity': qty, 'rating': rating}}
        print(items)
        # print(data)
        session['data'] = data
        session['items'] = items
        return render_template('update.html', loggedin=True)


@app.route('/update_itm')
def update_itm():
    if(session['login']==False):
        return render_template('login.html')
    #db.itm.find()
    items = session.get('items', None)
    data = session.get('data', None)
    print("i am into updattte items")
    user = session.get('my_var', None)
    # cat = session.get('cat', None)
    # item = session.get('item', None)
    cat = []
    item = []
    for j in items.keys():
        cat.append(j)
    for j in cat:
        for k in items[j].keys():
            item.append(k)
    print('cat= ', cat)
    print('items= ', item)
    print(user)
    get_bid = db.users.find({'uname': user})
    bid = get_bid[0]['bid']
    det = db.itm.find({'bid': bid})
    copy_comm = det[0]['comm']
    print(det)
    print(copy_comm)
    print(data)
    print(items)
    for j in cat:
        for k in item:
            if (j in copy_comm.keys()):
                if (k in items[j].keys()):
                    copy_comm[j][k] = items[j][k]
            else:
                copy_comm[j] = items[j]
    print(copy_comm)
    db.itm.update({'bid': bid}, {'$set': {'comm': copy_comm}})
    cat.clear()
    item.clear()
    data.clear()
    items.clear()
    session['data'] = data
    session['items'] = items
    return render_template('decide.html', loggedin=True)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if (request.method == 'GET'):
        lgin = session.get('login', None)
        if (lgin == True):
            return render_template('delete.html', loggedin=True)
        return render_template('login.html')
    if (request.method == 'POST'):
        cat = request.form['cat']
        itm = request.form['item']
        user = session.get('my_var', None)
        get_bid = db.users.find({'uname': user})
        bid = get_bid[0]['bid']
        det = db.itm.find({'bid': bid})

        det2 = det[0]
        print(det[0])
        if (cat in det[0]['comm'].keys()):
            if (itm in det[0]['comm'][cat].keys()):
                det1 = det[0]['comm'][cat]
                det1.pop(itm)
                print(det1)
                det2['comm'][cat] = det1
                print(det2)
                db.itm.update({'bid': bid}, {'$set': {'comm': det2['comm']}})
                msg = 'Deleted item : ' + itm + '  and category : ' + cat
            else:
                msg = 'item not found'
        else:
            msg = 'category not found'

        # print(det1)
        # a=db.itm.deleteOne({'bid':bid} , {'comm':{cat:{itm:det1}}})
        # print(a)
        print(cat, itm)

        return render_template('delete.html', loggedin=True, msg=msg)

@app.route('/update_cpn' , methods=['GET','POST'])
def update_cpn():
    if request.method == 'GET':
        lgin = session.get('login', None)
        if (lgin == True):
            return render_template('update_cpn.html', loggedin=True)
        return render_template('login.html')
    if request.method == 'POST':
        cpn = request.form['cpn']
        cpn_des = request.form['cpn_des']
        adv = request.form['adv']
        user = session.get('my_var', None)
        # print(user)
        det = db.users.find({'uname': user})
        bid=det[0]['bid']
        db.itm.update({'bid':bid},{'$set':{'cpn':cpn , 'cpn_des':cpn_des , 'adv':adv}})
        return render_template('decide.html',loggedin=True)


@app.route('/footfall',methods=['GET','POST'])
def footfall():
    user = session.get('my_var', None)
    det = db.users.find({'uname': user})
    bid = det[0]['bid']
    footfall = db.footfall.find({'bid': bid})
    yearno = str(date.today().isocalendar()[0])
    weekNumber = (date.today().isocalendar()[1])
    weekNumber = str(weekNumber - 1)
    last_week_data = footfall[0][yearno][weekNumber]
    count = []
    for i in last_week_data.values():
        count.append(i)
    prev_year = str(int(yearno) - 1)
    last_year_data = footfall[0][prev_year][weekNumber]
    count1 = []
    for i in last_year_data.values():
        count1.append(i)
    if(request.method=='GET'):
        return render_template('footfall.html',loggedin=True,count=count,count1=count1,check=False,msg="YOU WILL FIND MORE DETAILS BELOW")
    if(request.method=='POST'):
        input_date=request.form['date']
        day,month,year = input_date.split('/')
        input_weekno=datetime.date(int(year), int(month), int(day)).isocalendar()[1]
        count3=[]
        msg=""
        dayofweek = datetime.date(int(year), int(month), int(day)).strftime("%A")
        print(dayofweek)
        if(str(year) in footfall[0].keys()):
            if(str(input_weekno) in footfall[0][year].keys()):
                count3=footfall[0][year][str(input_weekno)][dayofweek]
                check=True
        if(count3==[]):
            check=False
            msg="DATA NOT FOUND FOR THIS DATE"
        return render_template('footfall.html',loggedin=True,count1=count1,count=count,count3=count3,check=check,msg=msg,dayofweek=dayofweek)

        
        
        

@app.route('/logout')
def logout():
    session['login']=False
    return redirect('/index')


# def data_store():
# db.insert(data)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')
