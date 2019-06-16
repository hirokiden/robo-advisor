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

import requests
import json # need this to import json string into dictionary
from datetime import datetime #Taken from stackoverflow


# Also, we know that we are working with $ pricing so let's get the formatting out of the way

def usd_format(my_price):
    return "${0:,.2f}".format(my_price) # This UDF will change numerical denomination to currency and cents format when passed through

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

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






# breakpoint()





# 
#  INFO OUTPUTS
# 



print("-------------------------")
print(f"SELECTED SYMBOL: {traded_stock_ticker}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {usd_format(float(most_recent_close))}") # a float() is necessary to convert a string to a float, otherwise error
print(f"RECENT HIGH: {usd_format(float(most_recent_high))}")
print(f"RECENT LOW: {usd_format(float(most_recent_low))}")
print(f"VOLUMES TRADED: {int(most_recent_total_volumes_traded)}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")