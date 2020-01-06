import pandas as pd
from plotly.offline import plot
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import string
import os
from werkzeug.utils import secure_filename
from res import convert, file_tokenize, fetch_name, fetch_email,fetch_contact, fetch_degree, convert1,path
from flask import jsonify
from flask import Flask, redirect, url_for, render_template, request, Markup
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'tmp'

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template("car.html")

@app.route('/jd',methods = ['POST','GET'])
def menus():

    res = dict()
    if request.method == 'POST':
        f=request.files['file1']
        e=request.form['fname']
        l=request.form.get('location')

        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], "test."+filename.split(".")[1]))
        out = app.config['UPLOAD_FOLDER']+'/'+ "test."+filename.split(".")[1]
       
        data = convert(out)
        re = convert1(data=data,exp=e,location=l)
        tokenized_data = file_tokenize(data=data)
        #res["Degree"] = fetch_degree(tokenized_data)
        res["Email"] = fetch_email(data=data)
        res["Phone"] = fetch_contact(data=data)       
        res["Name"] = fetch_name(data=data)

    if isinstance(re, pd.DataFrame):
        return render_template('car.html',result=res,da = re.to_html())
    else:
        return render_template('car.html',result=res,stt = re)

	
if __name__ == '__main__':
   app.run()