import os
import numpy as np
import pandas as pd
import simplejson as json
import requests
import quandl

import bokeh
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file,save

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
        # name is a list of stock tickers, change to upper case and split into a list
        app.vars['name'] = request.form['name'].upper().split(',')
        # input_faeture = open, close, high, low
        app.vars['input_feature'] = []
        if request.form.get('open'):  app.vars['input_feature'].append(' - Open')
        if request.form.get('close'): app.vars['input_feature'].append(' - Close')
        if request.form.get('high'):  app.vars['input_feature'].append(' - High')
        if request.form.get('low'):   app.vars['input_feature'].append(' - Low')
    

        #----------------------start python analysis and bokeh plot----------------
        tickers = app.vars['name']        # A list of tickers
        input_feature = app.vars['input_feature']   # A list of features to show
        # create a list of dataset names
        dset =[]
        for ticker in tickers:
            dset.append("WIKI/"+ ticker +"-Open")
        
        #get stock data in pandas dataframe
        stock = quandl.get(dataset= dset,  api_key= 'wad4CxZw1s-6BTGhjei6', returns= 'pandas' )
        # column names to select from pandas data
        features =[]
        for ds in dset:
            for f in input_feature:
                features.append(ds + f)

        # select only features wanted
        stock_data= stock.loc[:, features]
        stock_data['Date'] = stock_data.index.values.astype('datetime64[ns]')

        color_list = ['red','#33A02C','#B2DF8A','#FB9A99' ]  # list 4 colors for lines
        plot_list =[]   # empty list of plots
    



        for x in tickers:
            globals()['p%s' % x] = figure(x_axis_type="datetime", title="Stock Prices: "+x)
            globals()['p%s' % x].grid.grid_line_alpha=0.3
            globals()['p%s' % x].xaxis.axis_label = 'Date'
            globals()['p%s' % x].yaxis.axis_label = 'Price'
            globals()['p%s' % x].ygrid.band_fill_color = "olive"
            globals()['p%s' % x].ygrid.band_fill_alpha = 0.04
    
            for f in input_feature :
                i= input_feature.index(f)
                #print(i, x, f)
                globals()['p%s' % x].line(stock_data['Date'], stock_data['WIKI/'+x+'-Open'+f], color= color_list[i], legend= x+f)
    
            globals()['p%s' % x].legend.location = "top_left"
    
            plot_list.append(globals()['p%s' % x])

        '''#----------------------------------------
        f = open('%s_price.txt'%(app.vars['name']),'w')
        f.write('Name: %s\n'%(app.vars['name']))
        f.write('price'+ '|'.join(app.vars['input_feature'])+'\n')
        f.write('column'+ '|'.join(features)+'\n')
        f.write('plot'+ '|'.join(tickers)+'\n')
        f.close()
        #---------------------------------------'''
        output_file("./templates/stock.html", title="Stock Price")
        save(gridplot([plot_list], plot_width=600, plot_height=600))  # open a browser
        return render_template('stock.html')
        #script, div = components(plot_list)
        #-------------------return html plot from bokeh----------------------
        #return render_template('stocks.html', script=script, div=div)


##########################################################################

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
