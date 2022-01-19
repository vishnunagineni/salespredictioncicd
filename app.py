from flask import Flask, request, jsonify
import pandas as pd
import joblib
from sklearn.base import BaseEstimator

class OutletTypeEncoder(BaseEstimator):
    def __init__(self):
        pass
    
    def fit(self,documents,y=None):
        return self
    
    def transform(self,x_dataset):
        x_dataset['outlet_grocery_store'] = (x_dataset['Outlet_Type'] == 'Grocery Store')*1
        x_dataset['outlet_supermarket_3'] = (x_dataset['Outlet_Type'] == 'Supermarket Type3')*1
        x_dataset['outlet_identifier_OUT027'] = (x_dataset['Outlet_Identifier'] == 'OUT027')*1
        return x_dataset

def load_model():
    model=joblib.load("saved_model/model.joblib")
    return model

app = Flask(__name__)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            model=load_model()
            if request.json:
                d=pd.DataFrame(request.json)
                res=model.predict(d)
                print(res[0])
            return jsonify(res[0])
        except:
            return "Something went wrong!!!!"
    else:
        return "Error Occured!!!!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)