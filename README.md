**![](https://lh4.googleusercontent.com/TsiWZ9fTYm4njrqMhPpnUXMKydEXvIaV43kQ4yfQQw7Mezske9ckWToNmdu7zlRQkveaZhWCf17d_Yy2XAkZWSEim2MdZTCkGPFHTtbNwN7NLBQ8UhEAmgOe1qHNpZuSL7X5yDRDWFY)**
# Disaster on Twitter
This project is to help relevant organization build situational awareness by live twitter data from the location identified by NASA satellite that’s on fire (detected by the surface temperature and light). So we can help people in need or arranging resources.

## 1. Work Flow
**![](https://lh3.googleusercontent.com/ejvRIPyVai61MylL3oU8seMUXsMzbk3l1l7lRzPWtruURWkDOYYqve1H5U5hjpHjJiKRONRt9UVy8CC3EJTMVEaiQ9sfJqj_16cDxIVIiQ4JQqFqj_-h10BmCoMhs68eI80vaUikJEo)**
### 1) Data collection
There are 3 types of data needed for this project. The over all work-flow for data collection is to collected labeled twitter data build a model. Using live satellite data to get fire coordinate information. Searching twitter in those in those locations as testing set to make prediction.
- 1) Training set.
Training data is from [CrisisNLP](https://crisisnlp.qcri.org/) and [Kaggle](https://www.kaggle.com/). With 8323 manually labeled twitter with relevance to fire disaster.
- 2) Live Fire Information
The Fire Information for Resource Management System ([FIRMS](https://firms.modaps.eosdis.nasa.gov/)) distributes Near Real-Time (NRT) active fire data within 3 hours of satellite observation from both the Moderate Resolution Imaging Spectroradiometer (MODIS) and the Visible Infrared Imaging Radiometer Suite (VIIRS).
- 3) Testing data from
Testing data is collected through [Twitter Python API](https://python-twitter.readthedocs.io/en/latest/). Search criterion is the fire coordinates generated from FIRMS and 10 miles radius
### 2) Modeling & Prediction
Training and testing twitter are both applied to stemming process first and then to a TFIDF vectorizer with a max feature of 2000.  After using NLP method clean and preprocess the Twitter data. I feed data into these 4 models, and the table shows the accuracy of each model. As we can see, SVC model have the highest accuracy.

||training|testing|
|---|---|---|
|Logistic Regression|95.6%|93.35%|
|SVC|97.99%|94.81%|
|Random Forest|86.42%|85.72%|
|Neural Network|94.23%|93.35%|

### 3) Visualization
[Folium](https://python-visualization.github.io/folium/) is based on leaflet.js and adapted to python, it’s very easy to use and powerful tool to build an interactive map. For this project I'm using Folium to build the map, the following link is a demonstration of how the map works:[Demo Map](https://rawcdn.githack.com/Kuduhe/Disaster_on_twitter/7d34d5a53e5314fad206902a2bc7b80a4bdf4d74/Maps/20191104map.html)
## 2. Map
Using [folium](https://python-visualization.github.io/folium/) to build Interactive map in HTML.
**![](./Maps/Demo.gif)**

## 3. Files

1. [Data collection](./Code/Data_collection.py)
2. [Data Cleaning](./Code/Cleaning.py)
3. [Modeling](./Code/Modeling.py)
4. [Mapping](/Code/Map.py)


## 4. Presentation
Here is a link to the [Presentation](https://docs.google.com/presentation/d/1BqGOjToTsxA7bS1ZYiku7zGGz6AGCvnpz2zphT1QKs8/edit?usp=sharing).
