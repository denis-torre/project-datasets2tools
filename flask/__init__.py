############################################################
############################################################
############### Datasets2Tools Web Interface ###############
############################################################
############################################################

#######################################################
########## 1. Setup Web Page ##########################
#######################################################

##############################
##### 1.1 Python Libraries
##############################
import sys
import pandas as pd
from flask import Flask, request, render_template

##############################
##### 1.2 Custom Libraries
##############################
sys.path.append('static/lib')
from dbConnection import *
from chromeExtensionAPI import *
from dataSubmissionAPI import *

##############################
##### 1.3 Setup App
##############################
# Initialize Flask App
app = Flask(__name__)

# Connect to MySQL
app, mysql = setupLocalMySQLConnection(app)
# app, mysql = setupMySQLConnection(app)

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