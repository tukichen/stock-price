import os
import numpy as np
import pandas as pd
import simplejson as json
import requests
import quandl

import bokeh
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

from flask import Flask,render_template,request, redirect
# ----------------------------------------------------------------------
app = Flask(__name__)

# a dict to collect input data
app.vars = {}

##########################################################################
@app.route('/')
def homepg():
    return redirect('/index')

##########################################################################
@app.route('/index',methods=['GET','POST'])
def index():
    
    if request.method == 'GET':
        return render_template('userinfo.html' )
    else:        #request was a POST
        # name is a list of stock tickers
        app.vars['name'] = request.form['name'].split(',')
        # input_faeture = open, close, high, low
        app.vars['input_feature'] = []
        if request.form['open']:  app.vars['input_feature'].append(' - Open')
        if request.form['close']: app.vars['input_feature'].append(' - Close')
        if request.form['high']:  app.vars['input_feature'].append(' - High')
        if request.form['low']:   app.vars['input_feature'].append(' - Low')
        
        f = open('%s_price.txt'%(app.vars['name']),'w')
        f.write('Name: %s\n'%(app.vars['name']))
        f.write('price'+ '|'.join(app.vars['input_feature'])+'\n')
        f.close()
        
        
        
        #-------------------return html plot from bokeh----------------------
        return render_template('stocks.html')


##########################################################################

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
