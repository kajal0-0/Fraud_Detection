from flask import Flask, render_template, request
import pickle

model = pickle.load(open("xgboost_fraud_model.pkl", "rb"))

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    step = float(request.form['step'])
    trans_type = request.form['type']
    amount = float(request.form['amount'])
    nameOrig = request.form['nameOrig']
    oldbalanceOrg = float(request.form['oldbalanceOrg'])
    newbalanceOrig = float(request.form['newbalanceOrig'])
    nameDest = request.form['nameDest']
    oldbalanceDest = float(request.form['oldbalanceDest'])
    newbalanceDest = float(request.form['newbalanceDest'])
    amount_cleaned = float(request.form['amount_cleaned'])

    type_encoded = {
        'TRANSFER': 0,
        'CASH_OUT': 1,
        'DEBIT': 2,
        'PAYMENT': 3,
        'CASH_IN': 4
    }.get(trans_type, -1)

    nameOrig_encoded = hash(nameOrig) % 1000000
    nameDest_encoded = hash(nameDest) % 1000000

    features = [[
        step, type_encoded, amount, nameOrig_encoded, oldbalanceOrg,
        newbalanceOrig, nameDest_encoded, oldbalanceDest, newbalanceDest, amount_cleaned
    ]]

    prediction = int(model.predict(features)[0])
    result = "Fraudulent Transaction" if prediction == 1 else "Legitimate Transaction"
    return render_template('index.html', predict=result)

if __name__ == '__main__':
    app.run(debug=True)
