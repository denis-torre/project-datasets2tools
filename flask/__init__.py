############################################################
############################################################
############### Datasets2Tools Web Interface ###############
############################################################
############################################################

#######################################################
########## 1. Setup Web Page ##########################
#######################################################

##############################
##### 1.1 Load Libraries
##############################
# Python Libraries
# import os
import sys, urlparse, os
import pandas as pd

# Flask Libraries
from flask import Flask, request, render_template

# Custom libraries
sys.path.append('/datasets2tools/flask/static/lib')
sys.path.append('static/lib')
from lib import *

##############################
##### 1.2 Setup App
##############################
# Initialize Flask App
app = Flask(__name__)

# Get Connection File
# databaseConnectionFile = '/app/flaskr/static/dbconnection/dbconnection.json'
# databaseConnectionFile = 'static/dbconnection/dbconnection.json'

# Connect to MySQL
# app, mysql = setupMySQLConnection(app, databaseConnectionFile, 'phpmyadmin')
app, mysql = setupMySQLConnection(app)

#######################################################
########## 2. Setup Web Page ##########################
#######################################################

##############################
##### 2.1 Connection Setup
##############################

### 2.1.1 Main
@app.route('/datasets2tools')
def main():
	return 'hello'

##############################
##### 2.2 API
##############################
### 2.2.1
@app.route('/datasets2tools/data')
def data():
	if '?' in request.url:
		datasetAccessions = request.url.split('?')[1].split('+')
		return mainAPI(datasetAccessions, mysql)
	else:
		return 'data'

#######################################################
########## 3. Run Flask App ###########################
#######################################################
# Run App
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')