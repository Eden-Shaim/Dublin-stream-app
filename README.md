# Dublin stream app - Plan your ride
Dublin stream app - plan your ride is a real-time analisys app of dublin bus sensors data and dublin traffic tweets from @DublinLive.

To find the bus line that will take you to your desired destination - visit "which line to take?"

To plan your ride please visit "Real time traffic analysis" where you can find:
 - Avg delayes of your choosen bus line on the time interval you want to investigate 
 - The temperature outside in the chosen time interval
 - A heat-map showing the congestion reports in the time interval, for the chosen line
 - A prediction - will you encounter an accident in the time range you filtered? a probability for an event to happen

To uploade new data - visit "upload" page


## Requirements

For running the files on a private environment please install needed packages using: pip install -r requirement.txt.

## Instructions
To create the twitter data please run the script create_tweeter_data.py 

To save streaming data and the predictions on the stream data to Elastic serach use the warmup.ipynb notebook (also for the external data that can be uploaded from the web-app)

To run an H sample to solve the problem of the imbalance of our predicted label (event = car accident or roadblock) and to enhance the quality of the prediction using the bagging method please run creative - h_sampeing_with_bagging.ipynb notebook.
- An implementation of the suggested method in the article ["An Effective Method for Imbalanced Time Series Classification: Hybrid Sampling"](https://www.researchgate.net/publication/256838360_An_Effective_Method_for_Imbalanced_Time_Series_Classification_Hybrid_Sampling)
  
#### To start the web-app please run: website.py

## App Usage
 - Find the appropriate line that connects the departure station to the destination station you need
 - You can get a snapshot of the traffic in Delbin according to a filter for the line you selected and the desired time frame
 - You can get a prediction of whether there will be an event of a car accident or roadblock at the time you plan to leave
 
### Filter Data:
 - Click "+ Add Filter" from upper left corner of the page
 - The filter that is relevant for you is the one for "lineId" filed, there you can select the relevant line number. Then, click save. 
 - In the bar in the right corner you can select the time frame in which you plan to leave.

At any time, you can clear all the filters. 

