# -*- coding: utf-8 -*-
"""ndvi_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fPCNzHlP--9mtYJxzpUgL9fvB6bMpphO
"""

from google.colab import drive
drive.mount('/content/gdrive')

"""## Drive links:
1. Files - https://drive.google.com/drive/folders/1r1OjiEoqWs5J49QAyLytaf4SFKtYHI0h?usp=drive_link
2. Ndvi Tiff Data Raw - https://drive.google.com/drive/u/0/folders/1m9VIxtjSmBos-YhNcy3asaQptyC5iImj
"""



"""## Downloading NDVI data from Google Earth Engine"""

import ee
import rasterio
import numpy as np
import os
import pickle
import georasters as gr


# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project="ee-ashwins2407")

county_ids = [
    1, 3, 5, 7, 9, 11, 13, 15, 17, 19,
    21, 23, 25, 27, 29, 31, 33, 35, 37, 39,
    41, 43, 45, 47, 49, 51, 53, 55, 57, 59,
    61, 63, 65, 67, 69, 71, 73, 75, 77, 79,
    81, 83, 85, 87, 89, 91, 93, 95, 97, 99,
    101, 103, 105
]

# Define the region of interest (North Dakota bounding box)
region = ee.FeatureCollection('TIGER/2018/States').filter(ee.Filter.eq('NAME', 'North Dakota')).geometry()

# Load MODIS NDVI data for the desired date range and select NDVI band
modis_ndvi = ee.ImageCollection('MODIS/006/MOD13Q1') \
             .filterDate('2011-04-01', '2020-09-30') \
             .select('NDVI')

# Load the counties of North Dakota
counties_nd = ee.FeatureCollection('TIGER/2018/Counties').filter(ee.Filter.eq('STATEFP', '38'))

# Define a function to parse county feature properties
def parse_county(feature):
    return feature.set('COUNTYFP', ee.Number.parse(feature.get('COUNTYFP')))

# Map the function over the counties
counties_nd = counties_nd.map(parse_county)

# Define the export function
def export_ndvi_image_to_drive(image, export_name):
    task = ee.batch.Export.image.toDrive(image=image.toFloat(),
                                         description=export_name,
                                         folder='GEE_Exports',
                                         fileNamePrefix=export_name,
                                         region=region,
                                         scale=250,
                                         crs='EPSG:4326')
    task.start()

# Iterate over each year
for year in range(2012, 2021):
    # Filter NDVI images for the current year
    modis_ndvi_year = modis_ndvi.filterDate(str(year) + '-04-01', str(year) + '-09-30')

    # Calculate mean NDVI for the current year
    mean_ndvi_year = modis_ndvi_year.mean()

    # Iterate over each county
    for county_id in county_ids:  # North Dakota has 53 counties
        # Filter the county
        county = counties_nd.filterMetadata('COUNTYFP', 'equals', county_id).first()

        # Clip the NDVI image to the county
        clipped_ndvi = mean_ndvi_year.clip(county.geometry())

        # Export the clipped NDVI image to Google Drive
        export_name = f'NDVI_NorthDakota_County_{county_id}_Year_{year}'
        export_ndvi_image_to_drive(clipped_ndvi, export_name)

print('Batch exporting NDVI images for North Dakota counties from April to September for the past 10 years.')

import ee

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project="ee-ashwinsmys")

county_ids_sd = [
    3, 5, 7, 9, 11, 13, 15, 17, 19, 21,
    23, 25, 27, 29, 31, 33, 35, 37, 39, 41,
    43, 45, 47, 49, 51, 53, 55, 57, 59, 61,
    63, 65, 67, 69, 71, 73, 75, 77, 79, 81,
    83, 85, 87, 89, 91, 93, 95, 97, 99, 101,
    103, 105, 107, 109, 111, 113, 115, 117, 119,
    121, 123, 125, 127, 129, 135, 137
]

# Define the region of interest (North Dakota bounding box)
region = ee.FeatureCollection('TIGER/2018/States').filter(ee.Filter.eq('NAME', 'South Dakota')).geometry()

# Load MODIS NDVI data for the desired date range and select NDVI band
modis_ndvi = ee.ImageCollection('MODIS/006/MOD13Q1') \
             .filterDate('2011-04-01', '2020-09-30') \
             .select('NDVI')

# Load the counties of North Dakota
counties_nd = ee.FeatureCollection('TIGER/2018/Counties').filter(ee.Filter.eq('STATEFP', '46'))

# Define a function to parse county feature properties
def parse_county(feature):
    return feature.set('COUNTYFP', ee.Number.parse(feature.get('COUNTYFP')))

# Map the function over the counties
counties_nd = counties_nd.map(parse_county)

# Define the export function
def export_ndvi_image_to_drive(image, export_name):
    task = ee.batch.Export.image.toDrive(image=image.toFloat(),
                                         description=export_name,
                                         folder='GEE_Exports',
                                         fileNamePrefix=export_name,
                                         region=region,
                                         scale=250,
                                         crs='EPSG:4326')
    task.start()

# Iterate over each year
for year in range(2012, 2021):
    # Filter NDVI images for the current year
    modis_ndvi_year = modis_ndvi.filterDate(str(year) + '-04-01', str(year) + '-09-30')

    # Calculate mean NDVI for the current year
    mean_ndvi_year = modis_ndvi_year.mean()

    # Iterate over each county
    for county_id in county_ids_sd:  # South Dakota has 67 counties
        # Filter the county
        county = counties_nd.filterMetadata('COUNTYFP', 'equals', county_id).first()

        # Clip the NDVI image to the county
        clipped_ndvi = mean_ndvi_year.clip(county.geometry())

        # Export the clipped NDVI image to Google Drive
        export_name = f'NDVI_SouthDakota_County_{county_id}_Year_{year}'
        export_ndvi_image_to_drive(clipped_ndvi, export_name)

print('Batch exporting NDVI images for South Dakota counties from April to September for the past 10 years.')



import ee

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project="ee-ashwinsmys")

county_ids_mt = [
    3, 5, 7, 9, 11, 13, 15, 17, 19, 21,
    23, 25, 27, 29, 31, 33, 35, 37, 39, 41,
    43, 45, 47, 49, 51, 53, 55, 57, 59, 61,
    63, 65, 67, 69, 71, 73, 75, 77, 79, 81,
    83, 85, 87, 89, 91, 93, 95, 97, 99, 101,
    103, 105, 107, 109, 111
]

# Define the region of interest (North Dakota bounding box)
region = ee.FeatureCollection('TIGER/2018/States').filter(ee.Filter.eq('NAME', 'Montana')).geometry()

# Load MODIS NDVI data for the desired date range and select NDVI band
modis_ndvi = ee.ImageCollection('MODIS/006/MOD13Q1') \
             .filterDate('2011-04-01', '2020-09-30') \
             .select('NDVI')

# Load the counties of North Dakota
counties_nd = ee.FeatureCollection('TIGER/2018/Counties').filter(ee.Filter.eq('STATEFP', '30'))

# Define a function to parse county feature properties
def parse_county(feature):
    return feature.set('COUNTYFP', ee.Number.parse(feature.get('COUNTYFP')))

# Map the function over the counties
counties_nd = counties_nd.map(parse_county)

# Define the export function
def export_ndvi_image_to_drive(image, export_name):
    task = ee.batch.Export.image.toDrive(image=image.toFloat(),
                                         description=export_name,
                                         folder='GEE_Exports',
                                         fileNamePrefix=export_name,
                                         region=region,
                                         scale=250,
                                         crs='EPSG:4326')
    task.start()

# Iterate over each year
for year in range(2012, 2021):
    # Filter NDVI images for the current year
    modis_ndvi_year = modis_ndvi.filterDate(str(year) + '-04-01', str(year) + '-09-30')

    # Calculate mean NDVI for the current year
    mean_ndvi_year = modis_ndvi_year.mean()

    # Iterate over each county
    for county_id in county_ids_mt:  # Montana has 56 counties
        # Filter the county
        county = counties_nd.filterMetadata('COUNTYFP', 'equals', county_id).first()

        # Clip the NDVI image to the county
        clipped_ndvi = mean_ndvi_year.clip(county.geometry())

        # Export the clipped NDVI image to Google Drive
        export_name = f'NDVI_Montana_County_{county_id}_Year_{year}'
        export_ndvi_image_to_drive(clipped_ndvi, export_name)

print('Batch exporting NDVI images for Montana counties from April to September for the past 10 years.')

"""## tif preprocessing"""

#!pip install rasterio

#!pip install georasters


#import cupy as cp

def tif_plot(img_path):
    # Read tiff file
    tiff_img = gr.from_file(img_path)
    tiff_img.plot()
    # Convert the tiff image to a NumPy array
    tiff_array = tiff_img.raster

    # Print the array shape
    print("Tiff Array Shape:", tiff_array.shape)

    return tiff_array

tif_ar = tif_plot('/content/gdrive/MyDrive/GEE_Exports/NDVI_NorthDakota_County_1_Year_2013.tif')

def tif_preprocessing(img_path):
    # Open GeoTIFF file
    with rasterio.open(img_path) as src:
        # Print raster properties
        #print("Raster bounds:", src.bounds)
        #print("Raster shape:", src.shape)

        # Read raster data
        raster_data = src.read(1)  # Read the first band
        raster_data = np.array(raster_data)  # Convert to NumPy array
        #cupy_raster_data = cp.asarray(raster_data)
        # Print raster data
        #print("Raster data:", raster_data)
        return raster_data

dir_path = "/content/gdrive/MyDrive/GEE_Exports/"
img_paths = os.listdir('/content/gdrive/MyDrive/GEE_Exports')
print("No of Tif files:", len(img_paths))

nd_imgs = []
sd_imgs = []
mn_imgs = []

for path in img_paths:
  if path.split("_")[1] == "Montana":
    mn_imgs.append(path)
  elif path.split("_")[1] == "SouthDakota":
    sd_imgs.append(path)
  else:
    nd_imgs.append(path)

print(len(mn_imgs))
print(len(sd_imgs))
print(len(nd_imgs))

def replace_nan_inf(tif_arr):
  # Iterate over each image in the array
  for i in range(tif_arr.shape[0]):
    # Replace NaN values with 0 and ensure data type is float
    tif_arr[i] = np.nan_to_num(tif_arr[i], nan=0, posinf=0, neginf=0).astype(float)
  return tif_arr

def remove_sparsity(image):
    # Find non-zero pixels
    non_zero_pixels = np.nonzero(image)

    # Calculate bounding box with margin
    min_y = max(0, np.min(non_zero_pixels[0]) - 5)
    max_y = min(image.shape[0], np.max(non_zero_pixels[0]) + 6)
    min_x = max(0, np.min(non_zero_pixels[1]) - 5)
    max_x = min(image.shape[1], np.max(non_zero_pixels[1]) + 6)

    # Crop the image to the bounding box
    cropped_image = image[min_y:max_y, min_x:max_x]

    return cropped_image

def process_tif_images(img_paths, dir_path):
    # Calculate the total number of images
    total_images = len(img_paths)

    # Initialize lists for cropped images, shapes, county IDs, and years
    cropped_images = []
    cropped_img_shapes = []
    tif_county_id = []
    tif_county_year = []

    # Find the maximum height and width among all images
    max_height, max_width = 0, 0
    for img_path in img_paths:
        # Read TIFF image and remove sparsity
        tif_img = tif_preprocessing(dir_path + img_path)
        cropped_image = remove_sparsity(replace_nan_inf(tif_img))

        # Append cropped image and its shape
        cropped_images.append(cropped_image)
        cropped_img_shapes.append(cropped_image.shape)

        # Extract county ID and year from the image path
        county_id = int(img_path.split("_")[3])
        year = int(img_path.split("_")[-1][:-4])

        # Append county ID and year
        tif_county_id.append(county_id)
        tif_county_year.append(year)

        # Update maximum height and width
        max_height = max(max_height, cropped_image.shape[0])
        max_width = max(max_width, cropped_image.shape[1])

    # Pad each image to match the maximum height and width
    padded_images = []
    for image, shape in zip(cropped_images, cropped_img_shapes):
        pad_height = max_height - shape[0]
        pad_width = max_width - shape[1]
        padded_image = np.pad(image, ((0, pad_height), (0, pad_width)), mode='constant')
        padded_images.append(padded_image)

    # Stack padded images into a single NumPy array
    ndvi_padded_array = np.array(padded_images)

    return ndvi_padded_array, tif_county_id, tif_county_year

mn_ndvi_arr1, mn_tif_county_id1, mn_tif_county_year1 = process_tif_images(mn_imgs[:250], dir_path)

mn_ndvi_arr2, mn_tif_county_id2, mn_tif_county_year2 = process_tif_images(mn_imgs[250:], dir_path)

print(mn_ndvi_arr1.shape)
print(mn_ndvi_arr2.shape)

mn_ndvi_arr = np.concatenate((mn_ndvi_arr1, mn_ndvi_arr2), axis=0)
mn_tif_county_id = mn_tif_county_id1 + mn_tif_county_id2
mn_tif_county_year = mn_tif_county_year1 + mn_tif_county_year2
mn_ndvi_arr.shape

sd_ndvi_arr1, sd_tif_county_id1, sd_tif_county_year1 = process_tif_images(sd_imgs[:290], dir_path)

sd_ndvi_arr2, sd_tif_county_id2, sd_tif_county_year2 = process_tif_images(sd_imgs[290:], dir_path)

print(sd_ndvi_arr1.shape)
print(sd_ndvi_arr2.shape)

sd_ndvi_arr = np.concatenate((sd_ndvi_arr1, sd_ndvi_arr2), axis=0)
sd_tif_county_id = sd_tif_county_id1 + sd_tif_county_id2
sd_tif_county_year = sd_tif_county_year1 + sd_tif_county_year2
sd_ndvi_arr.shape

nd_ndvi_arr1, nd_tif_county_id1, nd_tif_county_year1 = process_tif_images(nd_imgs[:260], dir_path)

nd_ndvi_arr2, nd_tif_county_id2, nd_tif_county_year2 = process_tif_images(nd_imgs[260:], dir_path)

print(nd_ndvi_arr1.shape)
print(nd_ndvi_arr2.shape)

nd_ndvi_arr = np.concatenate((nd_ndvi_arr1, nd_ndvi_arr2), axis=0)
nd_tif_county_id = nd_tif_county_id1 + nd_tif_county_id2
nd_tif_county_year = nd_tif_county_year1 + nd_tif_county_year2
nd_ndvi_arr.shape



def get_county_names(county_data, tif_county_id):
  # Create a dictionary mapping county IDs to names
  county_mapping = {county_id: county_name for county_id, county_name in county_data}

  # List of county names corresponding to county IDs
  tif_county_name = [county_mapping[county_id] for county_id in tif_county_id]
  return tif_county_name

# Define the list of county IDs and names for ND
county_data_nd = [
    (1, 'Adams'),
    (3, 'Barnes'),
    (5, 'Benson'),
    (7, 'Billings'),
    (9, 'Bottineau'),
    (11, 'Bowman'),
    (13, 'Burke'),
    (15, 'Burleigh'),
    (17, 'Cass'),
    (19, 'Cavalier'),
    (21, 'Dickey'),
    (23, 'Divide'),
    (25, 'Dunn'),
    (27, 'Eddy'),
    (29, 'Emmons'),
    (31, 'Foster'),
    (33, 'Golden Valley'),
    (35, 'Grand Forks'),
    (37, 'Grant'),
    (39, 'Griggs'),
    (41, 'Hettinger'),
    (43, 'Kidder'),
    (45, 'LaMoure'),
    (47, 'Logan'),
    (49, 'McHenry'),
    (51, 'McIntosh'),
    (53, 'McKenzie'),
    (55, 'McLean'),
    (57, 'Mercer'),
    (59, 'Morton'),
    (61, 'Mountrail'),
    (63, 'Nelson'),
    (65, 'Oliver'),
    (67, 'Pembina'),
    (69, 'Pierce'),
    (71, 'Ramsey'),
    (73, 'Ransom'),
    (75, 'Renville'),
    (77, 'Richland'),
    (79, 'Rolette'),
    (81, 'Sargent'),
    (83, 'Sheridan'),
    (85, 'Sioux'),
    (87, 'Slope'),
    (89, 'Stark'),
    (91, 'Steele'),
    (93, 'Stutsman'),
    (95, 'Towner'),
    (97, 'Traill'),
    (99, 'Walsh'),
    (101, 'Ward'),
    (103, 'Wells'),
    (105, 'Williams')
]

nd_tif_county_name = get_county_names(county_data_nd, nd_tif_county_id)

#for Montana
county_data_mn = [
    (1, 'Beaverhead'),
    (3, 'Big Horn'),
    (5, 'Blaine'),
    (7, 'Broadwater'),
    (9, 'Carbon'),
    (11, 'Carter'),
    (13, 'Cascade'),
    (15, 'Chouteau'),
    (17, 'Custer'),
    (19, 'Daniels'),
    (21, 'Dawson'),
    (23, 'Anaconda-Deer Lodge'),
    (25, 'Fallon'),
    (27, 'Fergus'),
    (29, 'Flathead'),
    (31, 'Gallatin'),
    (33, 'Garfield'),
    (35, 'Glacier'),
    (37, 'Golden Valley'),
    (39, 'Granite'),
    (41, 'Hill'),
    (43, 'Jefferson'),
    (45, 'Judith Basin'),
    (47, 'Lake'),
    (49, 'Lewis and Clark'),
    (51, 'Liberty'),
    (53, 'Lincoln'),
    (55, 'McCone'),
    (57, 'Madison'),
    (59, 'Meagher'),
    (61, 'Mineral'),
    (63, 'Missoula'),
    (65, 'Musselshell'),
    (67, 'Park'),
    (69, 'Petroleum'),
    (71, 'Phillips'),
    (73, 'Pondera'),
    (75, 'Powder River'),
    (77, 'Powell'),
    (79, 'Prairie'),
    (81, 'Ravalli'),
    (83, 'Richland'),
    (85, 'Roosevelt'),
    (87, 'Rosebud'),
    (89, 'Sanders'),
    (91, 'Sheridan'),
    (93, 'Butte-Silver Bow'),
    (95, 'Stillwater'),
    (97, 'Sweet Grass'),
    (99, 'Teton'),
    (101, 'Toole'),
    (103, 'Treasure'),
    (105, 'Valley'),
    (107, 'Wheatland'),
    (109, 'Wibaux'),
    (111, 'Yellowstone')
]

mn_tif_county_name = get_county_names(county_data_mn, mn_tif_county_id)

county_data_sd = [
    (3, 'Aurora'),
    (5, 'Beadle'),
    (7, 'Bennett'),
    (9, 'Bon Homme'),
    (11, 'Brookings'),
    (13, 'Brown'),
    (15, 'Brule'),
    (17, 'Buffalo'),
    (19, 'Butte'),
    (21, 'Campbell'),
    (23, 'Charles Mix'),
    (25, 'Clark'),
    (27, 'Clay'),
    (29, 'Codington'),
    (31, 'Corson'),
    (33, 'Custer'),
    (35, 'Davison'),
    (37, 'Day'),
    (39, 'Deuel'),
    (41, 'Dewey'),
    (43, 'Douglas'),
    (45, 'Edmunds'),
    (47, 'Fall River'),
    (49, 'Faulk'),
    (51, 'Grant'),
    (53, 'Gregory'),
    (55, 'Haakon'),
    (57, 'Hamlin'),
    (59, 'Hand'),
    (61, 'Hanson'),
    (63, 'Harding'),
    (65, 'Hughes'),
    (67, 'Hutchinson'),
    (69, 'Hyde'),
    (71, 'Jackson'),
    (73, 'Jerauld'),
    (75, 'Jones'),
    (77, 'Kingsbury'),
    (79, 'Lake'),
    (81, 'Lawrence'),
    (83, 'Lincoln'),
    (85, 'Lyman'),
    (87, 'McCook'),
    (89, 'McPherson'),
    (91, 'Marshall'),
    (93, 'Meade'),
    (95, 'Mellette'),
    (97, 'Miner'),
    (99, 'Minnehaha'),
    (101, 'Moody'),
    (103, 'Pennington'),
    (105, 'Perkins'),
    (107, 'Potter'),
    (109, 'Roberts'),
    (111, 'Sanborn'),
    (113, 'Shannon'),
    (115, 'Spink'),
    (117, 'Stanley'),
    (119, 'Sully'),
    (121, 'Todd'),
    (123, 'Tripp'),
    (125, 'Turner'),
    (127, 'Union'),
    (129, 'Walworth'),
    (135, 'Yankton'),
    (137, 'Ziebach')
]

sd_tif_county_name = get_county_names(county_data_sd, sd_tif_county_id)



"""## wheat data preprocessing"""

import pandas as pd
import numpy as np

def wheat_csv_preprocess(df_path):
  wheat_df = pd.read_csv(df_path)
  wheat_df = wheat_df[['Year', 'County', 'Data Item', 'Value']]
  new_df = wheat_df.groupby(['Year', 'County'])['Value'].sum().reset_index()
  new_df = new_df.rename(columns={'Value': 'Yield (BU/acre)'})

  return new_df

wheat_df_path_mn = '/content/gdrive/MyDrive/Agri_Policy_Proj/wheat_yield_mn_2011_2020.csv'
wheat_df_mn = wheat_csv_preprocess(wheat_df_path_mn)
wheat_df_mn.head()

wheat_df_mn['Year'].value_counts()

wheat_df_path_sd = '/content/gdrive/MyDrive/Agri_Policy_Proj/wheat_yield_sd_2011_2020.csv'
wheat_df_sd = wheat_csv_preprocess(wheat_df_path_sd)
wheat_df_sd.head()

wheat_df_sd['Year'].value_counts()

wheat_df_path_nd = '/content/gdrive/MyDrive/Agri_Policy_Proj/wheat_yield_nd_2011_2020_53counties.csv'
wheat_df_nd = wheat_csv_preprocess(wheat_df_path_nd)
wheat_df_nd.head()

wheat_df_nd['Year'].value_counts()



"""## Wheat data X NDVI data processing"""

def ndvi_wheat_preprocess(tif_arr, tif_county_id,
                          tif_county_name, tif_county_year, wheat_df):
  temp = {
    'Array_Ind': np.arange(len(tif_arr)),
    'Year': tif_county_year,
    'County_ID': tif_county_id,
    'County': tif_county_name,
  }
  temp_df = pd.DataFrame(temp)
  temp_df['County'] = temp_df['County'].str.upper()

  merged_df = pd.merge(temp_df, wheat_df, on=['Year', 'County'], how='inner')

  # Reorder columns as per your requirement
  merged_df = merged_df[['Array_Ind', 'Year', 'County_ID', 'County', 'Yield (BU/acre)']]
  #print(merged_df.shape)
  array_ind = list(merged_df[['Array_Ind']].values)

  total_img = len(array_ind)

  h = tif_arr.shape[1]
  w = tif_arr.shape[2]
  # Preallocate space for the final array
  new_ndvi_arr = np.empty((total_img+1, h, w)) # Adding 1 for the initial array

  # Read and append each image to the final array
  for index, arr_ind in enumerate(array_ind):
    new_ndvi_arr[index + 1] = tif_arr[arr_ind]

  new_ndvi_arr = new_ndvi_arr[1:]

  return new_ndvi_arr, merged_df

new_ndvi_arr_mn, merged_df_mn = ndvi_wheat_preprocess(mn_ndvi_arr, mn_tif_county_id, mn_tif_county_name, mn_tif_county_year, wheat_df_mn)
new_ndvi_arr_mn.shape

new_ndvi_arr_sd, merged_df_sd = ndvi_wheat_preprocess(sd_ndvi_arr, sd_tif_county_id, sd_tif_county_name, sd_tif_county_year, wheat_df_sd)
new_ndvi_arr_sd.shape

new_ndvi_arr_nd, merged_df_nd = ndvi_wheat_preprocess(nd_ndvi_arr, nd_tif_county_id, nd_tif_county_name, nd_tif_county_year, wheat_df_nd)
new_ndvi_arr_nd.shape

def save_preprocessed(ndvi_arr, merged_df, filename):
  ndvi_yield_preprocessed = {"NDVI_Array": ndvi_arr,
                    "County_ID": list(merged_df['County_ID']),
                    "County_Name": list(merged_df['County']),\
                    "Year": list(merged_df['Year']),
                    "Yield": list(merged_df['Yield (BU/acre)'])

                    }

  pickle_filename = '/content/gdrive/MyDrive/Agri_Policy_Proj/' + filename

  # Save the dictionary as a pickle file
  with open(pickle_filename, 'wb') as f:
    pickle.dump(ndvi_yield_preprocessed, f)
  print("File Saved")

save_preprocessed(new_ndvi_arr_mn, merged_df_mn, 'ndvi_yield_mn.pkl')

save_preprocessed(new_ndvi_arr_sd, merged_df_sd, 'ndvi_yield_sd.pkl')

save_preprocessed(new_ndvi_arr_nd, merged_df_nd, 'ndvi_yield_nd.pkl')

def open_pickle_file(filename):
    pickle_filename = '/content/gdrive/MyDrive/Agri_Policy_Proj/' + filename

    with open(pickle_filename, 'rb') as f:
        data = pickle.load(f)
    print("File Loaded Successfully")
    return data

ndvi_yield_mn = open_pickle_file('ndvi_yield_mn.pkl')
ndvi_yield_sd = open_pickle_file('ndvi_yield_sd.pkl')
ndvi_yield_nd = open_pickle_file('ndvi_yield_nd.pkl')

print(ndvi_yield_mn['NDVI_Array'].shape)
print(ndvi_yield_sd['NDVI_Array'].shape)
print(ndvi_yield_nd['NDVI_Array'].shape)

ndvi_arr_mn = ndvi_yield_mn['NDVI_Array']
ndvi_arr_sd = ndvi_yield_sd['NDVI_Array']
ndvi_arr_nd = ndvi_yield_nd['NDVI_Array']

yield_mn = ndvi_yield_mn['Yield']
yield_sd = ndvi_yield_sd['Yield']
yield_nd = ndvi_yield_nd['Yield']

county_id_mn = ndvi_yield_mn['County_ID']
county_id_sd = ndvi_yield_sd['County_ID']
county_id_nd = ndvi_yield_nd['County_ID']

county_name_mn = ndvi_yield_mn['County_Name']
county_name_sd = ndvi_yield_sd['County_Name']
county_name_nd = ndvi_yield_nd['County_Name']

year_mn = ndvi_yield_mn['Year']
year_sd = ndvi_yield_sd['Year']
year_nd = ndvi_yield_nd['Year']



def pad_and_concatenate_arrays(array1, array2, array3, target_shape=(800, 1120)):
    # Pad each array to the target shape
    padded_array1 = np.pad(array1, ((0, 0),
                                    (0, target_shape[0] - array1.shape[1]),
                                    (0, target_shape[1] - array1.shape[2])),
                           mode='constant')

    padded_array2 = np.pad(array2, ((0, 0),
                                    (0, target_shape[0] - array2.shape[1]),
                                    (0, target_shape[1] - array2.shape[2])),
                           mode='constant')

    padded_array3 = np.pad(array3, ((0, 0),
                                    (0, target_shape[0] - array3.shape[1]),
                                    (0, target_shape[1] - array3.shape[2])),
                           mode='constant')

    # Concatenate the padded arrays along axis 0
    concatenated_array = np.concatenate((padded_array1, padded_array2, padded_array3), axis=0)

    return concatenated_array

ndvi_all = pad_and_concatenate_arrays(ndvi_arr_mn, ndvi_arr_sd, ndvi_arr_nd, target_shape=(800, 1120))
ndvi_all.shape

yield_all = np.array(yield_mn + yield_sd + yield_nd)
yield_all.shape

county_id_all = np.array(county_id_mn + county_id_sd + county_id_nd)
county_name_all = np.array(county_name_mn + county_name_sd + county_name_nd)
year_all = np.array(year_mn + year_sd + year_nd)

ndvi_yield_all = {"NDVI_Array": ndvi_all,
                  "County_ID": county_id_all,
                  "County_Name": county_name_all,
                  "Year": year_all,
                  "Yield": yield_all
                   }

pickle_filename = '/content/gdrive/MyDrive/Agri_Policy_Proj/ndvi_yield_all.pkl'

  # Save the dictionary as a pickle file
with open(pickle_filename, 'wb') as f:
  pickle.dump(ndvi_yield_all, f)
print("File Saved")

