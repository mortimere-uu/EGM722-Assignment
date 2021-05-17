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
#def generate_handles(labels, colors, edge='k', alpha=1):
#    lc = len(colors)  # get the length of the color list
#    handles = []
#    for i in range(len(labels)):
#        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
#    return handles

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
counties_1961 = gpd.read_file(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Counties_1961.shp') # 1961 counties data
wards = gpd.read_file (r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\Wards.shp') # 2011 wards data
population_df = pd.read_csv(r'C:\Users\Ed\Documents\GitHub\EGM722_Assignment\data_files\population.csv') # uk population data from 1991 to 2019

# print(countries.head())
# print(wards.crs)
print(population_df.head()) # check population table data


testFig = plt.figure(figsize=(10, 10)) # create a figure of size 10x10 (representing the page siz in inches)

newCRS = ccrs.UTM(30) # create a Universal Transverse Mercator reference system to transform the data.

ax = plt.axes(projection=ccrs.Mercator()) # create an axes object in the figure, using Mercater projection to plot data

country_outline = ShapelyFeature(countries['geometry'], newCRS, edgecolor='k', facecolor='w') # add the countries outlines to figure using cartopy's ShapelyFeature
xmin, ymin, xmax, ymax = countries.total_bounds
ax.add_feature(country_outline)

ax.set_extent([xmin, xmax, ymin, ymax], crs=newCRS)

counties_UA_outline = ShapelyFeature(counties_UA['geometry'], newCRS, edgecolor='k', facecolor='w', linewidth=0.2)
ax.add_feature(counties_UA_outline)

wards_outline = ShapelyFeature(wards['geometry'], newCRS, edgecolor='k', facecolor='w', linewidth=0.2)
ax.add_feature(wards_outline)

#scale_bar(ax)

#testFig.savefig('testfig.png', bbox_inches='tight', dpi=300)

# join countries to counties/UA to generate summary statistics

# next step merge population data with counties