import joblib
import pandas as pd
from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route("/predict",methods=['POST','GET'])
def predict():
    if request.method=='POST':
        model=joblib.load('./saved_model/model.joblib')
        try:
            if request.json:
                d=pd.DataFrame(request.json)
                res=model.predict(d)
                return jsonify(res)
        except:
            return "Something went wrong!!!"

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)

