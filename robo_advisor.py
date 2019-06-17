# TO RUN THIS SCRIPT COPY THIS COMMAND INTO THE TERMINAL -----> python robo_advisor.py

packages_setup = ['''

conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env

pip install -r requirements.txt
pip install pytest # (only if you'll be writing tests)

python robo_advisor.py

''']


# Examples (click for JSON output)
# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo

# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=demo



# To issue an http request in python, you must import a 'request package'

import os
import requests
import json # need this to import json string into dictionary
from datetime import datetime # taken from stackoverflow
import csv # so you can write date to .csv

##### THIS SECTION HERE ENABLES + ALLOWS YOU TO USE .ENV FILES WHERE API KEY IS STORED ################################################

# Derived from course repository and robo-advisor video guide

from dotenv import load_dotenv 
import requests

load_dotenv() #> loads contents of the .env file into the script's environment

api_key = os.environ.get("ALPHAVANTAGE_API_KEY") # default to using the "demo" key if an Env Var is not supplied
#  However, the "ALPHAVANTAGE_API_KEY" will refer to the api key that you have generated and stored on the .env file


# print(api_key) --> don't include this as the api key is secret, but it worked ! *thumbs up!*

#######################################################################################################################################



# Current Time for transaction pull
date_time = datetime.now().strftime("%m/%d/%Y, %I:%M:%S%P\n")
# print(date_time)

# Also, we know that we are working with $ pricing so let's get the formatting out of the way

def usd_format(my_price):
    return "${0:,.2f}".format(my_price) # This UDF will change numerical denomination to currency and cents format when passed through


# api_key = "demo" --> no longer in use, API_KEY


print("Please enter a valid stock ticker symbol!  As an example, Disney is 'DIS' and AT&T is 'T'. ")
user_input_ticker = input()

# testuser_input_ticker = input()


request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={user_input_ticker}&apikey={api_key}"

response = requests.get(request_url)

# print(type(response))
# print(response.status_code)
# print(response.text) # This is a string

parsed_response = json.loads(response.text) #this converts string format into dictionary

dates_list = list(parsed_response["Time Series (Daily)"].keys()) # convert the dates dictionary keys into list format


current_date = dates_list[0] # son loads will alphavantage's most recent values that is already sorted, but might need to sort just in case later

traded_stock_ticker = parsed_response["Meta Data"]["2. Symbol"]

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
most_recent_close = parsed_response["Time Series (Daily)"][current_date]["4. close"]
most_recent_high = parsed_response["Time Series (Daily)"][current_date]["2. high"]
most_recent_low = parsed_response["Time Series (Daily)"][current_date]["3. low"]
most_recent_total_volumes_traded = parsed_response["Time Series (Daily)"][current_date]["5. volume"]


# To find out what the keys are in dictionary format, remember to use command ' parsed_response.keys() '
# Now let's dig a bit deeper, use format ' parsed_response["Meta Data"] ' to find the contents within this key, a.k.a. nested data
# Further inspection of nested data you can use ' parsed_response["Meta Data"]["3. Last Refreshed"] ' --> Last refreshed portion
# Now let's try finding the most recent close.  To access this, you need to access the nested dictionary.
# Enter parsed_response into the terminal to expand dict.keys(), which you find that nested structure or refer to 
# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo
# to find the structure.  You find that the format is ' parsed_response["Time Series (Daily)"][current_date]["4. close"] '
# However, realize the '["2019-06-14"]' is anchored and will be irrelevant tomorrow! so replace that as variable
# Set a variable to dynamic function  
# ' parsed_response["Time Series (Daily)"].keys() ' to find the dictionary keys of 'Time series Daily'
# Convert the Time series Daily' dictionary keys into a list so we can do as simply do current_date[0] to pull the first date
# With this variable now configured, we can now simply copy paste each of the following ranging from
    # a) most_recent_close 
    # b) most_recent_high
    # c) most_recent_low


# Recommendation will entail % change from high and whether it exceeds a certain % amount.  Use conditional if then statement



# breakpoint()



csv_file_path = os.path.join(os.path.dirname(__file__), "data", "prices.csv") # a relative filepath
#prior examples had ".." --> this means go above one directory.  since app file is not in a separate folder, no need for ".."



with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    
    csv_headers = ["TimeStamp", "Open", "High", "Low", "Close", "Volume"]
    writer = csv.DictWriter(csv_file, fieldnames = csv_headers)
    writer.writeheader() # uses fieldnames set above
   
    for date in dates_list:
        daily_performance = parsed_response["Time Series (Daily)"][date]

        writer.writerow({
        "TimeStamp": date, 
        "Open": daily_performance["1. open"], 
        "High": daily_performance["2. high"], 
        "Low": daily_performance["3. low"], 
        "Close": daily_performance["4. close"], 
        "Volume": daily_performance["5. volume"] 
        
        })




# 
#  INFO OUTPUTS
# 



print("-------------------------")
print(f"SELECTED SYMBOL: {traded_stock_ticker}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:", date_time)
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {usd_format(float(most_recent_close))}") # a float() is necessary to convert a string to a float, otherwise error
print(f"RECENT HIGH: {usd_format(float(most_recent_high))}")
print(f"RECENT LOW: {usd_format(float(most_recent_low))}")
print(f"VOLUMES TRADED: {int(most_recent_total_volumes_traded)}") #switch this portion to int() since no such thing as fraction of share...
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("DATA STORED TO .CSV FILE")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


