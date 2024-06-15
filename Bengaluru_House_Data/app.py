from flask import Flask,render_template,request,url_for
import json
import pickle
import numpy as np

app = Flask(__name__)

with open("columns.json") as f:
    data=json.load(f)
    
   

with open("data.json") as f:
    datacolumns=json.load(f)['data_columns']

with open("bangalore_home_price_model2.pickle","rb") as f:
    model=pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html',data = data)

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        area= int(request.form['area'])
        bhk= int(request.form['bhk'])
        bath= int(request.form['bathrooms'])
        location= request.form['location']
        print(area)
        print(bhk)
        print(bath)
        print(location)
        location_lower = location.lower()
        try:
            loc_index=datacolumns.index(location_lower)
            print(loc_index)
        except:
            loc_index =-1
        x = np.zeros(244)  
        x[0] = float(area)
        x[1] = bath
        x[2] = bhk
        if loc_index >=0:
            x[loc_index] =1
        # Predict
        estimated_price = model.predict([x])[0]
        print(estimated_price)
        # Round the predicted price to two decimal places
        estimated_price_rounded = round(estimated_price, 2)
        # Round the predicted price to two decimal places
        estimated_price_rounded = round(estimated_price, 2)
        return render_template('predict.html',data = data,predicted_value=estimated_price_rounded,location=location.capitalize(),bath=bath,bhk=bhk,total_sqft=float(area))

if __name__ == '__main__':
    app.run(debug=True)