import requests 
import smtplib
import json
from datetime import datetime,date,timedelta,timezone
import serpapi
import os

today = date.today()

week_advance = today + timedelta(days=7)

week_advance = week_advance.strftime('%Y-%m-%d')
#DATE INFO ABOVE---------------------------

flight_sheet_url = 'https://api.sheety.co/c7219a9b12f3686568f50141d3a6cefa/flightTracker/sheet1'
flight_sheet_header = {'Authorization' :os.environ['SHEETY_FLIGHTS']}

flights_list = []

flight_sheet = requests.get(url=flight_sheet_url,headers = flight_sheet_header)

sheet_json_data = flight_sheet.json()

flight_num = 1
for flight in sheet_json_data['sheet1']:
  flights_list.append(flight)



#IMPORT SHEETY API



#print(results['best_flights'][0].keys())
#print('\n')
#print(results['search_metadata']['google_flights_url'])



counter = 0

def compare_prices ():
  global flights_list
  global week_advance
  

  func_flights_list = []

  for flight_test in flights_list:
    client = serpapi.Client(api_key=os.environ['SERP_API_KEY'])
    flight_results = client.search({
    
        "engine": "google_flights",
        "currency": "USD",
        "type": "2",
        "outbound_date":week_advance ,
        "departure_id": "MEX",
        "arrival_id": flight_test['arrivalId'],
        'deep_search' : True

      })

    

    try:
      if flight_results['best_flights'][0]['price'] < flight_test['price']:
       

        # 1. Set credentials and details
        sender = "kryptowarrior1@gmail.com"
        password = os.environ['FLIGHT_GOOGLE_CREATED_KEY']  # Generated from account settings
        receiver = os.environ['PERSONAL_EMAIL']

        # 2. Format a raw message string (Subject must be separated by two blank lines)
        message = f"flights for {flight_test['plaintextName']} are cheap -> {flight_results['search_metadata']['google_flights_url']}"

        # 3. Connect, secure, login, and send
        with smtplib.SMTP("smpt.gmail.com", 587) as server:
            server.starttls()  # Makes the connection secure
            server.login(sender, password)
            server.sendmail(sender, receiver, message)




      else:
        print('not cheap rn',flight_results['best_flights'][0]['price'],flight_test['price'],flight_test['arrivalId'])
        print('--------------------------------------------------------------')


      

    except KeyError:
      print('data not avaliable for ->',flight_test['arrivalId'])
      print('------------------------------------------------------------------------------------------------------------')
      print('\n')

    


print(compare_prices())


#GET PRICE       print(flight_results['best_flights'][0]['price'])
#GET COUNTRY       print(flight_results['search_parameters']['arrival_id'])


