import requests
import json


# API key used to connect to API Call.
api_key = '8e30431e1ff6c195669623febad87f2f'

# API URL used to call public OpenWeatherMap API.
api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key

print('This application provides a 5 day weather forecast using OpenWeatherMaps API!')

# Variable used to loop through condition statement
running = True

# Program loop
while running:

    # Asks the user for the city or zip code to be queried
    while True:

        # Input validation
        try:
            print('\nDo you have a city you would like to search? Type "Y" for Yes or type "N" for No')
            search = str(input('Please input Y or N: '))
        except ValueError:
            print("Sorry, I didn't understand that.")
        else:

            # Passed the validation test
            if search == 'Y':

                city = input('Please input the city name: ')
                if city.lower() == 'sf':
                    city = 'San Francisco, US'

                # Appends the city to the api call
                api_call += '&q=' + city
                break

            elif search == 'N':
                print('\nThank you for using the OpenWeatherMap application!')
                running = False
                break

    # Stores the Json response
    json_data: object = requests.get(api_call).json()

    location_data = {
        'city': json_data['city']['name'],
        'country': json_data['city']['country']
    }

    print('\n{city}, {country}'.format(**location_data))

    # The current date we are iterating through
    current_date = ''

    # Iterates through the array of dictionaries named list in json_data
    for item in json_data['list']:

        # Time of the weather data received, partitioned into 3 hour blocks
        time = item['dt_txt']

        # Split the time into date and hour [2018-04-15 06:00:00]
        next_date, hour = time.split(' ')

        # Stores the current date and prints it once
        if current_date != next_date:
            current_date = next_date
            year, month, day = current_date.split('-')
            date = {'y': year, 'm': month, 'd': day}
            print('\n{m}/{d}/{y}'.format(**date))

        # Grabs the first 2 integers from our HH:MM:SS string to get the hours
        hour = int(hour[:2])

        # Sets the AM (ante meridiem) or PM (post meridiem) period
        if hour < 12:
            if hour == 0:
                hour = 12
            meridiem = 'AM'
        else:
            if hour > 12:
                hour -= 12
            meridiem = 'PM'

        # Prints the hours [HH:MM AM/PM]
        print('\n%i:00 %s' % (hour, meridiem))

        # Temperature is measured in Kelvin
        temperature = item['main']['temp']

        # Weather condition
        description = item['weather'][0]['description'],

        weather_data = {
         'city': json_data['city']['name'],
         'country': json_data['city']['country'],
         'temperature': item['main']['temp'],
         'description': item['weather'][0]['description'],
         'time': item['dt_txt']
          }

        # Save the weather_data json dictionary to a json file called 'weatherdata.json'
        with open('weatherdata.json', 'w') as fp:
            json.dump(weather_data, fp)

        # Prints the description as well as the temperature in Celcius and Farenheit
        print('Weather condition: %s' % description)
        print('Celcius: {:.2f}'.format(temperature - 273.15))
        print('Farenheit: %.2f' % (temperature * 9 / 5 - 459.67))

        # AWS S3 Transfer
        # import logging
        import boto3
        # from botocore.exceptions import ClientError
        import os
        import json

    AWS_S3_BUCKET = os.getenv("pyweather-data")
    AWS_ACCESS_KEY_ID = os.getenv("AKIARTGTKUKDDOHY6OET")
    AWS_SECRET_ACCESS_KEY = os.getenv("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")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # Get the s3 object
    s3 = boto3.client('s3')

    # Uploads the 'weatherdata.json' to the 'pyweather-data' s3 bucket and saving the file as 'weather_daily_table'
    s3.upload_file('weatherdata.json', 'pyweather-data', 'weather_daily_table.json')

    # Stores the weather_data python dictonary object as JSON in S3 Bucket
    serializedMyData = json.dumps(weather_data)

    s3.put_object(Bucket='pyweather-data', Key='AKIARTGTKUKDLL22ZV2B')
