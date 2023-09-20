from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf


app = FastAPI()


model_path = "../serving-dir/1694455820/"
loaded_model = tf.keras.models.load_model(model_path)


### api 

#  {
#   "age" : 31 ,
#   "capital_gain" : 5178,
#   "capital_loss" : 0,
#   "education" : "Master",
#   "education_num" : 14 ,
#   "fnlwgt" : 159449 ,
#   "hours_per_week" : 40,
#   "marital_status" : "Married-civ-spouse",
#   "native_country" :  "United-States",
#   "occupation" : "Exec-managerial",
#   "race" : "White",
#   "relationship" : "husband",
#   "sex" : "Male",
#   "workclass" : "Private"
 
#  } 


class item(BaseModel):

    age : int
    capital_gain : int
    capital_loss : int 
    education : str 
    education_num : int
    fnlwgt : int
    hours_per_week : int
    marital_status : str 
    native_country : str 
    occupation : str 
    race : str 
    relationship : str 
    sex : str 
    workclass : str


@app.post('/')
async def create(items : item):

    example  = {
    'age': tf.constant([[items.age]], dtype=tf.int64),
    'capital-gain': tf.constant([[items.capital_gain]], dtype=tf.int64),
    'capital-loss': tf.constant([[items.capital_loss]], dtype=tf.int64),
    'education': tf.constant([[items.education]], dtype=tf.string),
    'education-num': tf.constant([[items.education_num]], dtype=tf.int64),
    'fnlwgt': tf.constant([[items.fnlwgt]], dtype=tf.int64),
    'hours-per-week': tf.constant([[items.hours_per_week]], dtype=tf.int64),
    'marital-status': tf.constant([[items.marital_status]], dtype=tf.string),
    'native-country': tf.constant([[ items.native_country]], dtype=tf.string),
    'occupation': tf.constant([[items.occupation]], dtype=tf.string),
    'race': tf.constant([[ items.race]], dtype=tf.string),
    'relationship': tf.constant([[ items.relationship]], dtype=tf.string),
    'sex': tf.constant([[items.sex]], dtype=tf.string),
    'workclass': tf.constant([[items.workclass]], dtype=tf.string),
    }
    print(example)

    # transform example 
    transformed_examples = loaded_model.tft_layer(example)
    # inference function
    y_pred = loaded_model(transformed_examples)
    y_pred = y_pred.numpy()
    if y_pred <= 0.5 :
        return f"Label 0 : {y_pred}"
    else :
        return f"Label 1 :{y_pred}"
   

#run server uvicorn main:app --reload