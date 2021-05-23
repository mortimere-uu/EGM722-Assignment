# This script displays UK Counties/Unitary Authorities coded by UK population data for a selected year.
# Summary statistics are generated.

import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import pandas as pd

# FUNCTIONS-------------------------------------------------------------------------------------------------------------

def generate_handles(labels, colors, edge='k', alpha=1):
    """Generates matplotlib handles to create a legend of mapped features.

    :param labels: (str) colour names
    :param colors: (str) colour codes
    :param edge: (str) outline colour on individual items in legend, set to black
    :param alpha: (int) image transparency, set to 1

    :return: output: Legend items for figures,example legend entry for outlines for geographic zones.
    """
    lc = len(colors)  # generates the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


def scale_bar(ax, location=(0.92, 0.95)):
    """ Adds a scale bar to the upper right corner of the map.

    :param ax: (str) define axes to determine the scale bar
    :param location: (int) centre location of scale bar

    :return: output: Scale-bar in the upper right corner of the map figure.
    """
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    ax.plot([sbx, sbx - 50000], [sby, sby], color='k', linewidth=5, transform=tmc)
#   plt.plot([sbx, sbx - 25000], [sby, sby], color='k', linewidth=5, transform=tmc)
#   plt.plot([sbx-25000, sbx - 50000], [sby, sby], color='w', linewidth=5, transform=tmc)

    ax.text(sbx-40000, sby- -10000, '50km', transform=tmc, fontsize=6)
#   plt.text(sbx-12500, sby-4500, '10 km', transform=tmc, fontsize=8)
#   plt.text(sbx-24500, sby-4500, '0 km', transform=tmc, fontsize=8)


def years_check(select_year, select_year1, data_year_start, data_year_end):
    """ Check selected years are correct, select_year1>select_year for population difference calculation

    :param select_year:  (str) input year within dataset to start calculation
    :param select_year1: (str) input year within dataset to end calculation
    :param data_year_start: (int) enter first year of the dataframe
    :param data_year_end: (int) enter last year of the dataframe

    :return: Compares select_year to select_year1 and returns a statement if years selected are suitable to continue.
    """
    select_year = int(select_year)
    if select_year < data_year_start:
        print('{} is outside the data range for years. Please provide a new year.'.format(select_year))
    elif select_year1 > data_year_end:
        print('{} is outside the data range for years. Please provide a new year.'.format(select_year1))
    elif select_year > select_year1:
        print ('{} is incorrect, please provide start year before ({}).'.format(select_year, select_year1))
    elif select_year < select_year1:
        print ('The selected dates are suitable to continue.')
    elif select_year == select_year1:
        print('The selected years are the same, no difference will be displayed in the figure')


def year_population(select_year, counties_UA_id, counties_UA_name):
    """ Generates summary population statistics for a given year between 1991 and 2019.

    For a given year calculates the minimum and maximum county population, the mean population
    across all the counties and the total population for the UK in the given year. Results
    summarised in text statements.

    :param select_year: (str) input year within dataset to map
    :param counties_UA_id: (str) column containing counties/unitary authority unique ID
    :param counties_UA_name: (str) column containing counties/unitary authority name

    :return: Returns summary statistics (mean, min, ax and total) population statistcs for given year and creates a
             .csv file of the results. An example, using 2002 as select_year, generates:

             The mean county/unitary authorities population in the year 2002 was 274,841.10.
             The largest county/unitary authorities population in the year 2002 was 1,338,968.
             The smallest county/unitary authorities population in the year 2002 was 2,170.
             The UK population/unitary authorities in the year 2002 was 59,365,677.
    """
    select_year = str(select_year)
    mean_pop = (counties_UA_population[select_year].mean())
    print('The mean county/unitary authorities population in the year ' + str(select_year) + ' was {:,.2f}.'.format(mean_pop))
    max_pop = (counties_UA_population[select_year].max())
    print('The largest county/unitary authorities population in the year ' + str(select_year) + ' was {:,}.'.format(max_pop))
    min_pop = (counties_UA_population[select_year].min())
    print('The smallest county/unitary authorities population in the year ' + str(select_year) + ' was {:,}.'.format(min_pop))
    total_pop = (counties_UA_population[select_year].sum())
    print('The UK population/unitary authorities in the year ' + str(select_year) + ' was {:,}.'.format(total_pop))
    counties_UA_pop_order = counties_UA_population[[counties_UA_name, counties_UA_id, (select_year)]]
        # selects the county/UA name and ID column and population data for selected year
    print(counties_UA_pop_order.sort_values([select_year], ascending=[False])) # rearranges given year data into
        # descending order (highest to lowest populated counties/UA.
    counties_UA_pop_order.sort_values([select_year], ascending=[False]).to_csv\
        (fr'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\outputs\{counties_UA_id}_{select_year}.csv')


def counties_UA_population_data(select_county_UA, counties_UA_name):
    """ Selects population data for a given county.

    Fetches the population row data for a given county/UA from the merged counties_UA_population table
    and creates a .csv file of the data

    :param select_county_UA: (str) input county/unitary authority name.
    :param counties_UA_name: (str) column containing counties/unitary authority name

    :return: A table, and .csv file, of the population data for every year for the selected county/UA.
    """
    counties_UA_population_data = (counties_UA_population[counties_UA_population[counties_UA_name]
                                         == (select_county_UA)]) # selects the user selected county/UA from the merged counties/UA and population dataframe.
    counties_UA_population_data.to_csv(fr'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\outputs\counties_UA_name_{select_county_UA}.csv')
    print(counties_UA_population_data)


def country_data (data_year_start, data_year_end, counties_UA_id):
    """ Formats the population dataframe and merges with counties/UA geodataframe.

    :param data_year_start: (int) enter first year of the dataframe
    :param data_year_end: (int) enter last year of the dataframe
    :param counties_UA_id: (str) column containing counties/unitary authority unique ID

    :return: Returns a merged geodataframe of counties/unitary authority with the population dataframe.
    """
    years = [str(yr) for yr in range(data_year_start, data_year_end)]  # create a variable called years to compliment the provided dataset
    population_df[years] = population_df[years].apply(pd.to_numeric, args=(
    'coerce',))  # removes any non-number/nodata, no population data collected for Ireland 1991-2000
    country_population = (pd.merge(countries_counties_UA, population_df, on=(counties_UA_id),
                                   how='left'))  # merge population data with counties_UA using the CTYUA20CD coloumn
    #print(country_population)  # some issues with no data rows - is thei due to centre point being outside countryshape - groups of islands?
    country_population.to_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\outputs\country_population_all.csv')


def country_year_population(select_country, select_year, country_id):
    """ Generates a table and .csv file for selected countries yearly population for the dataset

    Fetches the population data for a given county from the merged country_population table
    and creates a .csv file of the country data including individual counties/UA and geometry data.

    :param select_country: (str) input country name
    :param select_year: (str) input year within dataset to map
    :param country_id: (str) column containing countries unique ID

    :return: Creates a summary statement for the countries population for seleted year and a .csv file of the countries
             population data for all year. An example of the staement generated:

             Total population of England in 2006 was 50,709,444.
    """
    select_country = select_country.title()
    select_year = str(select_year)
    country = (country_population[country_population[country_id] == (select_country)])
    country_year = country_population[country_population[country_id] == (select_country)][(select_year)].sum()
    print('Total population of ' + str(select_country) + ' in ' + str(select_year) + ' was {:,}.'.format(country_year))
    country.to_csv(
        fr'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\outputs\country_{select_country}_population.csv')


def country_all_year (select_year, country_id):
    """ Prints a list of UK countries population for selected year, in descending order.

    :param select_year: (str) input year within dataset to analyse.
    :param country_id: (str) column containing countries unique ID

    :return: Returns a list of countries total population in descending order for selected yea. An example of the
             output:

            The below table list counties in descending population order for the year 2006.
            CTRY20NM
            England             50709444
            Scotland             4975870
            Wales                2985668
            Northern Ireland     1743113
    """
    select_year = str(select_year)
    sum_country_total = country_population.groupby(country_population[country_id])[select_year].sum()
    print('The table below list the countries in order of descending population for the year ' + (select_year) + '.')
    print(sum_country_total.sort_values(ascending=[False]))


def counties_UA_population_change(select_year, select_year1):
    """ Calculates the population difference between selected years.

    :param select_year: (str) input year within dataset to analyse.
    :param select_year1: (str) input later year within dataset to perform calculation.

    :return: Creates a column ot population difference (positive or negative int) which is used in figure to represent
             population change over selected timeframe. Table is presented in descending population difference.
    """
    select_year = str(select_year)
    select_year1 = str(select_year1)
    counties_UA_population['Population change'] = counties_UA_population[select_year1] - \
                                                  counties_UA_population[select_year]
    print(counties_UA_population.sort_values(['Population change'], ascending=[False]))


# DATASETS-------------------------------------------------------------------------------------------------------------

# Load the training datasets from the git repository. User needs to modify the filepath location to match users location
countries = gpd.read_file(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Countries_(December_2020)_UK_BUC.shp')
        # 2020 UK country shapefile - training data
counties_UA = gpd.read_file (r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Counties_and_Unitary_Authorities.shp')
        # 2020 UK Counties and Unitary Authorities shapefile - training data
population_df = pd.read_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\population_number.csv')
        # UK population data from 1991 to 2019 - training data

# lines of code below check crs match for the Countries and Counties/UA vector files, or users own files.
# print(countries.crs)  # check the vector shapefile epsg code
# print(countries.crs == counties_UA.crs) # check the CRS match for the Countries and Counties/UA vector files.

# epsg code for test data is 27700, if using own data and does not match epsg/crs code modifications to the script
# are required.

# ANALYSIS--------------------------------------------------------------------------------------------------------------

# Please input the variables you want to study:
select_year = '2002' # select year of interest/start year for population difference
select_county_UA = 'Conwy' # select county/unitary authority
select_country = 'England' #select country
select_year1 = 2019 # select end year for population difference

#data parameters:
data_year_start = 1991 # start year of data
data_year_end = 2019 # end year of data
counties_UA_id = 'CTYUA20CD' # title of data column with county/UA identifier
counties_UA_name = 'County / unitary (as of April 2021)' # title of data column with county/UA name
country_id = 'CTRY20NM' # title of data column with country identifier

# check years selected suitable to population difference calculation
years_check(select_year, select_year1, data_year_start, data_year_end)

# print(population_df[counties_UA_name])#prints list of counties/UA to input as select_county_UA
# print(countries[country_id]) # prints a list of countries to input as select_country

# Country statistics for a given year

#join countries and counties_UA
counties_UA_centrepoint = counties_UA.copy()
counties_UA_centrepoint['geometry'] = counties_UA_centrepoint['geometry'].centroid # calculate the centrepoint
        # for counties/UA polygons

#join countries and counties_UA
countries_counties_UA = gpd.sjoin(countries, counties_UA_centrepoint, how='right', lsuffix='left', rsuffix='right')
years = [str(yr) for yr in range(data_year_start, data_year_end)] # create a variable called years to compliment the provided dataset
population_df[years] = population_df[years].apply(pd.to_numeric, args=('coerce',)) # removes non-number/nodata, no population data collected for Ireland 1991-2000
country_population = (pd.merge(countries_counties_UA, population_df, on=counties_UA_id, how='left')) # merge population data with counties_UA using the CTYUA20CD coloumn

# Country Summary Statistics Analysis

# Generates table for individual counties/UN in each country and population data from 1991 to 2019
country_data(data_year_start, data_year_end, counties_UA_id)

# Generates table of selected country and year including counties/UA
country_year_population(select_country, select_year, country_id) # prints statement of countries population for given year and generate table

# Generates a table for all countries populations for given year.
country_all_year(select_year, country_id)

# Counties and Unitary Authorities Summary Statistics

# merge the population_df with counties_UA shapefile to add geometry data to df to create year maps
years = [str(yr) for yr in range(data_year_start, data_year_end)]
population_df[years] = population_df[years].apply(pd.to_numeric, args=('coerce',)) # removes any non-number/nodata population for Ireland 1991-2000
counties_UA_population = (pd.merge(counties_UA, population_df, on=counties_UA_id, how='left')) # merge population data with counties_UA
del counties_UA_population['CTYUA20NMW'], counties_UA_population['BNG_E'], \
    counties_UA_population['BNG_N'], counties_UA_population['LONG'], \
    counties_UA_population['LAT'] # remove unwanted columns
#print(counties_UA_population.columns) # check removal of columns and header check of merged table
#print(counties_UA_population)
counties_UA_population.to_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\outputs\counties_UA_population.csv') # file note accurate, multiple islands grouped as one geometry are causing an issue with the output table.

# Generate yearly population figures coded by counties/UA
year_population(select_year, counties_UA_id, counties_UA_name) # print selected years population stats from the year_population function above.

# Generate yearly population data for a selected County/Unitary Authorities
counties_UA_population_data(select_county_UA, counties_UA_name)

# Calculate population change (growth or loss) in counties and unitary authorities in UK for Figure 2
counties_UA_population_change(select_year, select_year1)

# FIGURES---------------------------------------------------------------------------------------------------------------

# Figure for selected year population data for each County/UA
# create a figure of size 10x10 (representing the page size in inches)
fig = plt.figure(figsize=(10, 10))

# create a crs that matches figures epsg 27700, if using other data modify this.
myCRS = ccrs.OSGB()

# create an axes object in the figure, using OSGB projection to plot data
ax = plt.axes(projection=ccrs.OSGB())

# adds a colorbar to the map
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the counties and unitary authority population data for a given year into our axis, using
counties_UA_population_plot = counties_UA_population.plot(column=select_year, ax=ax, vmin=-1800, vmax=1600000, cmap='PuRd',
                       legend=True, cax=cax, legend_kwds={'label' : 'Population, in millions', 'orientation': 'vertical'})

# add counties_UA boundaries shapefile
counties_UA_outline = ShapelyFeature(counties_UA['geometry'], myCRS, edgecolor='k', facecolor='none', linewidth=0.2) # changed facecover
xmin, ymin, xmax, ymax = counties_UA.total_bounds
ax.add_feature(counties_UA_outline)

ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

# add items for legend
county_handles = generate_handles([''], ['none'], edge='k')
ax.legend(county_handles, ['Counties/Unitary Authorities'], fontsize=8, loc='upper left', framealpha=1)

# add gridlines to figure
gridlines = ax.gridlines(draw_labels=True,
                        xlocs=[-8, -6, -4, -2, 0, +2],
                         ylocs=[52, 54, 56, 58, 60])
gridlines.right_labels = False
gridlines.bottom_labels = False

# add year title
title = '' + str(select_year) + ' UK Population'
ax.set_title(title, fontdict={'fontsize': '12', 'fontweight': '5'})

# add scale bar
scale_bar(ax)

# save the figure
fig.savefig(fr'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\outputs\UK population_{select_year}.png', dpi=300, bbox_inches='tight')

# Figure illustrating population loss/growth between 2001 and 2019
fig2, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

ax = plt.axes(projection=ccrs.OSGB())

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -6, -4, -2, 0, +2],
                         ylocs=[52, 54, 56, 58, 60])
gridlines.right_labels = False
gridlines.bottom_labels = False

counties_UA_population_plot = counties_UA_population.plot(column='Population change', ax=ax,
                                vmin=counties_UA_population['Population change'].min(), vmax=counties_UA_population['Population change'].max(),
                                cmap='rainbow',legend=True, cax=cax, legend_kwds={'label' : 'Population change', 'orientation': 'vertical'})

counties_UA_outline = ShapelyFeature(counties_UA['geometry'], myCRS, edgecolor='k', facecolor='none', linewidth=0.2) # changed facecover
ax.add_feature(counties_UA_outline)

ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

county_handles = generate_handles([''], ['none'], edge='k')

ax.legend(county_handles, ['Counties/Unitary Authorities'], fontsize=8, loc='upper left', framealpha=1)

title = 'Population change from ' + str(select_year) + ' to ' + str(select_year1)
ax.set_title(title, fontdict={'fontsize': '12', 'fontweight': '5'})

scale_bar(ax)

fig2.savefig(fr'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\outputs\Population change_{select_year}_{select_year1}.png', dpi=300, bbox_inches='tight')

# A pie-chart plot of Country statistics
select_year = (select_year)
sum_country_total = country_population.groupby(country_population[country_id])[select_year].sum()

fig_pie = plt.figure(figsize=(20,20))
ax1 = plt.subplot(121, aspect='equal')
sum_country_total.plot(kind='pie', y = select_year, ax=ax1, autopct='%1.1f%%', startangle=90,
                       shadow=False, labels=('England', 'Northern Ireland', 'Scotland', 'Wales'), legend=True, fontsize=10)
fig_pie.savefig(fr'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\outputs\country_population_{select_year}.png', dpi=300, bbox_inches='tight')