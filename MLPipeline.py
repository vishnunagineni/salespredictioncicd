#!/usr/bin/env python
# coding: utf-8

# In[1]:


#building pipeline for all the above steps

#importing libraries
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import category_encoders as ce
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

#reading training dataset

data=pd.read_csv('SalesPrediction.csv')

data.head()


# In[22]:


from sklearn.model_selection import train_test_split
X=data.drop(["Item_Outlet_Sales"],axis=1)
Y=data[["Item_Outlet_Sales"]]
train_x,test_x,train_y,test_y=train_test_split(X,Y,test_size=0.2)


# In[59]:


x=train_x.head(1).values.tolist()[0]


# In[57]:


y=train_x.head().columns.tolist()


# In[61]:


d={}


# In[67]:


for i in range(0,len(y)):
    d[y[i]]=[x[i]]


# In[68]:


d


# In[69]:


x_in=pd.DataFrame(d)


# In[25]:


#importing baseestimator

from sklearn.base import BaseEstimator

#creating class outlet identifier
#custom transformer must have fit and transform methods
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


# In[26]:


#preprocessing step
#dropping columns
#imputing the missing values
#Scaling the data if needed

pre_process=ColumnTransformer(remainder='passthrough',
                                transformers=[('drop_columns', 'drop', ['Item_Identifier',
                                                                        'Outlet_Identifier',
                                                                        'Item_Fat_Content',
                                                                        'Item_Type',
                                                                        'Outlet_Identifier',
                                                                        'Outlet_Size',
                                                                        'Outlet_Location_Type',
                                                                        'Outlet_Type'
                                                                       ]),
                                              ('impute_item_weight', SimpleImputer(strategy='mean'), ['Item_Weight']),
                                              ('scale_data', StandardScaler(),['Item_MRP'])])


# In[34]:


#Defining pipeline 

"""
Step1: get the updated binary columns
Step2: preprocessing
Step3: Training the model
"""
rf=Pipeline(steps=[('get_outlet_binary_columns', OutletTypeEncoder()), 
                                 ('pre_processing',pre_process),
                                 ('random_forest', RandomForestRegressor(max_depth=10,random_state=2))
                                 ])

#fit the pipeline with training data
rf.fit(train_x,train_y)

#predicting the training values
predictions=rf.predict(test_x)


# In[35]:


RMSE=mean_squared_error(test_y, predictions)**0.5


# In[87]:


import joblib
import os


# In[90]:


if not os.path.exists("saved_model"):
    os.makedirs("saved_model")
model_path=os.path.join("saved_model","model.joblib")


# In[91]:


with open(model_path,"wb") as f:
    joblib.dump(rf,f)

