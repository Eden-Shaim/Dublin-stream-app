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

### Twitter data
For running create_tweeter_data.py which creates the events_tweet file please install snscrape using: pip3 install snscrape


## Instructions
To create the twitter data please run the script create_tweeter_data.py 

To save streaming data and the predictions on the stream data to Elastic serach use the warmup.ipynb notebook

To run an H sample to solve the problem of the imbalance of our predicted label (event = car accident or roadblock) and to enhance the quality of the prediction using the bagging method please run _ notebook. Implementation of the suggested method from the article "An Effective Method for Imbalanced Time Series Classification: Hybrid Sampling"

To start the web-app please run: python _

## App Usage
