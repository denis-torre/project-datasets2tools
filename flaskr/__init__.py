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
import sys
import pandas as pd

# Flask Libraries
from flask import Flask, request, render_template
from flaskext.mysql import MySQL

# Custom libraries
sys.path.append('static/lib')
from lib import *

##############################
##### 1.2 Setup MySQL
##############################
# Initialize Flask App
app = Flask(__name__)

# Initialize MySQL Connection
mysql = MySQL()

# Configure MySQL Connection
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MyNewPass'
app.config['MYSQL_DATABASE_DB'] = 'datasets2tools'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#######################################################
########## 2. Setup Web Page ##########################
#######################################################

##############################
##### 2.1 Connection Setup
##############################

### 2.1.1 Main
@app.route('/')
def main():
	return render_template('index.html')

### 2.1.2 Save Canned Analysis
@app.route('/save')
def save():
	# Query tools
	tool_dataframe = executeQuery("SELECT * FROM tool", mysql)
	return render_template('save.html', tool_dataframe=tool_dataframe)

### 2.1.3 Dataset Search
@app.route('/datasetSearch', methods=['POST'])
def datasetSearch():
	dataset_search_query = request.form['dataset_search_query']
	return dataset_search_query




#######################################################
########## 3. Run Flask App ###########################
#######################################################
# Run App
if __name__ == "__main__":
	app.run(debug=True)