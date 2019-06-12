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
            print(final_list)

            if final_list == []:
                return {'error':False,'match':False,'response':None},200

            return {'error':False,'match':True,'response':final_list},200
        except KeyError:
            return {'error':True},400

api.add_resource(Search,'/search')

if __name__ == '__main__':
    app.run(debug=True)
