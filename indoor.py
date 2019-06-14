from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/sample"
mongo = PyMongo(app)

@app.route('/',methods=['GET','POST'])
def home():
    return(str((mongo.db.name)))

if __name__ == '__main__':
    app.run(debug=True)
