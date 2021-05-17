import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import pandas as pd

# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


plt.ion()

# ---------------------------------------------------------------------------------------------------------------------
# in this section, write the script to load the data and complete the main part of the analysis.
# load datasets
counties_UA = gpd.read_file (r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Counties_and_Unitary_Authorities.shp')
population_df = pd.read_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\population.csv') # uk population data from 1991 to 2019


# try to print the results to the screen using the format method demonstrated in the workbook
# print(counties.head())

# load the necessary data here and transform to a UTM projection
# counties = counties.to_crs(epsg=32629) # convert counties to UTM
# wards = wards.to_crs(epsg=32629) # convert wards to UTM

# next step merge population data table with counties_ua shapefile

counties_UA_population = (pd.merge(counties_UA, population_df, on='CTYUA20CD', how='left')) # merge population data with counties_ua
del counties_UA_population['CTYUA20NMW'], counties_UA_population['BNG_E'], counties_UA_population['BNG_N'], counties_UA_population['LONG'], counties_UA_population['LAT'] # remove unwanted columns
print(counties_UA_population.columns) # column headers from merged table

# your analysis goes here...

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
counties_UA_population_plot = counties_UA_population.plot(column='2019', ax=ax, vmin=2000, vmax=1600000, cmap='viridis',
                       legend=True, cax=cax)

counties_UA_outline = ShapelyFeature(counties_UA['geometry'], myCRS, edgecolor='k', facecolor='w', linewidth=0.2)
ax.add_feature(counties_UA_outline)

county_handles = generate_handles([''], ['none'], edge='r')

ax.legend(county_handles, ['Counties'], fontsize=12, loc='upper left', framealpha=1)

# save the figure
# plt.show()
fig.savefig('sample_pop_newscript.png', dpi=300, bbox_inches='tight')
