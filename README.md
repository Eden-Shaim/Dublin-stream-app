# Dublin stream app - Plan your ride
Dublin stream app - plan your ride is a real-time analisys app of dublin bus sensors data and dublin traffic tweets from @DublinLive.

To find the bus line that will take you to your desired destination - visit "which line to take?"
- Select your departure station and destination station and see which direct lines can serve you
- The requested stations will appear on the map on the right, where you can examine the different lines according to the route of their stations.

To plan your ride please visit "Real time traffic analysis" where you can find:
 - A prediction - will you encounter an accident\ road block in the time range you filtered with the bus line you chose? a probability for that event to happen
 - The temperature outside in the chosen time interval
 - The amout of rain outside in the chosen time interval
 - Avg delayes of your choosen bus line on the time interval you want to investigate 
 
To uploade new data - visit "upload" page. 

The uploaded data will aoutomaticlly be uploaded to Elastic search - our data werhouse ,and will feed the  "Real time traffic analysis" page.

## Data

Our main dataset contains 230 million records from bus sensors within Dublin, between July 2017 to September 2018.

In addition we integrated:
 - Dublin weather data from Kuggel : Attached a csv file is in the repository as "weather_ron_eden_updated.csv"
 - tweets on dublin traffic from @DublinLive that contain one or more words from the word-list ['traffic', 'Traffic', 'trafic', 'Trafic', 'crash', 'Crash', 'incident', 'Incident','accident', 'Accident', 'road', 'Road']. The csv file is attached as event_tweet_update1.csv
 
Dublin bus stops static data - the csv files are in the website directory, one is zipped due to lack of space.

## Technologies
*Apache Spark*  2.4.5 as processing framework.

Dockers for instaling *Elasticsearch*, All the data is loaded to Elasticsearch.

Analysis on the data with *Kibana* & *Apache Spark*

*kafka* as a suplier of streaming data

*Python* 3.5+ for runing the website

## Requirements

For running the files on a private environment, please install needed packages using: pip install -r requirement.txt.

## Instructions
To create the twitter data please run the script create_tweeter_data.py 

To save streaming data and the predictions on the stream data to Elastic serach use the warmup.ipynb notebook (also for the external data that can be uploaded from the web-app)

To run an H sample to solve the problem of the imbalance of our predicted label (event = car accident or roadblock) and to enhance the quality of the prediction using the bagging method please run creative - h_sampeing_with_bagging.ipynb notebook.
- An implementation of the suggested method in the article ["An Effective Method for Imbalanced Time Series Classification: Hybrid Sampling"](https://www.researchgate.net/publication/256838360_An_Effective_Method_for_Imbalanced_Time_Series_Classification_Hybrid_Sampling)
  
#### To start the web-app please run: website.py which is located in the website directory

Note: The page "which line to take?" in our site is based on static data we created from Dublin bus stops dataset which you can download from:
https://hub.arcgis.com/datasets/EsriIreland::dublin-bus-stops.

For your convenience we uploaded the ready csv files to the website directory

## App Usage
 - Find the appropriate line that connects the departure station to the destination station you need
 - You can get a snapshot of the traffic in Dulbin according to a filter for the line you selected and the desired time frame
 - You can get a prediction of whether there will be an event of a car accident or roadblock at the time you plan to leave
 
### Filter Data:
 - Click "+ Add Filter" from upper left corner of the page
 - The filter that is relevant for you is the one for "lineId" filed, there you can select the relevant line number. Then, click save. 
 - In the bar in the right corner you can select the time frame in which you plan to leave.

At any time, you can clear all the filters. 

## Upload Data:

The allowed schema for uploading new data is (mendatory) :

['_id', 'delay', 'congestion', 'lineId', 'vehicleId', 'timestamp', 'areaId', 'areaId1', 'areaId2',
'areaId3', 'gridID', 'actualDelay', 'longitude', 'latitude', 'currentHour', 'dateTypeEnum', 'angle',
'ellapsedTime', 'vehicleSpeed', 'distanceCovered', 'journeyPatternId', 'direction', 'busStop',
'poiId', 'poiId2', 'systemTimestamp', 'calendar', 'filteredActualDelay', 'atStop', 'dateType',
'justStopped', 'justLeftStop', 'probability', 'anomaly', 'loc']


