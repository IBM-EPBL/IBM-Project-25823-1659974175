import numpy as np
import os
import requests
from flask import Flask, request, render_template, redirect, url_for
import pickle
# from cloudant.client import Cloudant

filename = 'Linear_Regression.pkl'

regressor = pickle.load(open(filename, 'rb'))

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "zVsoaE6d4nyR7hKtiXZi19ElXPmpHmrbXIB3mzjI3UcE"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    temp_array = list()

    if request.method == 'POST':
        #gre_score = request.form["gre"]
        #toefl_score = request.form["tofl"]
        #university_rating = request.form["rating"]
        #sop = request.form["sop"]
        #lor = request.form["lor"]
        #cgpa = request.form["cgpa"]
        #research = request.form["research"]

        gre_score = int(request.form["gre"])
        toefl_score = int(request.form["tofl"])
        university_rating= int(request.form["rating"])
        sop = float(request.form["sop"])
        lor = float(request.form["lor"])
        cgpa = float(request.form["cgpa"])
        research = request.form["research"]
        payload_scoring = {"input_data": [{"field": ["GRE Score", "TOEFL Score", "University Rating", "SOP", "LOR", "CGPA", "Research", "Chance of Admit"], "values": [[gre_score, toefl_score, university_rating, sop, lor, cgpa]]}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/eede2024-9b01-4f89-8f2b-9d0cb309fae0/predictions?version=2022-11-17', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        predictions = response_scoring.json()
        print(predictions)
        pred = predictions['predictions'][0]['values'][0][0]
        print(gre_score)
        print(toefl_score)
        print(university_rating)
        print(sop)
        print(lor)
        print(cgpa)

        temp_array = temp_array + [gre_score, toefl_score, university_rating, sop, lor, cgpa]
        data = np.array([temp_array])
        print(data)
        print(temp_array)
        my_prediction = int(regressor.predict(data)[0])
        print(my_prediction)
        return render_template('result.html',lower_limit=my_prediction)
	
if __name__ == "__main__":
    app.run(debug=True)