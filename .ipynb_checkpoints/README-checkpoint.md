# Census ML Pipelines

Begin by pulling the model server image from my Docker hub

```
docker pull hieudinhpro/census_api:v1

```
Run the server

```
docker run  -d -p  8000:8000 hieudinhpro/census_api:v1 

```

Let's do inference a example , open a new command line window or tab and run the following command:

```
curl -X 'POST' \
  'http://localhost:8000/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age" : 31 ,
  "capital_gain" : 5178,
  "capital_loss" : 0,
  "education" : "Master",
  "education_num" : 14 ,
  "fnlwgt" : 159449 ,
  "hours_per_week" : 40,
  "marital_status" : "Married-civ-spouse",
  "native_country" :  "United-States",
  "occupation" : "Exec-managerial",
  "race" : "White",
  "relationship" : "husband",
  "sex" : "Male",
  "workclass" : "Private"
 
 } 
'
```
output will be like  "Label 1 : [0.8479395]"
