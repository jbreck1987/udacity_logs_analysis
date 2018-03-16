# Log Analysis Project

### Introduction

This small tool was created to satisfy the Logs Analysis project from the Udacity Full Stack Web Developer Nanodegree. There are three pieces of information that have been requested and the tool uses SQL to get this data from a sample PostgreSQL database.

### Queries
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


### SQL Views
SQL views were utilized in this tool to simplify the code. Below are the SQL queries that were used for this tool:

* What are the most popular three articles of all time?
```
CREATE VIEW view_select_popular_articles AS
SELECT 
    articles.title, 
    count(log.path) AS views
FROM 
    articles 
LEFT JOIN log ON articles.slug = ( SELECT REPLACE(log.path, '/article/', '') )
GROUP BY 
    articles.title
ORDER BY 
    views DESC
LIMIT 3;
```

* Who are the most popular article authors of all time?
```
CREATE VIEW view_select_popular_authors AS
SELECT 
    authors.name, 
    count(log.path) AS views
FROM 
    articles
JOIN log ON articles.slug = (SELECT REPLACE(log.path, '/article/', ''))
JOIN authors ON articles.author = authors.id

GROUP BY
    authors.name
ORDER BY
    views DESC;
```
* On which days did more than 1% of requests lead to errors?
```
CREATE VIEW view_select_error_percent AS
SELECT 
    day,
    ROUND(err_percent, 2) as percent

FROM
    (SELECT 
        error.day,
        error.error_count::decimal/(error.error_count + ok.ok_count)*100.0 AS err_percent

    FROM
        (SELECT 
            status AS error_status,
            to_char(time, 'yyyy-mm-dd') AS day,
            count(*) AS error_count 
         FROM log
         WHERE status = '404 NOT FOUND'
         GROUP BY day, status
        ) AS error
    JOIN
        (SELECT
            status AS ok_status,
            to_char(time, 'yyyy-mm-dd') AS day,
            count(*) AS ok_count
         FROM log
         WHERE status = '200 OK'
         GROUP BY day, status
         ) AS ok 
    ON error.day = ok.day
    ) AS totals
WHERE
    err_percent > 1;
```

### Usage

* This tool requires the PostgreSQL psycopg2 Python library to run.
* The sample SQL database used for the assignement must also be available.
* The SQL views given above must also be created within the sample SQL database for the queries to run successfully.
