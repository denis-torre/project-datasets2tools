############################################################
############################################################
############### 1. Datasets2Tools Python Library ###########
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
from flaskext.mysql import MySQL

############################################################
############################################################
############### 2. Database Connection #####################
############################################################
############################################################

#######################################################
########## 2.1 Database Connection ####################
#######################################################

##############################
##### 2.1.1 Setup Connection
##############################

# def setupMySQLConnection(app, databaseConnectionFile, connectionLabel):

# 	# Open Connection File
# 	with open(databaseConnectionFile, 'r') as openfile:

# 		# Get JSON
# 		databaseConnectionJson = openfile.readlines()[0]

# 	# Convert to Dictionary
# 	databaseConnectionDict = json.loads(databaseConnectionJson)

# 	# Initialize MySQL Connection
# 	mysql = MySQL()

# 	# Configure MySQL Connection
# 	app.config['MYSQL_DATABASE_USER'] = databaseConnectionDict[connectionLabel]['user']
# 	app.config['MYSQL_DATABASE_PASSWORD'] = databaseConnectionDict[connectionLabel]['password']
# 	app.config['MYSQL_DATABASE_DB'] = databaseConnectionDict[connectionLabel]['db']
# 	app.config['MYSQL_DATABASE_HOST'] = databaseConnectionDict[connectionLabel]['host']
# 	mysql.init_app(app)

# 	# Return app
# 	return app, mysql

def setupMySQLConnection(app):

	# Initialize MySQL Connection
	mysql = MySQL()

	# Configure MySQL Connection
	app.config['MYSQL_DATABASE_USER'] = os.environ['DB_USER']
	app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['DB_PASS']
	app.config['MYSQL_DATABASE_DB'] = os.environ['DB_NAME']
	app.config['MYSQL_DATABASE_HOST'] = os.environ['DB_HOST']
	mysql.init_app(app)

	# Return app
	return app, mysql

##############################
##### 2.1.2 Run MySQL Query
##############################

def executeQuery(queryString, mysqlEngine):
	
	# Create cursor
	cursor = mysqlEngine.connect().cursor()

	# Call procedure
	cursor.execute(queryString)

	# Get field names
	fieldNames = [x[0] for x in cursor.description]

	# Get search results
	queryResults = cursor.fetchall()

	# Get query result dataframe
	query_result_dataframe = pd.DataFrame(list(queryResults), columns = fieldNames)

	# Return result
	return query_result_dataframe

############################################################
############################################################
############### 3. API #####################################
############################################################
############################################################

#######################################################
########## 3.1 Database Queries #######################
#######################################################

##############################
##### 3.1.1 getCannedAnalysisDataframe 
##############################

def getCannedAnalysisDataframe(datasetAccessions, mysqlEngine):

	# Create Comma-Separated String
	datasetAccessionString = "', '".join(datasetAccessions)
	
	# Create Query String
	queryString = ''' SELECT ca.id AS canned_analysis_id, accession, tool_fk AS tool_id, link AS canned_analysis_url
					  FROM canned_analysis ca
					  LEFT JOIN dataset d
					  ON d.id = ca.dataset_fk
					  WHERE accession IN ('%(datasetAccessionString)s') ''' % locals()

	# Perform Query
	canned_analysis_dataframe = executeQuery(queryString, mysqlEngine)#.set_index('canned_analysis_id')

	# Return Result
	return canned_analysis_dataframe

##############################
##### 3.1.2 getCannedAnalysisMetadataDataframe 
##############################

def getCannedAnalysisMetadataDataframe(datasetAccessions, mysqlEngine):

	# Create Comma-Separated String
	datasetAccessionString = "', '".join(datasetAccessions)
	
	# Create Query String
	queryString = ''' SELECT canned_analysis_fk AS canned_analysis_id, variable, value
					  FROM canned_analysis_metadata cam
						  LEFT JOIN canned_analysis ca
						  ON ca.id = cam.canned_analysis_fk
						  	LEFT JOIN dataset d
						  	ON d.id = ca.dataset_fk
					  WHERE accession IN ('%(datasetAccessionString)s') ''' % locals()

	# Perform Query
	canned_analysis_metadata_dataframe = executeQuery(queryString, mysqlEngine)

	# Return Result
	return canned_analysis_metadata_dataframe

##############################
##### 3.1.3 getToolMetadataDataframe 
##############################

def getToolMetadataDataframe(toolIds, mysqlEngine):

	# Create Comma-Separated String
	toolIdString = "', '".join([str(x) for x in toolIds])
	
	# Create Query String
	queryString = ''' SELECT * 
					  FROM tool
					  WHERE id IN ('%(toolIdString)s') ''' % locals()

	# Perform Query
	tool_metadata_dataframe = executeQuery(queryString, mysqlEngine)

	# Return Result
	return tool_metadata_dataframe

#######################################################
########## 3.2 Analysis Description ###################
#######################################################

##############################
##### 3.2.1 createCannedAnalysisDescription 
##############################

def createCannedAnalysisDescription(canned_analysis_metadata, tool_name):

		# Define Toolame2Label Dictionary
		toolname2Label = {'Enrichr': 'Enrichment analysis', 'PAEA': 'PAEA analysis', 'L1000CDS2': 'Signature search', 'Clustergrammer': 'Heatmap visualization', 'Crowdsourcing': 'Crowdsourcing analysis'}

		# Define Direction2Label Dictionary
		direction2Label = {'1': 'overexpressed', '-1': 'underexpressed', '0': 'combined upregulated and downregulated'}

		# Get Differential expression method description
		if 'threshold' in canned_analysis_metadata.keys():

			# Prepare Geneset Info
			genesetInfo = 'most ' + direction2Label[canned_analysis_metadata['direction']] + ' genes '

			# Prepare Method Info
			methodInfo = ' (p < ' + canned_analysis_metadata['threshold'] + ', ' + canned_analysis_metadata['diff_exp_method'] + ' differential expression method, ' + canned_analysis_metadata['ttest_correction_method'] + ' correction)'

		elif 'cutoff' in canned_analysis_metadata.keys():

			# Prepare Geneset Info
			genesetInfo = canned_analysis_metadata['cutoff'] + ' ' + direction2Label[canned_analysis_metadata['direction']] + ' genes' 

			# Prepare Method Info
			methodInfo = ' (' + canned_analysis_metadata['diff_exp_method'] + ' differential expression method)'

		else:

			raise(ValueError('Differential expression method incorrectly annotated!'))

		# Get additional info
		tag_value_pairs = [' '.join([canned_analysis_metadata[tag], tag]) for tag in canned_analysis_metadata.keys() if tag in ['drug', 'perturbation', 'gene', 'cell', 'time', 'temperature', 'organism', 'disease', '']]
		additionalInfo = ', ' + ', '.join(tag_value_pairs)

		# Prepare Result
		return toolname2Label[tool_name] + ' of top ' + genesetInfo + additionalInfo + methodInfo + '.'

#######################################################
########## 3.3 Dictionary Conversion ##################
#######################################################

##############################
##### 3.3.1 getCannedAnalysisMetadataDict 
##############################

def getCannedAnalysisMetadataDict(canned_analysis_metadata_dataframe):

	# Define Metadata Dict
	canned_analysis_metadata_dict = {cannedAnalysisId: {} for cannedAnalysisId in canned_analysis_metadata_dataframe['canned_analysis_id']}

	# Loop Through Canned Analyses
	for cannedAnalysisId in canned_analysis_metadata_dict.keys():
    
	    # Get Dataframe Subset
	    metadata_dataframe_subset = canned_analysis_metadata_dataframe.loc[canned_analysis_metadata_dataframe['canned_analysis_id'] == cannedAnalysisId, ['variable', 'value']]
	    
	    # Loop Through Variables and Values
	    for variable, value in metadata_dataframe_subset.as_matrix():
	        
	        # Add Value to Variable
	        canned_analysis_metadata_dict[cannedAnalysisId][variable] = value

    # Return Result
	return canned_analysis_metadata_dict

##############################
##### 3.3.2 getCannedAnalysesDict
##############################

def getCannedAnalysisData(canned_analysis_dataframe, canned_analysis_metadata_dict, tool_metadata_dataframe):

	# Define Dictionary
	canned_analyses_dict = {datasetAccession:{} for datasetAccession in set(canned_analysis_dataframe['accession'])}

	# Get Tool Dict
	tool_metadata_dict = tool_metadata_dataframe.set_index('id').to_dict('index')

	# Loop Through Datasets
	for datasetAccession in canned_analyses_dict.keys():
	    
	    # Get Dataframe Subset
	    canned_analysis_dataframe_subset = canned_analysis_dataframe.loc[canned_analysis_dataframe['accession'] == datasetAccession, :]

	    # Loop Through Tools
	    for toolId in set(canned_analysis_dataframe_subset['tool_id']):

	    	# Add Key
	    	canned_analyses_dict[datasetAccession][toolId] = {}

	    	# Loop Through Canned Analyses
	    	for cannedAnalysisId, cannedAnalysisUrl in canned_analysis_dataframe_subset.loc[canned_analysis_dataframe_subset['tool_id'] == toolId, ['canned_analysis_id', 'canned_analysis_url']].as_matrix():
	        
		        # Add URL
		        canned_analyses_dict[datasetAccession][toolId][cannedAnalysisId] = canned_analysis_metadata_dict[cannedAnalysisId]
		        canned_analyses_dict[datasetAccession][toolId][cannedAnalysisId]['canned_analysis_url'] = cannedAnalysisUrl
		        canned_analyses_dict[datasetAccession][toolId][cannedAnalysisId]['description'] = createCannedAnalysisDescription(canned_analysis_metadata_dict[cannedAnalysisId], tool_metadata_dict[toolId]['tool_name'])

	# Return Result
	return {'canned_analyses': canned_analyses_dict, 'tools': tool_metadata_dict}

#######################################################
########## 3.3 Wrapper ################################
#######################################################

##############################
##### 3.3.1 mainAPI 
##############################

def mainAPI(datasetAccessions, mysqlEngine):

	# Get Canned Analysis Dataframe
	canned_analysis_dataframe = getCannedAnalysisDataframe(datasetAccessions, mysqlEngine)

	# Get Metadata Dataframe
	canned_analysis_metadata_dataframe = getCannedAnalysisMetadataDataframe(datasetAccessions, mysqlEngine)

	# Get Canned Analysis Metadata Dataframe
	canned_analysis_metadata_dict = getCannedAnalysisMetadataDict(canned_analysis_metadata_dataframe)

	# Get Tool Metadata Dataframe
	tool_metadata_dataframe = getToolMetadataDataframe(set(canned_analysis_dataframe['tool_id']), mysqlEngine)

	# Get Data
	canned_analysis_data = getCannedAnalysisData(canned_analysis_dataframe, canned_analysis_metadata_dict, tool_metadata_dataframe)

	# Convert to JSON
	canned_analysis_data_json = json.dumps(canned_analysis_data)

	# Return Canned Analysis Data
	return canned_analysis_data_json
