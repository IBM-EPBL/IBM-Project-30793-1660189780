import flask
from flask import request, render_template
from flask_cors import CORS
import joblib
 
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
    modelx = joblib.load('modelx.pkl')
    status = modelx.predict(X)[0]
    return render_template('predict.html',predict=status)
 
if __name__ == '__main__':
    app.run()

    