# Logs Analysis
This program is part of the Udacity Fullstack Nanodegree curriculum.  The program is designed using python and psycopg to query a PostgreSQL database to support a fictional newspaper company.

## Database and Setup
The database is composed of three tables - logs, articles, and authors.

The database can be seeded by running `psql -d news -f newsdata.sql` in the terminal

NOTE: the database used for this repo is not deployed here based on file size

## Design
For the log table, the file path is assumed to contain the article slug, by parsing the path and removing slashes and higher level folders

datetime in imported to assist in working with timestamp fields

## Output
Three queries are executed with results printed to the console:
* Popular articles - the three most popular articles, by page views via the log, are returned
* Popular authors - all authors are returned sorted by total views
* Error frequency - days are returned in which the percent of errors logged was greater than 1%

## Running
`python logs_analysis_project.py`
