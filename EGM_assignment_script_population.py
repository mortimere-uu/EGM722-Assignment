# give a summary of what the script will do (datasets, technqies and outputs)

import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
from shapely.geometry import Point, LineString, Polygon
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import pandas as pd

# ----------------------------------------------------------------------------------------------------------------------
# Functions

# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# add scale bar for maps - not working need to resolve, cehck docstring
# create a scale bar of length 20 km in the upper right corner of the map - needs correcting
def scale_bar(ax, location=(0.92, 0.95)):
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

def year_population(x):

    """ Generates summary population statistics for a given year (x) between 1991 and 2019.

    For a given year calculates the minimum and maximum county population, the mean population
    across all the counties and the total population for the UK in the given year. Results
    summarised in text statements."""

    x = str(x)
    mean_pop = (counties_UA_population[x].mean()) # this is wrong, not running on x running on 2019 hardwired?
    print('The mean county population in the year ' + str(x) + ' was {:,.2f}.'.format(mean_pop))
    max_pop = (counties_UA_population[x].max())
    print('The maximum county population in the year ' + str(x) + ' was {:,}.'.format(max_pop))
    min_pop = (counties_UA_population[x].min())
    print('The minimum county population in the year ' + str(x) + ' was {:,}.'.format(min_pop))
    total_pop = (counties_UA_population[x].sum())
    print('The UK population in the year ' + str(x) + ' was {:,}.'.format(total_pop))



def counties_UA_population_data(y): # for a given County/Unitary Authorities select all the population data fom 1991 to 2019, make docstring

    """ Selects population data for a given county.

    Fetches the population row data for a given county from the merged counties_UA_population table
    and creates a .csv file of the data"""

    counties_UA_population_data = (counties_UA_population[counties_UA_population['County / unitary (as of April 2021)'] == (y)])
    counties_UA_population_data.to_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\Counties_UA_selected.csv') # want to save an output file with county name in it
    print(counties_UA_population_data)

# add template for graphs

# plt.ion()

# ---------------------------------------------------------------------------------------------------------------------

# load datasets to be used in the analysis
countries = gpd.read_file(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Countries_(December_2020)_UK_BUC.shp') # 2020 UK country shapefile
counties_UA = gpd.read_file (r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Counties_and_Unitary_Authorities.shp') # 2020 UK Counties and Unitary Authorities shapefile
population_df = pd.read_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\population_number.csv') # UK population data from 1991 to 2019

# print(countries.crs) # check the countries shapefile epsg code
# print(countries.crs == counties_UA.crs) # check if the crs is the same for countries and counties.
# print(population_df.head()) # check population table header information

# country statistics

# join countries and counties_UA to code data - tied joining on polygon got repetition in results
# countries_counties_UA_poly = gpd.sjoin(countries, counties_UA, how='right', lsuffix='left', rsuffix='right')
# print(countries_counties_UA_poly)

# generate the centrepoint for each county_UA polygon and use this with country polygons
counties_UA_centrepoint = counties_UA.copy()
counties_UA_centrepoint['geometry'] = counties_UA_centrepoint['geometry'].centroid # calculate centrepoint for counties
print(counties_UA_centrepoint)


#join countries and counties_UA to code data - tied joining on polygon but got reetition in results
countries_counties_UA = gpd.sjoin(countries, counties_UA_centrepoint, how='right', lsuffix='left', rsuffix='right')
print(countries_counties_UA)

years = [str(yr) for yr in range(1991, 2020)] # creat a variable called years to compliment the provided dataset
population_df[years] = population_df[years].apply(pd.to_numeric, args=('coerce',)) # removes any non-number/nodata, no population data collected for Ireland 1991-2000
country_population = (pd.merge(countries_counties_UA, population_df, on='CTYUA20CD', how='left')) # merge population data with counties_UA using the CTYUA20CD coloumn
print(country_population) # some issues with no data rows - is thei due to centre point being outside countryshape - groups of islands?

#generate country summary statements - function this
print(country_population[country_population['CTRY20NM'] == 'Scotland'])
sum_country = country_population[country_population['CTRY20NM'] == 'Scotland']['2019'].sum()
print('{:,} total population of Scotland in 2019'.format(sum_country))

sum_country_total = country_population.groupby(country_population['CTRY20NM'])['2019'].sum()
print(sum_country_total)
#print(population_df)
country_population_total = (country_population['2019'].sum())
print(country_population_total)

population_df_total = (population_df['2019'].sum())
print(population_df_total)
print(country_population_total / population_df_total) # sense check

# plot a pie chart of country population total for 2019 (move down to figures?), modify in way for user inputs

fig_pie = plt.figure(figsize=(20,20))
ax1 = plt.subplot(121, aspect='equal')
sum_country_total.plot(kind='pie', y = '2019', ax=ax1, autopct='%1.1f%%', startangle=90,
                       shadow=False, labels=('England', 'Northern Ireland', 'Scotland', 'Wales'), legend=True, fontsize=10)
fig_pie.savefig('piechart2019.png', dpi=300, bbox_inches='tight')


# merge the population_df with counties_UA shapefile to add geometry data to df to create year maps
years = [str(yr) for yr in range(1991, 2020)] # creat a variable called years to compliment the provided dataset
population_df[years] = population_df[years].apply(pd.to_numeric, args=('coerce',)) # removes any non-number/nodata, no population data collected for Ireland 1991-2000
counties_UA_population = (pd.merge(counties_UA, population_df, on='CTYUA20CD', how='left')) # merge population data with counties_UA using the CTYUA20CD coloumn
del counties_UA_population['CTYUA20NMW'], counties_UA_population['BNG_E'], \
    counties_UA_population['BNG_N'], counties_UA_population['LONG'], \
    counties_UA_population['LAT'] # remove unwanted columns
print(counties_UA_population.columns) # check removal of columns and header check of merged table
print(counties_UA_population)
counties_UA_population.to_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\counties_UA_population.csv') # file note accurate, multiple islands grouped as one geometry are causing an issue with the output table.

# Use the def year_population function to pull the yearly population
#print('Please enter a year between 1991 and 2019?') #can i write a way for someone to inptu the year
year_population(2019) #print selected years population stats from the year_ppulation funcation above.
# print()
# year_population(2004)
# print()
# year_population(1991)

test_datasort = counties_UA_population[['County / unitary (as of April 2021)', '2019']] # selects the county/UA name column and population data for selected year
print(test_datasort.sort_values(['2019'], ascending=[False])) # rearranges given year data into descending order (highest to lowest populated counties/UA.

# provide yearly population data for a selected County/Unitary Authorities

#print('Please enter a County and/or Unitary Authorities from the list provided.') #can i write a way for someone to input the country and provide a list to selct from
print(counties_UA_population['County / unitary (as of April 2021)'])
counties_UA_population_data('Kent')
counties_UA_population_data('Conwy')
counties_UA_population_data('Devon')

# for a selected year can I print a line graph of the data? below has collected the row data for Kent but not sure what
# to do, should I be using an array?
test_county_select = (counties_UA_population[counties_UA_population['County / unitary (as of April 2021)'] == 'Kent']) # selects a neamed county/UA row and all the population data
print(test_county_select) # prints selected row
print(test_county_select.columns) # print coloumn headers
del test_county_select['OBJECTID'], test_county_select['CTYUA20CD'], test_county_select['CTYUA20NM'], \
    test_county_select['Shape__Are'], test_county_select['Shape__Len'], test_county_select['geometry'], \
    test_county_select['County / unitary (as of April 2021)'] # remove unnecessary columns
print(test_county_select.columns) # printed revised table, only printing years.

#Generate column population change (growth or loss) in counties and unitary authories in UK
# between 2001 to 2019 (cannot use 1991-2000 as no data for Ireland- see early for indiviudal maps)
counties_UA_population['Population change'] = counties_UA_population['2019'] - \
                                              counties_UA_population['2001']  # calculated population change 2019-2001

print(counties_UA_population)  # print the updated GeoDataFrame
print(counties_UA_population.sort_values(['Population change'], ascending=[False])) # arrange population change in descending order


# ---------------------------------------------------------------------------------------------------------------------
# below here, you may need to modify the script somewhat to create your map.


# figure for yearly population data
# create a figure of size 10x10 (representing the page size in inches
fig = plt.figure(figsize=(10, 10))

# create a crs using ccrs.UTM() that corresponds to our CRS
myCRS = ccrs.OSGB()

ax = plt.axes(projection=ccrs.OSGB()) # create an axes object in the figure, using Mercater projection to plot data


# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)
# ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

# plot the counties and unitary authority population data for a given year into our axis, using
counties_UA_population_plot = counties_UA_population.plot(column='2019', ax=ax, vmin=-1800, vmax=1600000, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label' : 'Population, in millions', 'orientation': 'vertical'})

# add counties_UA boundaries shapefile
counties_UA_outline = ShapelyFeature(counties_UA['geometry'], myCRS, edgecolor='k', facecolor='none', linewidth=0.2) # changed facecover
xmin, ymin, xmax, ymax = counties_UA.total_bounds
ax.add_feature(counties_UA_outline)

ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

county_handles = generate_handles([''], ['none'], edge='k')

ax.legend(county_handles, ['Counties and Unitary Authorities'], fontsize=8, loc='upper left', framealpha=1)

# add gridlines to figure
gridlines = ax.gridlines(draw_labels=True,
                        xlocs=[-8, -6, -4, -2, 0, +2],
                         ylocs=[52, 54, 56, 58, 60])
gridlines.right_labels = False
gridlines.bottom_labels = False

# add year title

title = 'my title' # modify to use year name
ax.set_title(title, fontdict={'fontsize': '12', 'fontweight': '5'})

# add scale bar

scale_bar(ax)

# save the figure

#fig.savefig('sample_pop_newscript2019.png', dpi=300, bbox_inches='tight')


# create a figure illustrating population loss/growth between 2001 and 2019

# figure for yearly population data
# create a figure of size 10x10 (representing the page size in inches
# fig2, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

# ax = plt.axes(projection=ccrs.Mercator()) # create an axes object in the figure, using Mercater projection to plot data

# add gridlines below
#gridlines = ax.gridlines(draw_labels=True,
#                         xlocs=[-8, -7, -6, -5, -4, -3, -2, -1, 0],
#                         ylocs=[54, 55, 56, 57, 58, 59, 60])
#gridlines.right_labels = False
#gridlines.bottom_labels = False

# to make a nice colorbar that stays in line with our map, use these lines:
#divider = make_axes_locatable(ax)
#cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the counties and unitary authority population data for a given year into our axis, using
# counties_UA_population_plot = counties_UA_population.plot(column='Population change', ax=ax, vmin=-7000, vmax=250000, cmap='PiYG',
#                       legend=True, cax=cax, legend_kwds={'label' : 'Population change', 'orientation': 'vertical'})

#counties_UA_outline = ShapelyFeature(counties_UA['geometry'], myCRS, edgecolor='k', facecolor='none', linewidth=0.2) # changed facecover
#ax.add_feature(counties_UA_outline)

#county_handles = generate_handles([''], ['none'], edge='k')

#ax.legend(county_handles, ['Counties'], fontsize=10, loc='upper left', framealpha=1)
# add year title to map/legend

# scale_bar(ax)

# save the figure
# plt.show()
#fig2.savefig('sample_pop_newscript_popchange.png', dpi=300, bbox_inches='tight')


# plot a line graph of data

