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

    Parameters:
        labels:
        colors:
        edge:
        alpha:

    Returns:
        Description
    """
    lc = len(colors)  # generates the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

def scale_bar(ax, location=(0.92, 0.95)):

    """ Adds a scale bar to the upper right corner of the map.

    Parameters:
        ax:
        location:

    Returns:
        Description
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

def year_population(select_year): # add in correct year if outside window.....maybe need somewhere to input years,
    # etc of interest

    """ Generates summary population statistics for a given year between 1991 and 2019.

    For a given year calculates the minimum and maximum county population, the mean population
    across all the counties and the total population for the UK in the given year. Results
    summarised in text statements.

    Parameters:
    :param select_year:

    Returns:
        Description
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
    counties_UA_pop_order = counties_UA_population[['County / unitary (as of April 2021)', 'CTYUA20CD', (select_year)]]
        # selects the county/UA name and ID column and population data for selected year
    print(counties_UA_pop_order.sort_values([select_year], ascending=[False])) # rearranges given year data into
        # descending order (highest to lowest populated counties/UA.
    counties_UA_pop_order.sort_values([select_year], ascending=[False]).to_csv\
        (fr'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\Counties_UA_{select_year}.csv')


def counties_UA_population_data(select_county_UA):

    """ Selects population data for a given county.

    Fetches the population row data for a given county from the merged counties_UA_population table
    and creates a .csv file of the data

    :param select_county_UA:

    :return:

        """

    counties_UA_population_data = (counties_UA_population[counties_UA_population['County / unitary (as of April 2021)']
                                                          == (select_county_UA)])
    counties_UA_population_data.to_csv(fr'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\Counties_UA_{select_county_UA}.csv')
            # user needs to change file location for generated outputs - can I make something to input this somewhere?
    print(counties_UA_population_data)

def country_year_population(select_country, select_year):

    """ Generates countries yearly population and table with countries population data, all years

    :param select_country
    :param select_year

    :return:


    """

    select_country = select_country.title()
    select_year = str(select_year)
    country = (country_population[country_population['CTRY20NM'] == (select_country)])
    country_year = country_population[country_population['CTRY20NM'] == (select_country)][(select_year)].sum()
    print('Total population of ' + str(select_country) + ' in ' + str(select_year) + ' was {:,}'.format(country_year))
    country.to_csv(
        fr'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\country_{select_country}_population.csv')


def country_all_year (select_year):

    """ Prints a list of Uk countries population for selected year, in descending order.

    :param select_year:

    :return:

    """

    select_year = str(select_year)
    sum_country_total = country_population.groupby(country_population['CTRY20NM'])[select_year].sum()
    print('The below table list counties in descending population order for the year ' + (select_year) + '.')
    print(sum_country_total.sort_values(ascending=[False]))


def counties_UA_population_change(select_year, select_year1):

    """ description

    :param select_year:
    :param select_year1:

    :return:

    """
    select_year = str(select_year) # type a rule select year 2 must be more recent than year1 and years betwee 1991-2019
    select_year1 = str(select_year1)
    counties_UA_population['Population change'] = counties_UA_population[select_year1] - \
                                                  counties_UA_population[select_year]
    # print(counties_UA_population) # groupby country?
    print(counties_UA_population.sort_values(['Population change'], ascending=[False]))

def country_data (year_start, year_end, counties_UA_id):

    """


    :param year_start:
    :param year_end:
    :param counties_UA_id:

    :return:
    """
    years = [str(yr) for yr in range(year_start, year_end)]  # create a variable called years to compliment the provided dataset
    population_df[years] = population_df[years].apply(pd.to_numeric, args=(
    'coerce',))  # removes any non-number/nodata, no population data collected for Ireland 1991-2000
    country_population = (pd.merge(countries_counties_UA, population_df, on=(counties_UA_id),
                                   how='left'))  # merge population data with counties_UA using the CTYUA20CD coloumn
    print(country_population)  # some issues with no data rows - is thei due to centre point being outside countryshape - groups of islands?
    country_population.to_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\country_population_all.csv')


# DATASETS-------------------------------------------------------------------------------------------------------------

# Load the training datasets from the git repository. User needs to modify the filepath location to match users location
countries = gpd.read_file(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Countries_(December_2020)_UK_BUC.shp')
        # 2020 UK country shapefile
counties_UA = gpd.read_file (r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Counties_and_Unitary_Authorities.shp')
        # 2020 UK Counties and Unitary Authorities shapefile
population_df = pd.read_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\population_number.csv')
        # UK population data from 1991 to 2019

# lines of code below check crs match for the Countries and Counties/UA vector files, or users own files.
# print(countries.crs)  # check the vector shapefile epsg code
# print(countries.crs == counties_UA.crs) # check the CRS match for the Countries and Counties/UA vector files.

# epsg code for test data is 27700, if using own data and does not match epsg/crs code modifications to the script
# are required.

# ANALYSIS--------------------------------------------------------------------------------------------------------------

# Please input the variables you want to study:
select_year = '2001'
select_county_UA = 'Suffolk'
select_country = 'England'

select_year1 = 2019

#data parameters:
year_start = 1991
year_end = 2019
counties_UA_id = 'CTYUA20CD' # title of data column with country identifier.
country_id = 'CTRY20NM'



def data_check(year_start, year_end):
    if year_end < year_start:
        print ('{} is incorrect, please provide year data after year start ({}).'.format(year_end, year_start))

data_check (year_start, year_end)

# Country statistics for a given year

# countries_counties_UA_poly = gpd.sjoin(countries, counties_UA, how='right', lsuffix='left', rsuffix='right')
    # join countries and counties_UA to code data - tied joining on polygon got repetition in results
# print(countries_counties_UA_poly) # This method did not work, resulted in repetition of data along country boundaries.

# generate the centrepoint for each county_UA polygon
counties_UA_centrepoint = counties_UA.copy()
counties_UA_centrepoint['geometry'] = counties_UA_centrepoint['geometry'].centroid # calculate centrepoint for counties

#join countries and counties_UA
countries_counties_UA = gpd.sjoin(countries, counties_UA_centrepoint, how='right', lsuffix='left', rsuffix='right')
# print(countries_counties_UA) # check table join - issues with multipolygon islands centrepoint outside country polygon.

years = [str(yr) for yr in range(year_start, year_end)] # create a variable called years to compliment the provided dataset
population_df[years] = population_df[years].apply(pd.to_numeric, args=('coerce',)) # removes any non-number/nodata, no population data collected for Ireland 1991-2000
country_population = (pd.merge(countries_counties_UA, population_df, on=counties_UA_id, how='left')) # merge population data with counties_UA using the CTYUA20CD coloumn
print(country_population) # some issues with no data rows - is thei due to centre point being outside countryshape - groups of islands?

# Country Summary Statistics Analysis

# Generates table for individual counties/UN in each country and population data from 1991 to 2019
country_data(year_start, year_end, counties_UA_id)

# For selected country and year calculates total population
print(countries[country_id]) # a list of countries

country_year_population(select_country, select_year) # prints statement of countries population for given year and generate table

# Generates a table for all countries populations for given year.
country_all_year(select_year)

# Counties and Unitary Authorities Summary Statistics

# merge the population_df with counties_UA shapefile to add geometry data to df to create year maps
years = [str(yr) for yr in range(year_start, year_end)] # creat a variable called years to compliment the provided dataset
population_df[years] = population_df[years].apply(pd.to_numeric, args=('coerce',)) # removes any non-number/nodata, no population data collected for Ireland 1991-2000
counties_UA_population = (pd.merge(counties_UA, population_df, on=counties_UA_id, how='left')) # merge population data with counties_UA using the CTYUA20CD coloumn
del counties_UA_population['CTYUA20NMW'], counties_UA_population['BNG_E'], \
    counties_UA_population['BNG_N'], counties_UA_population['LONG'], \
    counties_UA_population['LAT'] # remove unwanted columns
print(counties_UA_population.columns) # check removal of columns and header check of merged table
print(counties_UA_population)
counties_UA_population.to_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\counties_UA_population.csv') # file note accurate, multiple islands grouped as one geometry are causing an issue with the output table.

# Use the def year_population function to pull the yearly population
#print('Please enter a year between 1991 and 2019?') #can i write a way for someone to inptu the year

year_population(select_year) # print selected years population stats from the year_population function above.

# Generate yearly population data for a selected County/Unitary Authorities

#print('Please enter a County and/or Unitary Authorities from the list provided.') #can i write a way for someone to input the country and provide a list to selct from
print(counties_UA_population['County / unitary (as of April 2021)']) # prints list of all counites/UA authorities

#generates population statistics for selected county/UA
counties_UA_population_data(select_county_UA)

# Calculate population change (growth or loss) in counties and unitary authorities in UK

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
fig.savefig(f'UK population_{select_year}.png', dpi=300, bbox_inches='tight')

# Figure illustrating population loss/growth between 2001 and 2019

# create a figure of size 10x10 (representing the page size in inches
fig2, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

ax = plt.axes(projection=ccrs.OSGB())

# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -6, -4, -2, 0, +2],
                         ylocs=[52, 54, 56, 58, 60])
gridlines.right_labels = False
gridlines.bottom_labels = False

# plot the counties and unitary authorities population data for a given year into our axis, using
counties_UA_population_plot = counties_UA_population.plot(column='Population change', ax=ax, vmin=counties_UA_population['Population change'].min(), vmax=counties_UA_population['Population change'].max(), cmap='rainbow',
                       legend=True, cax=cax, legend_kwds={'label' : 'Population change', 'orientation': 'vertical'})

counties_UA_outline = ShapelyFeature(counties_UA['geometry'], myCRS, edgecolor='k', facecolor='none', linewidth=0.2) # changed facecover
ax.add_feature(counties_UA_outline)

ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

county_handles = generate_handles([''], ['none'], edge='k')

ax.legend(county_handles, ['Counties/Unitary Authorities'], fontsize=8, loc='upper left', framealpha=1)

# add year title
title = 'Population change from ' + str(select_year) + ' to ' + str(select_year1)
ax.set_title(title, fontdict={'fontsize': '12', 'fontweight': '5'})

scale_bar(ax)

fig2.savefig(f'Population change_{select_year}_{select_year1}.png', dpi=300, bbox_inches='tight')

# plot a line graph of data

# Country statistics plot a pie chart of country population total for 2019 (move down to figures?), modify in way for user inputs

#needed for piechart - can not link to function result
select_year = (select_year)
sum_country_total = country_population.groupby(country_population['CTRY20NM'])[select_year].sum()

fig_pie = plt.figure(figsize=(20,20))
ax1 = plt.subplot(121, aspect='equal')
sum_country_total.plot(kind='pie', y = select_year, ax=ax1, autopct='%1.1f%%', startangle=90,
                       shadow=False, labels=('England', 'Northern Ireland', 'Scotland', 'Wales'), legend=True, fontsize=10)
fig_pie.savefig(f'country_population_{select_year}.png', dpi=300, bbox_inches='tight') # add population numbers?
