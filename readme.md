# Analysis of wear parts inventory of Auto Küblbeck


## Projects Title 
Analysis of wear parts inventory of Auto Küblbeck
<br></br>

## Table of Contents
* [Introduction](#introduction)
* [Deliverables](#deliverberals)
* [Project Methodology](#project-methodology)
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
In a second step, these data analyses are to be made available to the Küblbeck company in a web app which can continue to be used and expanded internally even after the project has been completed.
<br></br>


## Stakolder Requirements

- “Availability is key": Have articles at the right time & right spot.

- Combine sales and inventory data sets plus supplier overview.

- Analyse and categorize the inventory according to stakeholders needs.

- Identify and exclude “dead inventory”.

- Identify articles which should be shipped to another subsidiary (~3,100).

- Provide an easy-to-use tool, which the stakeholder may easily distribute to his team.

<br></br>

## Deliverables

1. Overview of amount and value of all or selected articles in in warehouses overall and/or at specific subsidiaries.


2. Analysis and visualisation of which on-stock articles did not move/were not sold overall and for specific subsidiaries, incl. categorizing and evaluating. 


3. Output of a table with recommendations for redistributions (From, To, Article, Quantity).

4. Web application running the redistribution analysis script to keep track of further warehouse management quality.



## Project Methodology

<ol>1. Initial definition of stakeholder requirements</ol>
<ol>2. Data collection (in txt, csv and Excel formats) via the stakeholder's ftp server
<ul>- Reading the raw data into Python</ul>
<ul>- Data adaptation for export to the SQL server (adaptation of data type)</ul>
<ul>- Export data to capstone schema of PostgreSQL server</ul>
<ul>- Reading the SQL data into Python</ul></ol>
<ol>3. Gain data understanding and clarify meaning of columns
<ul>- Stakeholder Meeting</ul>
<ul>- Define MVP</ul>
<ul>- Identification of Project Deliverables, KPIs and Milestones</ul></ol>
<ol>4. Data cleaning and data manipulation
<ul>- Creation of dataframes from the SQL data</ul>
<ul>- Customize column names</ul>
<ul>- Merging of dataframes in df_master</ul></ol>
<ol>5. Analyze data and create visualizations
<ul>- Analysis of the df_master according to stakeholder specifications (storage quality)</ul>
<ul>- Representation of inventory in the dimensions stock and sales</ul>
<ul>- Analysis of the df_master according to stakeholder specifications (redistribution orders)</ul>
<ul>- Model development and implementation of redistribution logic</ul>
<ul>- Output redistribution orders</ul></ol>
<ol>6. Tool creation
<ul>- Evaluate initial customer requirements (QlikView or alternative)</ul>
<ul>- Identify and evaluate alternatives (output in website or application based on Python)</ul>
<ul>- Web application development for final customer use</ul>
<ul>- Link web application with redistribution logic</ul></ol>
<ol>7. Project completion
<ul>- Validation and Documentation</ul>
<ul>- Create Capstone Presentation</ul>
<ul>- Handover to stakeholders</ul></ol>

## Technologies
This project is created with:

- Administration/Project Management:
    - Asana 6.7.23
    - Git 2.39.2
    - Github 3.8.5
<br></br>
- Analytics and algorithm coding:
    - Numpy 1.23.5
    - Pandas 1.5.0
    - Python 3.10.0
    - Seaborn 0.12.2
<br></br>

- Application/Web Development:
    - Flask 2.3.2
    - Jinja2 3.1.2
    - pyinstaller 5.13.0
    - pywebview 4.2.2
    - Werkzeug 2.3.6
<br></br>
- Other tools:
    - Google Slides
    - PostgreSQL 15.2
    - XlsxWriter 3.1.2
<br></br>
## Credits

| Name | GitHub | LinkedIn | Talent App |
|------|--------|----------|------------| 
|Gina Wolter | https://github.com/Ginawolter | https://www.linkedin.com/in/gina-wolter-8b3479205/ | 
|Hans Reimer | https://github.com/hansreimer1980 | https://www.linkedin.com/in/hansreimer/ | https://talents.neuefische.de/profile/163d8663-b7fe-4b88-be73-075ed6669b93
|Marco Drecktrah | https://github.com/mdrecktrah | https://www.linkedin.com/in/marco-drecktrah/ | https://talents.neuefische.de/profile/e72e6a8d-9889-4916-a018-8f13fb7686eb
|Maximilian Eller | https://github.com/MaxiEller | https://www.linkedin.com/in/maximilian-eller-b1b07b87 | https://talents.neuefische.de/profile/8dc3190e-a271-4718-bd1a-21ef7b785fbc
<br></br>
