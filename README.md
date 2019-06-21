# robo-advisor Walkthrough README.md

###########################################################################################################################################
1) Getting the basics set up

a) Please run your terminal, select the file, right click/control + click and select 'new terminal at folder', or you can use terminal pathing via:  cd ~/documents/github/app/robo-advisor (note that this is dependent on where you stored your file)

In order to run this robo-advisor script, several packages need to be installed:


conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env

pip install -r requirements.txt
pip install pytest # (only if you'll be writing tests)


b) The command line below will run the script:


python robo_advisor.py


###########################################################################################################################################
2) Ensuring that you import the correct packages

a) To ensure that the script runs correctly, please import the following:


import os
import requests
import json 
from datetime import datetime 
import csv 


b) To briefly explain, os is needed for file pathing, requests and json is necessary to gather data from html and import json string into dictionary. datetime is necessary to acquire the current time.  csv is required to write data to a .csv file for later


###########################################################################################################################################
3) Setting up an .env file and making sure its content will be loaded into script's environment

a) Security is vital so we don't want to have your private API Key show up on your public github repository.  Hence, the the .gitignore component will prevent .env file to show up in the github repository.  Nonetheless, the .env file contents will have to be loaded into the script's environment via the following:


from dotenv import load_dotenv 
import requests

load_dotenv() 


###########################################################################################################################################
4) Gather an API Key from Alphavantage and store it in your .env file

a) In order to pull dynamic, real time stock and financial data, you need to go to https://www.alphavantage.co/support/#api-key to generate your personal API Key.  

set an api_key variable by using the following line:


api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 

b) within the .env file from earlier, include a line script called:

ALPHAVANTAGE_API_KEY="YOUR API KEY"


c) By doing this, you can securely store your private key without worries of others seeing it


###########################################################################################################################################
5) Set up your date and currency formatting to ensure less pain later

a) Since we know that stocks are reliant on date and $xx.xx formatting, we should set formatting up to avoid confusion later

b) The following will ensure that the date you provide or set in script is easy to read and current in real time


date_time = datetime.now().strftime("%m/%d/%Y, %I:%M:%S%P\n") 


c) The following is a UDF that will ensure that 'prices' (could be any other variable) pushed into the formula in $xx.xx format


def usd_format(my_price):
    return "${0:,.2f}".format(my_price) 


###########################################################################################################################################
6) Setting up Validation Step 1 and setting up the user input

a) Inputting a stock ticker is driven through correct user inputs, but there needs to be a simple fail-safe loop that prevents script from proceeding without an approved input.  This can be completed via using a 'while' loop and setting up a series of conditional statements so:

x) tickers that are numbers are invalid (prevents errors such as '88888')
y) tickers that exceed five characters are also invalid (prevents excessive inputs such as 'ABCDEFG')
z) note that user_input_ticker is the variable assigned to the user input


while True:
    user_input_ticker = input()
    

    if user_input_ticker.isdigit() == True: 
        print("Ticker cannot be a number, please try again")
    elif len(user_input_ticker) > 5:
        print("Ticker cannot exceed 5 characters, please try again")
    else:
        break


###########################################################################################################################################
6) Importing data from JSON and creating a Validation Step 2

a) Now that all the packages are imported, the next step is to pull JSON data using a request url and replacing the example url below with the subsequent url.  Then store the requested data 'requests.get()' to 'response' variable.  With this, you can now use the 'json.loads()' syntax to load the 'response' variable that will convert the string format into the proper dictionary format. Store that result under a new variable, which in this case is 'parsed_response'


Example URL FORMAT:
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo
--> Note that 'symbol' is replaced with the {user_input_ticker} and 'demo' is replaced with {api_key}

NEW URL FORMAT:
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={user_input_ticker}&apikey={api_key}"

response = requests.get(request_url)

parsed_response = json.loads(response.text) #this converts string format into dictionary


###########################################################################################################################################
7) Creating a Validation Step 2

a) To prevent an awkward error from poor html connectivity via incorrect/invalid input, we also need to design a fail-safe to gracefully end the script.  This can be achieved via a simply try:, except: clause.  If there is a failure in the JSON Pull, then the script will exit() to prevent error


try: 
    parsed_response["Meta Data"]
except:
    print("Invalid ticker, please rerun the script")
    exit()


###########################################################################################################################################
8) JSON Dictionary to Desired Output

a) Now that JSON components have been imported from the Alphavantage site using API Key and user input, we have to pull relevant data from the dictionary that a user generates (Can be any stock ticker)


The following code completes this process:

a) The dictionary keys from "Time Series (Daily)" is converted to list format


dates_list = list(parsed_response["Time Series (Daily)"].keys()) # convert the dates dictionary keys into list format


b) Then we program the current_date to ensure only the most recent values is pulled, accomplished by dates_list[0] #only first value is pulled


current_date = dates_list[0] 


c) Then you can set variables to pull data of interests, from the ticker, open, close, high, low and volume of most recent trading data


traded_stock_ticker = parsed_response["Meta Data"]["2. Symbol"]

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
most_recent_open = parsed_response["Time Series (Daily)"][current_date]["1. open"]
most_recent_close = parsed_response["Time Series (Daily)"][current_date]["4. close"]
most_recent_high = parsed_response["Time Series (Daily)"][current_date]["2. high"]
most_recent_low = parsed_response["Time Series (Daily)"][current_date]["3. low"]
most_recent_total_volumes_traded = parsed_response["Time Series (Daily)"][current_date]["5. volume"]


###########################################################################################################################################
9) Outputting Historical Stock Details onto a CSV File

We can write a .csv file with trading/stock data when we operate the script by preparing the following:

a) In order to have the aforementioned data printed onto a csv file, we first have to create a .csv file (use the terminal, touch .csv on mac)

Then connect the python script within the 'app' file to the .csv file within the 'data' file via the following code:

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv") # a relative filepath # Translates to 'join with "prices.csv" file located 1) above directory ("..") 2) within "data" file 3) actual file name "prices.csv"




b) Then we set up a 'write' script using the with open(csv_file_path, "w") syntax and then loop repetitions for each header via a 'for date in dates_list' loop function



with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    
    csv_headers = ["TimeStamp", "Open", "High", "Low", "Close", "Volume"] # list out each of the headers via variable
    writer = csv.DictWriter(csv_file, fieldnames = csv_headers)
    writer.writeheader() # uses fieldnames set above
   
    for date in dates_list: # set a loop up for the dates_list, for each date, write out the headers above for each row, repeat until end of page
        daily_performance = parsed_response["Time Series (Daily)"][date]

        writer.writerow({
        "TimeStamp": date, 
        "Open": daily_performance["1. open"], 
        "High": daily_performance["2. high"], 
        "Low": daily_performance["3. low"], 
        "Close": daily_performance["4. close"], 
        "Volume": daily_performance["5. volume"] 
        
        })


###########################################################################################################################################
10) Printing the Desired Results

a) We're almost there!  We can now print out the variables that we have selected from the dictionary earlier on.  Ensure that you pass the float(variables) through the previously defined currency formatter UDF from section 5 (in this case {usd_format(float(variable))} ).  With this, you should be able to print out all the desired variables in correct format.

I've also included a sample % change formula to a variable to document the % change calculations between opening and closing stock prices:


percentage_change_close_vs_open = (float(most_recent_close) - float(most_recent_open))/float(most_recent_open) # custom percentage change function for later

print("-------------------------")
print(f"SELECTED SYMBOL: {traded_stock_ticker}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:", date_time)
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST OPEN: {usd_format(float(most_recent_open))}")
print(f"LATEST CLOSE: {usd_format(float(most_recent_close))}") # a float() is necessary to convert a string to a float, otherwise error
print("% CHANGE FROM OPEN TO CLOSE", "{0:.3%}".format(percentage_change_close_vs_open)) # % replaces f and included 3 digits for precision
print(f"RECENT HIGH: {usd_format(float(most_recent_high))}")
print(f"RECENT LOW: {usd_format(float(most_recent_low))}")
print(f"VOLUMES TRADED: {int(most_recent_total_volumes_traded)}") #switch this portion to int() since no such thing as fraction of share...
print("-------------------------")


###########################################################################################################################################
11) Printing Your Personal Recommendations

a) You can incorporate whatever conditional recommendations you see fit, but I created some variables and my personal risk tolerance levels for % change + recommended moves:


recommendation_sell = "Sell, so you won't lose your shirt...  This stock went down by more than -8%..."

recommendation_buy = "Buy, this stock is potentially a great opportunity...  This stock went up by more than 3%..."

recommendation_hold = "Hold, don't do anything...  This stock is operating with no abrupt changes in price..."


b) The following conditional if, elif statements are incorporated and are printed out, along with statements that show that the .csv file is recorded with stock performance data as well as a final short greeting

if percentage_change_close_vs_open < float(-.08):
    print("RECOMMENDATION:", recommendation_sell)

elif percentage_change_close_vs_open > float(.03):
    print("RECOMMENDATION:", recommendation_buy)

elif percentage_change_close_vs_open > float(-.08) and percentage_change_close_vs_open < float(.03):
    print("RECOMMENDATION:", recommendation_hold)


print("DATA STORED TO .CSV FILE")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


###########################################################################################################################################
11) Final Statement

Hope this was a fun project!  With this set up we should have:

x a) Have a repository README.md that you can review at any time
x b) Have your API Key safely stored in a .env file and properly ignored by a .gitignore file for security/privacy purposes
x c) Validations that prevent an invalid ticker from breaking the script as well as preventing a break down via failed HTTP JSON request
x d) Proper implementation and pulling of accurate, real time data
x e) A sample of some final recommendations and justifications behind them
x f) Historical prices that are properly written to a .csv file
x g) Formatting that is correctly listed in $xx.xx format and date/time stamp that is easy to read
x h) Easy to process repository that shows incremental revision history






Actual Project Requirements:

xRepository	Includes README.md file with detailed instructions	7.5%
xSecurity	Excludes secret API Key values from the source code	12.5%
xValidations (Prelim)	Prevents an HTTP request if stock symbol not likely to be valid (e.g. symbol of "8888")	5%
xValidations	Fails gracefully if encountering a response error (e.g. symbol of "OOPS")	7.5%
xCalculations	Displays accurate information	15%
xInfo Outputs	Displays final recommendation, including justification / context	17.5%
xInfo Outputs	Writes historical prices to CSV file	10%
xInfo Outputs	Formats all prices as USD (doesn't apply to CSV file values)	5%
xDev Process	Submitted via remote Git repository which reflects an incremental revision history	20%

