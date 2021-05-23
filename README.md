# EGM722-Assignment
Population Mapping - This tool allows the user to create summary statistics and map county population figures across a country for a given year and illustrate population change across a given time period.

------------------------------------------------------------------------------------------------------------------
# Overview
My first repository on GitHub as part of Programming for GIS and Remote Sensing course (EGM722) at Ulster University.

------------------------------------------------------------------------------------------------------------------
# Getting started - Installation and conda environment 

To install and run the script it is recommended to use git (https://git-scm.com/) and the scientific Python distribution package Anaconda (https://docs.anaconda.com/). Please install and setup accounts for these before proceeding. 

# Download and clone the repository
To download the repository head to the repository (https://github.com/mortimere-uu/EGM722_Assignment) and click **fork**, this will create a fork of the repository and clone/copy to your account. Save the repository to a local folder on your computer and make a note of the file pathway.

Launch Anaconda and navigate to the local folder where you cloned the repository. 

Create a new environment by importing the **environment.yml** from the repository. This provides details on the **channels** to install packages from, listed in order of preference, and the **dependencies**.

In Anaconda switch to the correct environment.

# Running the script
Open the EGM722_assignment_script.py in your Integrated Development Environment (IDE).

Ensure that the data file pathway in the script is modified to your locally saved repository (\GitHub\EGM722_Assignment\data_files). These can be changed in the **DATASETS** section (lines 214 - 230) in the script.

In the **Analysis** section the user can input variables the year(s), counties/unitary authorities and country (script lines 231 - 244), along with some of the data parameters. Unfortunatley the script currently has to be modified before running, the variables are currently filled with values that generated the outputs saved to the repository. The variables that can be modified for the test data:

select_year = select year of interest/start year for population difference

select_county_UA = select county/unitary authority

select_country = select country

select_year1 = select end year for calculating population difference

To run the script some parameters from the test data had to be extracted. The below extracts the necessary parameters (years, columns of data). While running the test data it is not recommended to alter these. If using your own data, please identify the most appropriate column and replace. 

data_year_start = start year of data range

data_year_end = end year of data range

counties_UA_id = title of data column with county/UA identifier

counties_UA_name = title of data column with county/UA name

country_id = title of data column with country identifier

Execute the script and output figures and tabulated data will be generated and saved to the output folder. Folder pathways for outputs will also need to be changed in the script, please see **FUNCTIONS** and **FIGURES** and modify the pathway accordingly. 

# References
Training data available from:

NOMIS office labour market statistics. 2021. https://www.nomisweb.co.uk/query/construct/summary.asp?reset=yes&mode=construct&dataset=2002&version=0&anal=1&initsel=

Office for National Statistics. 2021. https://geoportal.statistics.gov.uk/
