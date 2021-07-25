# Udacity Data Engineering Nanodegree - Project 6: Capstone Data Pipelines

## Description

Horus is a brazilian startup that creates final user shopping behaviour reports related to the retail market. The company gathers its data using their price comparisson app, Pinngo.

This app helps consumers to find the cheapest prices in the supermarkets around them, seeing updated information in almost every category and segment. To achieve that Pinngo relies in the user collaboration,
as the end user scans the QR code present in supermarket bill receipts in Brazil and upload all the prices to the platform, helping other users to see more updated information.

With millions of products data everyday, Horus is able to understand the retail market in Brazil almost in real time, helping companies to address strategic decisions, in various department such as marketing, operations, sales and how to increase their market share.

## Data sources and staging

The data used in this project is a subset of the original Pinngo app data.  We will use a 7 days window of product sales from users across Brazil, the database of products from Horus,
a dataset from Nielsen with market categories, and a dataset of supermarket companies information (this one in JSON format).

The four datasets are stored in S3 and are going to be copied from there to Redshift to be used as staging tables.

The question the company needs to answer is how many unique product sales where made in one day, by city, and state. 

The stage tables in Redshit have the following structure:
![Final tables diagram](staging_tables.png.png)
_*Datbase schema close up to stage tables.*_

## Database design

The database designed implements a star schema, with 1 fact table and 3 dimensions. Our fact table `product_sales` is the total sales of a product by city, meanwhile the dimensions are:
* `categories` - Contains product category information such as meat, fruits, sweets, beverage....
* `time` - Contains dates only without the timestamp information
* `city` - Contains cities information such as city code, state, and country
 
![Final tables diagram](star_schema.png)
_*Datbase schema close up to final tables.*_

## Airflow DAG

The dag implemented creates all the necessary tables at the first stage, moving to stage of staging data from S3 to redshift. 

A custom operator was created with the possibility to template the `s3_key` attribute, as the files containing all the products invoice of a day are organized by the date of export.

After finishing the staging, it will start to load the dimensions and fact tables into redshift. The `city` and `categories` dimensions depends on their similar table at staging level.

The fact table depends on other 3 tables to be loaded, they are the `product` stage table, `company report` and the invoice receipts table.

After loading each of the facts and dimensions, a data quality is perfomed in fact table `product_sales`, in order to confirm that all the products have their unique ID.

Below we have the dag structure:

![DAG](dag_structure.png)
_*Datbase schema close up to final tables.*_



## Files Structure

* `udac_dag.py` - DAG setup
* `create_tables.sql` - contains the SQL queries used to create the required tables in Redshift
* `sql_queries.py` - contains the SQL queries used in the ETL process. It should be placed in the `plugins/helpers` directory of your Airflow installation.

For this project, personalized operators were created and they need to be placed in the `plugins/operators` directory of your Airflow installation:
* `stage_redshift.py` - `StageToRedshiftOperator` Copy JSON data from S3 to staging tables in the Redshift.
* `load_dimension.py` - `LoadDimensionOperator` Setup a dimension table from staging table data.
* `load_fact.py` -  `LoadFactOperator` Setup a fact table from staging table data.
* `data_quality.py` - `DataQualityOperator` Run data quality checks passing a list of SQL queries and expected results, it will fail if the results don't match.

## Configuration

* Make sure to add the following Airflow connections:
    * `aws_credentials` - Configure this Amazon Web Services connector with your access key and secret.
    * `redshift` - Connection to the redshift cluster using the Postgres connector.