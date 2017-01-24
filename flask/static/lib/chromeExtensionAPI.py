############################################################
############################################################
############### Datasets2Tools Extension API Module ########
############################################################
############################################################

#######################################################
########## 1.1 Setup ##################################
#######################################################

##############################
##### 1.1.1 Python Libraries
##############################
import json, sys
import pandas as pd

##############################
##### 1.1.2 Custom Libraries
##############################
sys.path.append('.')
from dbConnection import *

############################################################
############################################################
############### 2. Data Aggregation ########################
############################################################
############################################################

#######################################################
########## 2.1 Database Queries #######################
#######################################################

##############################
##### 2.1.1 Canned Analyses 
##############################

def getCannedAnalysisDataframe(datasetAccessions, mysqlEngine):

	# Create Comma-Separated String
	datasetAccessionString = "', '".join(datasetAccessions)
	
	# Create Query String
	queryString = ''' SELECT ca.id AS canned_analysis_id, dataset_accession, tool_fk AS tool_id, canned_analysis_url
					  FROM canned_analysis ca
					  LEFT JOIN dataset d
					  ON d.id = ca.dataset_fk
					  WHERE dataset_accession IN ('%(datasetAccessionString)s') ''' % locals()

	# Perform Query
	canned_analysis_dataframe = executeQuery(queryString, mysqlEngine)

	# Return Result
	return canned_analysis_dataframe

##############################
##### 2.1.2 Canned analysis metadata 
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
					  WHERE dataset_accession IN ('%(datasetAccessionString)s') ''' % locals()

	# Perform Query
	canned_analysis_metadata_dataframe = executeQuery(queryString, mysqlEngine)

	# Return Result
	return canned_analysis_metadata_dataframe

##############################
##### 2.1.3 Tool metadata 
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
########## 2.2 Description Creation ###################
#######################################################

##############################
##### 2.2.1 Create description 
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

############################################################
############################################################
############### 3. Data Manipulation #######################
############################################################
############################################################

#######################################################
########## 3.1 Dictionary Conversion ##################
#######################################################

##############################
##### 3.1.1 Get metadata dictionary 
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
##### 3.1.2 Get canned analysis dictionary
##############################

def getCannedAnalysisData(canned_analysis_dataframe, canned_analysis_metadata_dict, tool_metadata_dataframe):

	# Define Dictionary
	canned_analyses_dict = {datasetAccession:{} for datasetAccession in set(canned_analysis_dataframe['dataset_accession'])}

	# Get Tool Dict
	tool_metadata_dict = tool_metadata_dataframe.set_index('id').to_dict('index')

	# Loop Through Datasets
	for datasetAccession in canned_analyses_dict.keys():
	    
	    # Get Dataframe Subset
	    canned_analysis_dataframe_subset = canned_analysis_dataframe.loc[canned_analysis_dataframe['dataset_accession'] == datasetAccession, :]

	    # Loop Through Tools
	    for toolId in set(canned_analysis_dataframe_subset['tool_id']):

	    	# Add Key
	    	canned_analyses_dict[datasetAccession][toolId] = {}

	    	# Loop Through Canned Analyses
	    	for cannedAnalysisId, cannedAnalysisUrl in canned_analysis_dataframe_subset.loc[canned_analysis_dataframe_subset['tool_id'] == toolId, ['canned_analysis_id', 'canned_analysis_url']].as_matrix():
	        
	        	# Add metadata and description
		        try:
			        canned_analyses_dict[datasetAccession][toolId][cannedAnalysisId] = canned_analysis_metadata_dict[cannedAnalysisId]
			        canned_analyses_dict[datasetAccession][toolId][cannedAnalysisId]['description'] = canned_analysis_metadata_dict[cannedAnalysisId]['description']#createCannedAnalysisDescription(canned_analysis_metadata_dict[cannedAnalysisId], tool_metadata_dict[toolId]['tool_name'])
		        except KeyError:
			        canned_analyses_dict[datasetAccession][toolId][cannedAnalysisId] = {'description': 'No description available.'}

			    # Add URL
		        canned_analyses_dict[datasetAccession][toolId][cannedAnalysisId]['canned_analysis_url'] = cannedAnalysisUrl

	# Return Result
	return {'canned_analyses': canned_analyses_dict, 'tools': tool_metadata_dict}

#######################################################
########## 3.2 Wrapper ################################
#######################################################

##############################
##### 3.2.1 Main function 
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
