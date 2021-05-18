import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import pandas as pd

# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# add scale bar for maps
# create a scale bar of length 20 km in the upper right corner of the map - needs correcting


# add template for graphs

# plt.ion()

# ---------------------------------------------------------------------------------------------------------------------

# load datasets to be used in the analysis
countries = gpd.read_file(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Countries.shp') # 2020 UK country shapefile
counties_UA = gpd.read_file (r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Counties_and_Unitary_Authorities.shp') # 2020 UK Counties and Unitary Authorities shapefile
population_df = pd.read_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\population_number.csv') # UK population data from 1991 to 2019

# next step merge population data table with counties_ua shapefile

years = [str(yr) for yr in range(1991, 2020)]
population_df[years] = population_df[years].apply(pd.to_numeric, args=('coerce',))
counties_UA_population = (pd.merge(counties_UA, population_df, on='CTYUA20CD', how='left')) # merge population data with counties_ua
del counties_UA_population['CTYUA20NMW'], counties_UA_population['BNG_E'], counties_UA_population['BNG_N'], counties_UA_population['LONG'], counties_UA_population['LAT'] # remove unwanted columns
# print(counties_UA_population.columns) # column headers from merged table
print(counties_UA_population)
counties_UA_population.to_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\counties_UA_population.csv') # file note accurate

# mean_pop = (counties_UA_population['2019'].mean()) # calcualate mean counties_UA population for given year
# max_pop = (counties_UA_population['2019'].max()) # calcualate max counties_UA population for given year how name county?
# min_pop = (counties_UA_population['2019'].min()) # calcualate min counties_UA population for given year, how name county?
# total_pop = (counties_UA_population['2019'].sum()) # totals the poulation for the given year
# print('The mean county population for 2019 is {:.2f}.'.format(mean_pop)) # prints the mean counties_UA population for given year
# print('The maximum county population for 2019 is {:}.'.format(max_pop)) # prints the max counties_UA population for given year
# print('The minimum county population for 2019 is {:}.'.format(min_pop)) # prints the min counties_UA population for given year
# print('The UK population for 2019 is {:}.'.format(total_pop)) # prints the total population for the given year

def year_population(x): # make docstring
    x = str(x)
    mean_pop = (counties_UA_population[x].mean()) # this is wrong, not running on x running on 2019 hardwired?
    print('The mean county population in the year ' + str(x) + ' was {:,.2f}.'.format(mean_pop))
    max_pop = (counties_UA_population[x].max())
    print('The maximum county population in the year ' + str(x) + ' was {:,}.'.format(max_pop))
    min_pop = (counties_UA_population[x].min())
    print('The minimum county population in the year ' + str(x) + ' was {:,}.'.format(min_pop))
    total_pop = (counties_UA_population[x].sum())
    print('The UK population in the year ' + str(x) + ' was {:,}.'.format(total_pop))

year_population(2019)
print()
year_population(2004)
print()
year_population(1991)

test_datasort = counties_UA_population[['County / unitary (as of April 2021)', '2019']] # selects the county/UA name column and population data for selected year
print(test_datasort.sort_values(['2019'], ascending=[False])) # rearranges given year data into descending order (highest to lowest populated counties/UA.

test_county_select = (counties_UA_population[counties_UA_population['County / unitary (as of April 2021)'] == 'Kent']) # selects a neamed county/UA row and all the population data
print(test_county_select) # prints selected row

# write a function to provide a list of Counties/UA
def county_select(y):# for a given county select all the population data fom 1991 to 2019, make docstring
    test = (counties_UA_population[counties_UA_population['County / unitary (as of April 2021)'] == (y)])
    test.to_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\county_select_pop.csv') # want to save an output file with county name in it
    print(test)


county_select('Kent')
county_select('Conwy')
county_select('Devon')
# print polygon features (practical 3?)

test_county_select = (counties_UA_population[counties_UA_population['County / unitary (as of April 2021)'] == 'Kent']) # selects a neamed county/UA row and all the population data
print(test_county_select) # prints selected row

print(test_county_select.columns)

del test_county_select['OBJECTID'], test_county_select['CTYUA20CD'], test_county_select['CTYUA20NM'], test_county_select['Shape__Are'], test_county_select['Shape__Len'], test_county_select['geometry'], test_county_select['County / unitary (as of April 2021)']

print(test_county_select.columns)


# can i plot a figure of population difference (growth or loss) between 2001 and 2019
counties_UA_population['Population change'] = counties_UA_population['2019'] - counties_UA_population['2001']  # calculated population change 2019-2001 (cant use 1991-2000 as no data for ireland)

print(counties_UA_population)  # print the updated GeoDataFrame
print(counties_UA_population.sort_values(['Population change'], ascending=[False])) # arrange population change in descending order

# ---------------------------------------------------------------------------------------------------------------------
# below here, you may need to modify the script somewhat to create your map.
# create a crs using ccrs.UTM() that corresponds to our CRS
myCRS = ccrs.UTM(30)
# create a figure of size 10x10 (representing the page size in inches
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7, -6, -5, -4, -3, -2, -1, 0],
                         ylocs=[54, 55, 56, 57, 58, 59, 60])
gridlines.right_labels = False
gridlines.bottom_labels = False

# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the ward data into our axis, using
counties_UA_population_plot = counties_UA_population.plot(column='Population change', ax=ax, vmin=-7000, vmax=250000, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label' : 'Population change', 'orientation': 'vertical'})

counties_UA_outline = ShapelyFeature(counties_UA['geometry'], myCRS, edgecolor='k', facecolor='none', linewidth=0.2) # changed facecover
ax.add_feature(counties_UA_outline)

county_handles = generate_handles([''], ['none'], edge='k')

ax.legend(county_handles, ['Counties'], fontsize=10, loc='upper left', framealpha=1)
# add year title to map/legend

# scale_bar(ax)

# save the figure
# plt.show()
fig.savefig('sample_pop_newscript_popchange.png', dpi=300, bbox_inches='tight')


# plot a line graph of data
