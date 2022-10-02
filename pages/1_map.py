# import libraries
from distutils.command.upload import upload
import os
import tensorflow as tf
import streamlit as st
from keras import backend as K 
import segmentation_models as sm
import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from patchify import patchify
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
st.set_option('deprecation.showPyplotGlobalUse', False)
from app import coord

################################################################################################################################

# save uploaded file to run into pre-trained ML model
uploaded_file = st.file_uploader('Upload map image file')
if uploaded_file:
  img = Image.open(uploaded_file)
  st.subheader("Your uploaded image:")
  st.image(img)
  img = img.save("Input.png")
else:
  st.write("Upload file please")
################################################################################################################################
# Jacard coef for model parameter input
def jacard_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (intersection + 1.0) / (K.sum(y_true_f) + K.sum(y_pred_f) + intersection + 1.0)

# balanced weights for model 
weights = [0.1666, 0.1666, 0.1666, 0.1666, 0.1666, 0.1666]
dice_loss = sm.losses.DiceLoss(class_weights=weights) 
focal_loss = sm.losses.CategoricalFocalLoss()
total_loss = dice_loss + (1 * focal_loss) 

# load pre-trained model
@st.cache(allow_output_mutation=True)
def load_model():
    model=tf.keras.models.load_model("models\satellite_standard_unet_100epochs.hdf5",
                   custom_objects={'dice_loss_plus_1focal_loss': total_loss,
                                   'jacard_coef':jacard_coef})
    return model

# spinner to show loading 
with st.spinner("Loading Pre-trained Unett Model...."):
    model=load_model()

################################################################################################################################

# cropping helper function
def prepare(path, patch_size):
    patch_dataset = []
    image = cv2.imread(path)
    # get x and y dimensions rounded to multiples of 256
    SIZE_X = (image.shape[1]//patch_size) * patch_size 
    SIZE_Y = (image.shape[0]//patch_size) * patch_size 
    image = Image.fromarray(image)

    # crop the image
    image = image.crop((0,0,SIZE_X, SIZE_Y))
    image = np.array(image)

    # Extract patches from image
    patches_img = patchify(image, (patch_size, patch_size, 3), step=patch_size)

    for i in range(patches_img.shape[0]):
        for j in range(patches_img.shape[1]):
            
            single_patch_img = patches_img[i,j,:,:]
            
            #Use minmaxscaler instead of just dividing by 255. 
            single_patch_img = scaler.fit_transform(single_patch_img.reshape(-1, single_patch_img.shape[-1])).reshape(single_patch_img.shape)
            
            #single_patch_img = (single_patch_img.astype('float32')) / 255. 
            single_patch_img = single_patch_img[0] #Drop the extra unecessary dimension that patchify adds.

            patch_dataset.append(single_patch_img)   
                                 
    return patch_dataset
  
# Predicting helper function
def predict(pred_img_input):
    pred_img_input=np.expand_dims(pred_img_input, 0)
    prediction = model.predict(pred_img_input)
    predicted_img=np.argmax(prediction, axis=3)[0,:,:] 
    return predicted_img

# helper function for counting number of pixels
def count_building_pixels(predicted_img):
    counter = 0
    for i in range(0, 256):
        for j in range(0, 256):
            if int(predicted_img[i][j]) == 1:
                counter += 1
    return counter

# helper function to plot predicted patches
def plotpred(img, number):
    plt.figure(figsize=(18,6))
    plt.subplot(121)
    plt.title("Patch " + str(number))
    plt.imshow(img)

################################################################################################################################

# get screenshot input from user
if (uploaded_file):
  path = "Input.png"
  pred_img_input = prepare(path, patch_size = 256)
  screenshotVisual = st.container()

  with screenshotVisual:
    # intialise columns
    col1, col2 = st.columns(2)

    # initialise array to store all the patches of predicted image
    predicted_imgs = []
    for i in range(0, len(pred_img_input)):
      if (i % 2 == 0):
        col1.image(pred_img_input[i],use_column_width=True)
        predicted_img = predict(pred_img_input[i])
        predicted_imgs.append(predicted_img)
      else:
        col2.image(pred_img_input[i],use_column_width=True)
        predicted_img = predict(pred_img_input[i])
        predicted_imgs.append(predicted_img)

################################################################################################################################

predictionVisual = st.container()

with predictionVisual:
  # intialise columns
  col1, col2 = st.columns(2)
  # plot predicted patches
  if(uploaded_file):
    for i in range(0, len(predicted_imgs)):
      if (i % 2 == 0):
        col1.pyplot(plotpred(predicted_imgs[i], i+1))
      else:
        col2.pyplot(plotpred(predicted_imgs[i], i+1))

################################################################################################################################

# section to allow user to choose which patch of the image they want to get the statistics of
choosePatch = st.container()

with choosePatch:
  st.write("----")
  if (uploaded_file):
    st.header("Choose patch that you are interested in")
    patch_no = st.number_input('Pick a patch number', 1, len(predicted_imgs))
    try: 
      st.pyplot(plotpred(predicted_imgs[patch_no-1],number=patch_no))
      counter = count_building_pixels(predicted_imgs[patch_no-1])
      st.write("Number of 'flat area'-encoded pixels: " + str(counter))
    except:
      st.write("Choose a patch!")

#0.299m per pixel length -> 0.0894sqm per pixel
if (uploaded_file):
  conversion_factor = 0.0894
  area = conversion_factor * counter
  st.write("Estimated surface area: " + str(int(area)) + "m^2")


################################################################################################################################

stats = st.container()

# the different regions of SG and their central lang and long
if (uploaded_file):
  with stats:
    Regions = ['North', 'South', 'East', 'West', 'Central']
    DirCoord = pd.DataFrame([[1.3691, 103.8454], [1.2807, 103.8711], [1.3450, 103.9832], [1.3555, 103.7308], [1.3516, 103.8995]], columns = ['lat', 'lon'], index = Regions)

    # find region of location inputted
    region = "1" #initialise region first
    lowest = 100
    for i in Regions:
        dist = (DirCoord['lat'][i] - coord[0])+ (DirCoord['lon'][i] - coord[1])
        if dist < lowest:
            lowest = dist
            region = i
            
    st.write("The current region of location input in Singapore is: ", region)

################################################################################################################################

# from weatherdata notebook
    col1, col2 = st.columns(2)
    PR = 0.7341
    A = 1.636141
    H_North = 1610
    H_South = 1580
    H_East = 1600
    H_West = 1570
    H_Central = 1590
    r = 0.20
    Efficiency = pd.DataFrame(columns = ['North', 'South', 'East', 'West', 'Central'])
    Efficiency.at['Energy output over a period of 1 Year, By Region(kWh)', 'North'] = A * PR * H_North * r
    Efficiency.at['Energy output over a period of 1 Year, By Region(kWh)','South'] = A * PR * H_South * r
    Efficiency.at['Energy output over a period of 1 Year, By Region(kWh)','East'] = A * PR * H_East * r
    Efficiency.at['Energy output over a period of 1 Year, By Region(kWh)','Central'] = A * PR * H_Central * r
    Efficiency.at['Energy output over a period of 1 Year, By Region(kWh)','West'] = A * PR * H_West * r
    col1.write(Efficiency)

    MoneySaved = pd.DataFrame(columns = ['Per Day', 'Per Month', 'Per Year'], index = ['North', 'South', 'East', 'West', 'Central'])
    # Average cost of electricity in Singapore is 32.28 cents per kWh
    cost = 32.28
    # Energy output over a period of 1 year, assuming 73.41% conversion of sunlight to electricity is described in Efficiency DataFrame
    energy_North = Efficiency.iloc[0,0] # This is taken for the North Region
    energy_South = Efficiency.iloc[0,1]
    energy_East = Efficiency.iloc[0,2]
    energy_West = Efficiency.iloc[0,3]
    energy_Central = Efficiency.iloc[0,4]
    # We multiply the hours of sunlight obtained on average, over the course of 1 year, the energy output specific to each Region
    actual_energy_North = energy_North * 11 
    actual_energy_South = energy_South * 10
    actual_energy_East = energy_East * 8
    actual_energy_West = energy_West * 9
    actual_energy_Central = energy_Central * 7
    # We divide the value obtained by; 365 to obtain power generated in one day, 30 to obtain power generated in one month

    actual_energy_day_North = actual_energy_North / 365
    actual_energy_month_North = actual_energy_day_North * 30
    actual_energy_year_North = actual_energy_month_North * 12

    actual_energy_day_South = actual_energy_South / 365
    actual_energy_month_South = actual_energy_day_South * 30
    actual_energy_year_South = actual_energy_month_South * 12

    actual_energy_day_East = actual_energy_East / 365
    actual_energy_month_East = actual_energy_day_East * 30
    actual_energy_year_East = actual_energy_month_East * 12

    actual_energy_day_West = actual_energy_West / 365
    actual_energy_month_West = actual_energy_day_West * 30
    actual_energy_year_West = actual_energy_month_West * 12

    actual_energy_day_Central = actual_energy_Central / 365
    actual_energy_month_Central = actual_energy_day_Central * 30
    actual_energy_year_Central = actual_energy_month_Central * 12

    # We then multiply each of the aforementioned values by 32.28 cents to obtain money saved through the Solar Panels
    cost_saved_day_North = actual_energy_day_North * cost / 100
    cost_saved_month_North = actual_energy_month_North * cost / 100
    cost_saved_year_North = actual_energy_year_North * cost / 100

    cost_saved_day_South = actual_energy_day_South * cost / 100
    cost_saved_month_South = actual_energy_month_South * cost / 100
    cost_saved_year_South = actual_energy_year_South * cost / 100

    cost_saved_day_East = actual_energy_day_East * cost / 100
    cost_saved_month_East = actual_energy_month_East * cost / 100
    cost_saved_year_East = actual_energy_year_East * cost / 100

    cost_saved_day_West = actual_energy_day_West * cost / 100
    cost_saved_month_West = actual_energy_month_West * cost / 100
    cost_saved_year_West = actual_energy_year_West * cost / 100

    cost_saved_day_Central = actual_energy_day_Central * cost / 100
    cost_saved_month_Central = actual_energy_month_Central * cost / 100
    cost_saved_year_Central = actual_energy_year_Central * cost / 100


    MoneySaved.at['North', 'Per Day'] = cost_saved_day_North
    MoneySaved.at['North', 'Per Month'] = cost_saved_month_North
    MoneySaved.at['North', 'Per Year'] = cost_saved_year_North
    MoneySaved.at['South', 'Per Day'] = cost_saved_day_South
    MoneySaved.at['South', 'Per Month'] = cost_saved_month_South
    MoneySaved.at['South', 'Per Year'] = cost_saved_year_South
    MoneySaved.at['East', 'Per Day'] = cost_saved_day_East
    MoneySaved.at['East', 'Per Month'] = cost_saved_month_East
    MoneySaved.at['East', 'Per Year'] = cost_saved_year_East
    MoneySaved.at['West', 'Per Day'] = cost_saved_day_West
    MoneySaved.at['West', 'Per Month'] = cost_saved_month_West
    MoneySaved.at['West', 'Per Year'] = cost_saved_year_West
    MoneySaved.at['Central', 'Per Day'] = cost_saved_day_Central
    MoneySaved.at['Central', 'Per Month'] = cost_saved_month_Central
    MoneySaved.at['Central', 'Per Year'] = cost_saved_year_Central
    col2.write(MoneySaved)
    
################################################################################################################################

    st.write("----")
    st.subheader("Assuming every inch of surface area can be used to deploy solar panels")
    panelArea = 1.636141
    
    if(region == "North"):
      ind = 1
    elif (region == "South"):
      ind = 2
    elif (region == "East"):
      ind = 3
    elif (region == "West"):
      ind = 4
    elif (region == "Central"):
      ind = 5

    st.write("Area for Commercial Solar Panels = 1.636141m^2") 
    st.write("Money saved per day: $" + str(int((area/panelArea) * MoneySaved['Per Day'][ind])))
    st.write("Money saved per month: $" + str(int((area/panelArea) * MoneySaved['Per Month'][ind])))
    st.write("Money saved per year: $" + str(int((area/panelArea) * MoneySaved['Per Year'][ind])))
    
    st.subheader("Disclaimer")
    st.write("We understand that the values might be inaccurate and largely overestimated in terms of money saved. This is due to the previous assumption.")
    st.write("Therefore, without further data, computational power and better models, we are unable to provide a better estimate.")
