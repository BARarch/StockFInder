from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.embed import components

import requests
from bokeh.models import ColumnDataSource
from dateutil.parser import parse
from datetime import datetime as dt
import pandas as pd

from flask import Flask,render_template,request,redirect

# Load App
app_stock = Flask(__name__)

app_stock.tags = {}

app_stock.parameters = {}
app_stock.parameters['features'] = ('Close', 'Adj. Close', 'Open', 'Adj. Open')
app_stock.nParameters = len(app_stock.parameters)

@app_stock.route('/index_stock',methods=['GET','POST'])
def index_stock():
	if request.method == 'GET':
	 a1, a2, a3, a4 = list(app_stock.parameters.values())[0]	
	 return render_template('layout_symbol_form.html', ans1=a1, ans2=a2, ans3=a3, ans4=a4)
	else:
	 return redirect('/graph_stock')

@app_stock.route('/graph_stock',methods=['POST'])
def graph_stock():

	stock = request.form['symbol_ticker'].upper()
	para = request.form['symbol_feature']
	#print(stock)
	#print('%s'%(request.form['symbol_feature']))

	# API Call
	apiKey = 'qYxY1xupQhFYqX-su67r'
	api_url = ('https://www.quandl.com/api/v1/datasets/WIKI/%s.json?' % stock) + ('api_key=%s' % apiKey)

	session = requests.Session()
	session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
	raw_data = session.get(api_url)

	# Parse to Initial DataFrame
	test_read = pd.read_json(raw_data.text, typ='series')
	df = pd.DataFrame(test_read["data"],columns=test_read["column_names"])

	# Pick Columns to Plot
	dfDatetimes = [dt.strptime(x, '%Y-%m-%d') for x in df.Date]
	dfPara = [x for x in df['%s' % para]]

	source = ColumnDataSource(data={
    	'date' : dfDatetimes,
    	'para' : dfPara,
	})

	# Plot Call with columns
	p = figure(
    	       title='Data from Quandle WIKI set for %s' % stock,
        	   x_axis_label='date',
           	   x_axis_type='datetime')
	p.line('date', 'para', source=source)
	script, div = components(p)

	return render_template('graph_stock.html', script=script, div=div, ticker=stock)

if __name__ == '__main__':
	app_stock.run(debug=True, port=5002)