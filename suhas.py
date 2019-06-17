#!/usr/bin/python3
from flask import Flask,request
import pymongo
from flask_restful import Api,Resource
import json
from json import *
from bson.json_util import dumps
import base64,random

app = Flask(__name__)
app.config["MONGO_URI"] = ""
client=pymongo.MongoClient("mongodb://suhas:suhas@owner-shard-00-00-gwlya.mongodb.net:27017,owner-shard-00-01-gwlya.mongodb.net:27017,owner-shard-00-02-gwlya.mongodb.net:27017/owner?ssl=true&replicaSet=owner-shard-0&authSource=admin&retryWrites=true&w=majority",connect=False)
db = client.owner

api = Api(app)

class Search(Resource):
    def get(self):
        data = request.args
        try:
            item = data['item']
            category = data['category']
            all_stores = db.itm.find()

            ratings = []
            prices = []
            quant = []
            stores = []

            for store in all_stores:
                if category in store['comm'].keys() and item in store['comm'][category].keys():
                    stores.append(store['sname'])
                    ratings.append(store['comm'][category][item]['rating'])
                    prices.append(int(store['comm'][category][item]['price']))
                    quant.append(store['comm'][category][item]['quantity'])

            final_list = list(zip(stores,prices,ratings,quant))

            if final_list == []:
                print("\nerror\n")
                return {'error':False,'match':False,'response':None},200
            else:
                price_wise = final_list[:]
                rating_wise = final_list[:]
                price_wise.sort(key=lambda x: x[1])
                rating_wise.sort(key=lambda x: x[2],reverse=True)
                return {'error':False,'match':True,'response':{'price_wise':price_wise,'rating_wise':rating_wise}},200

        except KeyError as e:
            print("key error "+str(e))
            return {'error':True},400

class Map(Resource):
    def get(self):
        # store the images in the database as string:
        f = open('floorplan/'+random.choice(['img1.jpg','img2.jpg','img3.jpg']),'rb')
        data = base64.b64encode(f.read()).decode('utf-8')

        return {'name':f.name,'response':data}

    def post(self):
        data = request.get_json()
        try:
            bid = data['src']
            dest = data['dest']

            store = db.indoor.find({'src':bid,'dest':dest})[0]

            data = store['img_url']

            #data = base64.b64encode(img).decode('utf-8')

            return({'error':False,'response':data})

        except KeyError as e:
            print("key error "+str(e))
            return {'error':True},400

        except IndexError as e:
            print("No such route "+str(e))
            return {'error':True},400

class Marketing(Resource):
    def post(self):
        data = request.get_json()
        try:
            bid = data['bid']

            store = db.itm.find({'bid':bid})

            for i in store:
                ads = i['ads']
                coupons = i['cpn_des']

            data = {'ads':ads,'coupons':coupons}

            return {'error':False,'response':data}
        except KeyError:
            return {'error':True}


api.add_resource(Search,'/search')
api.add_resource(Map,'/map')
api.add_resource(Marketing,'/marketing')

if __name__ == '__main__':
    app.run(debug=True)
