# Analysis of wear parts inventory of Auto Küblbeck

## Projects Title 
Analysis of wear parts inventory of Auto Küblbeck
<br></br>

## Table of Contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Credits](#credits)
<br></br>

## Introduction
This project is an analysis of the stock management of spare parts for the spare parts dealer Küblbeck.<br> 
Our target is the examination and optimization for inventory management of the German locations. 
<br></br>
The aim is to exchange already existing parts between the locations according to current sales figures and thus to minimize both the storage capacities and the procurement of new parts. <br> 
Indicators for an exchange are the number of stored products per location, the corresponding sales figures per location as well as a location analysis.
<br></br>
In a second step, these data analyses are to be made available to the Küblbeck company in a dashboard or python script which can continue to be used and expanded internally even after the project has been completed.
<br></br>

## Project Methodology 

<ol>Initial definition of stakeholder requirements</ol>
<ol>Data collection (in txt, csv and Excel formats) via the stakeholder's ftp server
<ul>Reading the raw data into Python</ul>
<ul>Data adaptation for export to the SQL server (adaptation of data type)</ul>
<ul>Export data to capstone schema of PostgreSQL server</ul>
<ul>Reading the SQL data into Python</ul></ol>
<ol>Gain data understanding and clarify meaning of columns
<ul>Stakeholder Meeting</ul>
<ul>Define MVP</ul>
<ul>Identification of Project Deliverables, KPIs and Milestones</ul></ol>
<ol>Data cleaning and data manipulation
<ul>Creation of dataframes from the SQL data</ul>
<ul>Customize column names</ul>
<ul>Merging of dataframes in df_master</ul></ol>
<ol>Analyze data and create visualizations
<ul>Analysis of the df_master according to stakeholder specifications (storage quality)</ul>
<ul>Representation of inventory in the dimensions stock and sales</ul>
<ul>Analysis of the df_master according to stakeholder specifications (redistribution orders)</ul>
<ul>Model development and implementation of redistribution logic</ul>
<ul>Output redistribution orders</ul></ol>
<ol>Tool creation
<ul>Evaluate initial customer requirements (QlikView or alternative)</ul>
<ul>Identify and evaluate alternatives (output in website or application based on Python)</ul>
<ul>Web application development for final customer use</ul>
<ul>Link web application with redistribution logic</ul></ol>
<ol>Project completion
<ul>Validation and Documentation</ul>
<ul>Create Capstone Presentation</ul>
<ul>Handover to stakeholders</ul></ol>

## Technologies
This project is created with:
- Python 3.10.0
- PostgreSQL 15.2
- Asana 6.7.23
- GitHub 3.8.5
- Git 2.39.2
- Google Slides 
<br></br>

## Sources
<br></br>

## Credits

| Name | GitHub | LinkedIn |
|------|--------|----------|
|Gina Wolter | https://github.com/Ginawolter | https://www.linkedin.com/in/gina-wolter-8b3479205/
|Hans Reimer | https://github.com/hansreimer1980 | https://www.linkedin.com/in/hansreimer/
|Marco Drecktrah | https://github.com/mdrecktrah | https://www.linkedin.com/in/marco-drecktrah/
|Maximilian Eller | https://github.com/MaxiEller | https://www.linkedin.com/in/maximilian-eller-b1b07b87
<br></br>
