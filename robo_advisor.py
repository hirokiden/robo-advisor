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

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(request_url)

# print(type(response))
# print(response.status_code)
# print(response.text) # This is a string

parsed_response = json.loads(response.text) #this converts string format into dictionary

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

# To find out what the keys are in dictionary format, remember to use command ' parsed_response.keys() '
# Now let's dig a bit deeper, use format ' parsed_response["Meta Data"] ' to find the contents within this key, a.k.a. nested data
# Further inspection of nested data you can use ' parsed_response["Meta Data"]["3. Last Refreshed"] ' --> Last refreshed portion



# breakpoint()





# 
#  INFO OUTPUTS
# 



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")