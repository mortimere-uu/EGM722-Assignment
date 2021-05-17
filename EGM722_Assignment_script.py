import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import pandas as pd

# create functions and docstrings

# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# create a scale bar of length 20 km in the upper right corner of the map - needs correcting
#def scale_bar(ax, location=(0.92, 0.95)):
#    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
#    sbllx = (llx1 + llx0) / 2
#    sblly = lly0 + (lly1 - lly0) * location[1]

#    tmc = ccrs.TransverseMercator(sbllx, sblly)
#    x0, x1, y0, y1 = ax.get_extent(tmc)
#    sbx = x0 + (x1 - x0) * location[0]
#    sby = y0 + (y1 - y0) * location[1]

#    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=tmc)
#    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
#    plt.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=tmc)

#    plt.text(sbx, sby-4500, '20 km', transform=tmc, fontsize=8)
#    plt.text(sbx-12500, sby-4500, '10 km', transform=tmc, fontsize=8)
#    plt.text(sbx-24500, sby-4500, '0 km', transform=tmc, fontsize=8)

# load data for analysis

countries = gpd.read_file(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Countries.shp') # 2020 UK country .shp
counties_UA = gpd.read_file (r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Counties_and_Unitary_Authorities.shp')
# counties_1961 = gpd.read_file(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Counties_1961.shp') # 1961 counties data
# wards = gpd.read_file (r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Wards.shp') # 2011 wards data
population_df = pd.read_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\population.csv') # uk population data from 1991 to 2019

# print(countries.head())
# print(wards.crs)
# print(population_df.head()) # check population table data

# next step merge population data table with counties_ua shapefile

counties_UA_population = (pd.merge(counties_UA, population_df, on='CTYUA20CD', how='left')) # merge population data with counties_ua
del counties_UA_population['CTYUA20NMW'], counties_UA_population['BNG_E'], counties_UA_population['BNG_N'], counties_UA_population['LONG'], counties_UA_population['LAT'] # remove unwanted columns
print(counties_UA_population.columns) # column headers from merged table


newCRS = ccrs.UTM(30) # create a Universal Transverse Mercator reference system to transform the data.

testFig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=newCRS)) # create a figure of size 10x10 (representing the page siz in inches)

#ax = plt.axes(projection=ccrs.Mercator()) # create an axes object in the figure, using Mercater projection to plot data

# add gridlines below
# gridlines = ax.gridlines(draw_labels=True,
#                         Xlocx=[X, X, X, X, X],
#                         ylocs=[Y, Y, Y, Y])
# gridlines.right_labels = False
# gridline.bottom_labels = False

# colourbar
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.1, axes_class=plt.Axes)

# plot population country data
counties_UA_population_plot = counties_UA_population.plot(column='2018', ax=ax, vmin=2000, vmax=1600000, cmap='viridis',
                                                          legend=True, cax=cax)

country_outline = ShapelyFeature(countries['geometry'], newCRS, edgecolor='k', facecolor='w') # add the countries outlines to figure using cartopy's ShapelyFeature
xmin, ymin, xmax, ymax = countries.total_bounds
ax.add_feature(country_outline)

ax.set_extent([xmin, xmax, ymin, ymax], crs=newCRS)

counties_UA_outline = ShapelyFeature(counties_UA['geometry'], newCRS, edgecolor='k', facecolor='w', linewidth=0.2)
ax.add_feature(counties_UA_outline)
counties_handles = generate_handles([''], ['none'], edge='r')

ax.legend(counties_handles, ['Counties'], fontsize=12, loc='upper left', framealpha=1)
#wards_outline = ShapelyFeature(wards['geometry'], newCRS, edgecolor='k', facecolor='w', linewidth=0.2)
#ax.add_feature(wards_outline)

#scale_bar(ax)

testFig.savefig('testfig_population.png', bbox_inches='tight', dpi=300)

# join countries to counties/UA to generate summary statistics for countries
# print(countries.crs == counties_UA.crs) # test if crs are the same prior to join
# join = gpd.sjoin(countries, counties_UA, how='inner', lsuffix='left', rsuffix='right') # perfrom spatial join of countries to counties_ua
# print(join) # show the joined table




# line graphs