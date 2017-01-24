############################################################
############################################################
############### Datasets2Tools dbConnection Module #########
############################################################
############################################################

#######################################################
########## 1.1 Setup ##################################
#######################################################

##############################
##### 1.1.1 Load Libraries
##############################
# Python Libraries
import json, os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

############################################################
############################################################
############### 2. Database Connection #####################
############################################################
############################################################

#######################################################
########## 2.1 Database Connection ####################
#######################################################

##############################
##### 2.1.1 Local Connection
##############################

# def setupLocalMySQLConnection(app, connectionLabel='phpmyadmin', databaseConnectionFile='static/dbconnection/dbconnection.json'):

# 	# Open Connection File
# 	with open(databaseConnectionFile, 'r') as openfile:

# 		# Get JSON and convert to dictionary
# 		databaseConnectionDict = json.load(openfile)

	# # Get URI string
	# uriString = 'mysql://' + databaseConnectionDict[connectionLabel]['user'] + ':' + databaseConnectionDict[connectionLabel]['password'] + '@' + databaseConnectionDict[connectionLabel]['host'] + '/' + databaseConnectionDict[connectionLabel]['db'] 

	# # Add URI
	# app.config['SQLALCHEMY_DATABASE_URI'] = uriString

	# # Hide track modifications
	# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# # Setup engine
	# mysql = SQLAlchemy(app).engine

	# # Return app
	# return app, mysql

##############################
##### 2.1.2 Marathon Connection
##############################

def setupMySQLConnection(app):

	# Get URI string
	uriString = 'mysql://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASS'] + '@' + os.environ['DB_HOST'] + '/' + os.environ['DB_NAME']

	# Add URI
	app.config['SQLALCHEMY_DATABASE_URI'] = uriString

	# Hide track modifications
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# Setup engine
	mysql = SQLAlchemy(app).engine

	# Return app
	return app, mysql

#######################################################
########## 2.2 Database Commands ######################
#######################################################

##############################
##### 2.2.1 Insert data
##############################

def insertData(insertCommandString, mysql, returnInsertId=True):
	
	# Create connection
	mysqlConnection = mysql.engine.connect()

	# Insert data
	mysqlConnection.execute(insertCommandString)

	# Return ID
	if returnInsertId:

		# Get insert ID
		lastInsertId = int(mysqlConnection.execute('SELECT LAST_INSERT_ID()').fetchone()[0])

		# Return
		return lastInsertId


##############################
##### 2.2.1 Execute Query
##############################

def executeQuery(queryString, mysql):
	
	# Get query result dataframe
	query_result_dataframe = pd.read_sql(queryString, mysql)

	# Return result
	return query_result_dataframe
	
##############################
##### 2.2.1 Execute Query
##############################

def insertDataframe(dataframe, tableName, mysql):
	
	# Get query result dataframe
	# dataframe.to_sql(tableName, mysql, if_exists=if_exists, index=index, index_label=index_label)

	# Get column names
	colNames = dataframe.columns

	# Set columns string
	columnsString = "`, `".join(colNames)

	# Set values string
	valuesString = "(" + "),(".join([", ".join(['"%(y)s"' % locals() for y in x]) for x in dataframe[colNames].as_matrix()]) + ")"

	# Create insert command
	insertCommandString = ''' INSERT IGNORE INTO %(tableName)s
		                      (`%(columnsString)s`)
		                      VALUES %(valuesString)s''' % locals()

    # Insert data
	insertData(insertCommandString, mysql, returnInsertId=False)
