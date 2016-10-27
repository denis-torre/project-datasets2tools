############################################################
############################################################
############### Datasets2Tools Python Library ##############
############################################################
############################################################

#######################################################
########## 1. Setup ###################################
#######################################################

##############################
##### 1.1 Load Libraries
##############################
# Python Libraries
import pandas as pd

#######################################################
########## 2. Add Functions ###########################
#######################################################

##############################
##### 2.1 Call MySQL SP
##############################

# Calls MySQL Procedure and returns a table

def executeQuery(query, mysql_engine):
	
	# Create cursor
	cursor = mysql_engine.connect().cursor()

	# Call procedure
	cursor.execute(query)

	# Get field names
	field_names = [x[0] for x in cursor.description]

	# Get search results
	query_results = cursor.fetchall()

	# Get query result dataframe
	query_result_dataframe = pd.DataFrame(list(query_results), columns = field_names)

	# Return result
	return query_result_dataframe
