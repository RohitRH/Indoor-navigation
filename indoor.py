from flask import Flask

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    return '<strong style="font-size:50px;">indoor bitch</strong>'

if __name__ == '__main__':
    app.run(debug=True)
