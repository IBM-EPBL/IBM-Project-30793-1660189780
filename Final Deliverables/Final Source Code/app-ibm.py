import requests

import flask
from flask import request, render_template
from flask_cors import CORS
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "GQLuhAFcsKEFbFY85lykxpF56I9shRwl9wGBCYl95O_p"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = flask.Flask(__name__, static_url_path='')
CORS(app)
 
@app.route('/', methods=['GET'])
def sendHomePage():
    return render_template('index.html')
 
@app.route('/predict', methods=['POST'])
def predictLoanStatus():
    
    gender = float(request.form['gender'])
    married = float(request.form['married'])
    dependents = float(request.form['dependents'])
    edu = float(request.form['edu'])
    semp = float(request.form['semp'])
    appinc = float(request.form['appinc'])
    coappinc = float(request.form['coappinc'])
    lamt = float(request.form['lamt'])
    lamtterm = float(request.form['lamtterm'])
    crhist = float(request.form['crhist'])
    prop = float(request.form['prop'])
    X = [[gender,married,dependents,edu,semp,appinc,coappinc,lamt,lamtterm,crhist,prop]]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields":[[gender,married,dependents,edu,semp,appinc,coappinc,lamt,lamtterm,crhist,prop]], "values":X}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/05f386a7-5d84-43b3-b4e6-d1fa95ea7145/predictions?version=2022-11-20', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())

    print(response_scoring)
    predictions = response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]
    print("Final prediction :",predict)
    
    # showing the prediction results in a UI# showing the prediction results in a UI
    return render_template('predict.html', predict=predict)

if __name__ == '__main__' :
    app.run(debug= False)


