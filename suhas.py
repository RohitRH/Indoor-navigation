#!/usr/bin/python3
from flask import Flask,request
from flask_pymongo import PyMongo
from flask_restful import Api,Resource

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
    def post(self):
        pass


api.add_resource(Search,'/search')
api.add_resource(Map,'/map')

if __name__ == '__main__':
    app.run(debug=True)
