from flask import Flask,request
from flask_pymongo import PyMongo
from flask_restful import Api,Resource

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/sample"
mongo = PyMongo(app)
api = Api(app)

class Compare(Resource):
    def post(self):
        data = request.get_json()
        if 'item' in data.keys():
            item = data['item']
            res = mongo.db.sample.find()
            ratings = []
            prices = []
            for i in res:
                for j in i['comm']:
                    if item in j.keys():
                        ratings.append(j[item]['rating'])
                        prices.append(j[item]['price'])

            lowest_cost = min(prices)
            highest_rating = max(ratings)

            lowest_cost_store = mongo.db.sample.find_one({'bid':prices.index(min(prices))+1})['sname']
            print(ratings.index(max(ratings))+1)
            highest_rating_store = mongo.db.sample.find_one({'bid':ratings.index(max(ratings))+1})['sname']

            return {'price_wise':{'store_name':lowest_cost_store,'price':lowest_cost},'rating_wise':{'store_name':highest_rating_store,'rating':highest_rating}}


api.add_resource(Compare,'/compare')

if __name__ == '__main__':
    app.run(debug=True)
