# Census Machine learning classification Pipelines 

### The dataset 


[Census Income dataset](https://archive.ics.uci.edu/ml/datasets/Adult)  


* **age**: continuous.
* **workclass**: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
* **fnlwgt**: continuous.
* **education**: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
* **education-num**: continuous.
* **marital-status**: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
* **occupation**: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
* **relationship**: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
* **race**: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
* **sex**: Female, Male.
* **capital-gain**: continuous.
* **capital-loss**: continuous.
* **hours-per-week**: continuous.
* **native-country**: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.
* **lable** 0 ,1

### Pipeline on Vertex AI
![Link Name]("#")  
![Link Name]("#")  

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

# Deploy on Google Cloud Kubernetes

Create a new Docker repository named hieudinh-census-repo  in the location us-central1 with the description "Docker repository"

```
gcloud artifacts repositories create hieudinh-census-repo --repository-format=docker \
    --location=us-central1 --description="Docker repository"
```

Cloudbuild.yaml

 

```                  
steps:
  # Pull the Docker image from Docker Hub
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'pull'
      - 'hieudinhpro/census_api:v1'

  # Tag the pulled image for Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'tag'
      - 'hieudinhpro/census_api:v1'
      - 'us-central1-docker.pkg.dev/${PROJECT_ID}/hieudinh-census-repo/census_api:v1'

  # Push the tagged image to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'us-central1-docker.pkg.dev/${PROJECT_ID}/hieudinh-census-repo/census_api:v1'
```
In Cloud Shell, execute the following command to start a Cloud Build using cloudbuild.yaml as the build configuration file:

```
gcloud builds submit --region=us-central1 --config cloudbuild.yaml
```


### Creating a GKE cluster
```
gcloud config set compute/zone us-central1-f
PROJECT_ID=$(gcloud config get-value project)
CLUSTER_NAME=cluster-1

```
```
gcloud beta container clusters create $CLUSTER_NAME \
  --cluster-version=latest \
  --machine-type=e2-standard-4 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=3 \
  --num-nodes=1 
  ```


### Create deployment.yaml

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: census-api-deployment
spec:
  replicas: 1  
  selector:
    matchLabels:
      app: census-api
  template:
    metadata:
      labels:
        app: census-api
    spec:
      containers:
        - name: census-api-container
          image: us-central1-docker.pkg.dev/${PROJECT_ID}/hieudinh-census-repo/census_api:v1
          ports:
            - containerPort: 8000
```
Run command
```
kubectl apply -f deployment.yaml
```

### Create Service 

```
apiVersion: v1
kind: Service
metadata:
  name: census-api-service
spec:
  selector:
    app: census-api
  ports:
    - protocol: TCP
      port: 8000 # The external port 
      targetPort: 8000 # The container port
  type: LoadBalancer
```
Run commands

```
kubectl apply -f service.yaml

```
