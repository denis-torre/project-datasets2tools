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
##### 2.1 Database
##############################

DROP TABLE IF EXISTS `db`;
CREATE TABLE `db` (
	# Fields
	`id` INT AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(20) NOT NULL
);

##############################
##### 2.2 Dataset
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
##### 2.3 Tool
##############################

DROP TABLE IF EXISTS `tool`;
CREATE TABLE `tool` (
	# Fields
	`id` INT AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(20) NOT NULL,
	`icon_url` VARCHAR(100) NOT NULL,
	`tool_url` VARCHAR(100) NOT NULL,
	`description` TEXT
);

##############################
##### 2.4 Attribute
##############################

DROP TABLE IF EXISTS `attribute`;
CREATE TABLE `attribute` (
	# Fields
	`id` INT AUTO_INCREMENT PRIMARY KEY,
    `tool_fk` INT NOT NULL,
	`name` VARCHAR(20) NOT NULL,
	`description` TEXT,
    
    # Foreign keys
	FOREIGN KEY (tool_fk)
		REFERENCES tool(id)
		ON DELETE RESTRICT
);

##############################
##### 2.5 Attribute value
##############################

DROP TABLE IF EXISTS `attribute_value`;
CREATE TABLE `attribute_value` (
	# Fields
	`id` INT AUTO_INCREMENT PRIMARY KEY,
    `attribute_fk` INT NOT NULL,
	`value` VARCHAR(50) NOT NULL,
    
    # Foreign keys
	FOREIGN KEY (attribute_fk)
		REFERENCES attribute(id)
		ON DELETE RESTRICT
);

##############################
##### 2.6 Analysis
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
##### 2.7 Analysis result
##############################

DROP TABLE IF EXISTS `analysis_result`;
CREATE TABLE `analysis_result` (
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
