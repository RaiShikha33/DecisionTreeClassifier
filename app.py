from flask import Flask,request
import pandas as pd
import numpy as np
import joblib
from joblib import dump, load
import flasgger
from flasgger import Swagger

# 2.CREATE THE APP OBJECT
app=Flask(__name__)

Swagger(app)
DTclassifier = load('DecisionTree.pkl')

@app.route('/')
def index():
    return  "PREDICTION USING DECISION TREE CLASSIFIER ON WELL LOG DATA"

# 4. EXPOSE THE PREDICTION FUNCTIONALITY, MAKE PREDICTION FROM PASSED JSON DATA AND RETURN THE PREDICTED VALUE
@app.route('/predict',methods=["Get"])
def predict_litho_level():
  """To Predict the Lithology level from well log data
#   This is using docstrings for specifications.
  ---
  parameters:
    - name: RHOB
      in: query
      type: number
      required: true
    - name: GR
      in: query
      type: number
      required: true
    - name: NPHI
      in: query
      type: number
      required: true
    - name: DTC
      in: query
      type: number
      required: true
    - name: DTS
      in: query
      type: number
      required: true
  responses:
       200:
           description: The output values   
  
  """

  RHOB=request.args.get('RHOB')
  GR=request.args.get('GR')
  NPHI=request.args.get('NPHI')
  DTC=request.args.get('DTC')
  DTS=request.args.get('DTS')

  prediction=DTclassifier.predict([[RHOB,GR,NPHI,DTC,DTS]])
  lithoDic = {"[0]":'Sandstone',
              "[1]":'Shale',
              "[2]":'Limestone',
              "[3]":'Coal',
  }

  pred=str(prediction)
  print(pred)
  ans=lithoDic.get(pred)
  print(ans)
  
  return"The Predicted Lithology label is:"+str(pred)+"and Litho Type is:"+str(ans)


@app.route('/predict_file',methods=["POST"])
def predict_litho_level_file():
  """To Predict the Lithology level from well log data
#   This is using docstrings for specifications.
  ---
  parameters:
    - name: file
      in: formdata
      type: file
      required: true
  responses:
    200:
        description: The output values
  """

  train_data=pd.read_csv(request.files.get("file"))
  print(train_data.head())
  prediction=DTclassifier.predict(train_data)

  return "The predicted values for the csv file is:"+ str(list(prediction))


if __name__=='__main__':
  app.run()