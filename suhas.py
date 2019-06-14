#!/usr/bin/python3
from flask import Flask,request
from flask_pymongo import PyMongo
from flask_restful import Api,Resource
import json
from json import *
from bson.json_util import dumps
import base64

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/sample"
mongo = PyMongo(app)
api = Api(app)

class Search(Resource):
    def get(self):
        data = request.args
        try:
            item = data['item']
            category = data['category']

            all_stores = mongo.db.sample.find()

            ratings = []
            prices = []
            quant = []
            stores = []

            for store in all_stores:
                if category in store['comm'].keys() and item in store['comm'][category].keys():
                    stores.append(store['sname'])
                    ratings.append(store['comm'][category][item]['rating'])
                    prices.append(store['comm'][category][item]['price'])
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
        f = open('img1.jpg','rb').read()
        data = base64.b64encode(f).decode('ascii')

        return {'response':data}

    def post(self):
        data = request.get_json()
        try:
            bid = data['bid']
            src = data['src']
            dest = data['dest']

            store = mongo.db.sample.indoor.find({'bid':bid,'src':src,'dest':dest})[0]

            img = store['img']

            return({'error':False,'response':img})

        except KeyError as e:
            print("key error "+str(e))
            return {'error':True},400

        except IndexError as e:
            print("No such route "+str(e))
            return {'error':True},400

api.add_resource(Search,'/search')
api.add_resource(Map,'/map')

if __name__ == '__main__':
    app.run(debug=True)
