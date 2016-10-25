############################################################
############################################################
############### Datasets2Tools Schema Definition ###########
############################################################
############################################################

#######################################################
########## 1. Create Database #########################
#######################################################

##############################
##### 1.1 Create Database
##############################

### Create database
CREATE DATABASE IF NOT EXISTS `datasets2tools`;

### Use database
USE `datasets2tools`;

### Disable foreign key checks
SET FOREIGN_KEY_CHECKS=0;

#######################################################
########## 2. Create Tables ###########################
#######################################################

##############################
##### 1.1 Database
##############################

DROP TABLE IF EXISTS `db`;
CREATE TABLE `db` (
	# Fields
	`id` INT AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(20) NOT NULL
);

##############################
##### 1.2 Dataset
##############################

DROP TABLE IF EXISTS `dataset`;
CREATE TABLE `dataset` (
	# Fields
	`id` INT AUTO_INCREMENT PRIMARY KEY,
	`database_fk` INT NOT NULL,
	`accession` VARCHAR(20) NOT NULL,

	# Foreign keys
	FOREIGN KEY (database_fk)
		REFERENCES db(id)
		ON DELETE RESTRICT
);

##############################
##### 1.3 Tool
##############################

DROP TABLE IF EXISTS `tool`;
CREATE TABLE `tool` (
	# Fields
	`id` INT AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(20) NOT NULL,
	`icon_url` VARCHAR(100) NOT NULL,
	`tool_url` VARCHAR(100) NOT NULL
);

##############################
##### 1.4 Attribute
##############################

DROP TABLE IF EXISTS `attribute`;
CREATE TABLE `attribute` (
	# Fields
	`id` INT AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(20) NOT NULL,
	`description` VARCHAR(100)
);

##############################
##### 1.5 Analysis
##############################

DROP TABLE IF EXISTS `analysis`;
CREATE TABLE `analysis` (
	# Fields
	`id` INT AUTO_INCREMENT PRIMARY KEY,
	`dataset_fk` INT NOT NULL,
	`tool_fk` INT NOT NULL,

	# Foreign keys
	FOREIGN KEY (dataset_fk)
		REFERENCES dataset(id)
		ON DELETE RESTRICT,

	FOREIGN KEY (tool_fk)
		REFERENCES tool(id)
		ON DELETE RESTRICT
);

##############################
##### 1.6 Analysis result
##############################

DROP TABLE IF EXISTS `analysis_results`;
CREATE TABLE `analysis_results` (
	# Fields
	`id` INT AUTO_INCREMENT PRIMARY KEY,
	`analysis_fk` INT NOT NULL,
	`attribute_fk` INT NOT NULL,
	`value` VARCHAR(20) NOT NULL,

	# Foreign keys
	FOREIGN KEY (analysis_fk)
		REFERENCES analysis(id)
		ON DELETE RESTRICT,

	FOREIGN KEY (attribute_fk)
		REFERENCES attribute(id)
		ON DELETE RESTRICT
);

#######################################################
########## 3. Other ###################################
#######################################################

### Reset foreign key checks
SET FOREIGN_KEY_CHECKS=1;
