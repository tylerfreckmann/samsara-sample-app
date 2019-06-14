    Samsara Developer Example

Samsara Location API Sample Application
=======================================

This example walks through how to use the Samsara Location API to query the location of vehicles in your fleet.

Introduction
------------

We'll be writing a [Python](https://www.python.org/) script that will query Samsara for a vehicle's location information and then save that information to a database.

Here's what's covered in this example:

*   [Setup](#setup) will explain the technologies we'll be using.
*   [Overview](#overview) will explain the different location APIs that Samsara has to offer.
*   [Saving the data](#save-data) will show you how to query the APIs and save the data to a database.

The end result of this example can be found on [GitHub](stub). Feel free to reference it at any point if you get stuck along the way!

### Prerequisites

We'll assume that you have some familiarity with Python, but you should be able to follow along even if you're coming from a different programming language. We'll also be using REST APIs to query Samsara. We'll explain the basics of REST APIs below, and feel free to skip that section if you're already familiar.

If you need a quick review of Python, take a look [here](https://wiki.python.org/moin/BeginnersGuide/Programmers). We'll be using the [requests](https://2.python-requests.org/en/master/) library to make the REST API calls.

Setup
-----

Before you start, it will be good to familiarize yourself with the different technologies we'll be using to build the sample app. Feel free to skip any sections if they bore you ;)

### Command line

The command line or command prompt is where you enter commands to control your computer. It's also called a terminal. You can find more information about the command line [for Mac](http://www.macworld.co.uk/feature/mac-software/how-use-terminal-on-mac-3608274/), [for Windows](https://www.quora.com/How-do-I-open-terminal-in-windows), or [for Linux](https://www.howtogeek.com/140679/beginner-geek-how-to-start-using-the-linux-terminal/).

### Python

We'll be using Python 3, which may not be the default version of Python you have on your system. Check to see if you are running Python 3 by running python --version. You should see "Python" and a version number. If not, you can go [here](https://www.python.org/downloads/release/python-373/) to install. After you've installed, re-run python --version to make sure you're running Python 3.

### Code editor

We'll be writing Python files for this application. A code editor will be handy. I use [VS Code](https://code.visualstudio.com/), but feel free to use any code editor of your choice.

### Database

We'll store the location data we query from Samsara in a database. We'll use [SQLite](https://www.sqlite.org/index.html) as the database and [SQLAlchemy](https://www.sqlalchemy.org/) as the Python API to the database. SQLite is an open source, light-weight database that is perfect for a sample app like this. SQLAlchemy is a Python SQL toolkit that allows you to connect to many different types of databases (SQLite among them), so you could potentially use SQLAlchemy to connect to a different type of database that your team uses.

You can find the installation package for SQLite [on this page](https://www.sqlite.org/download.html), and you can install SQLAlchemy by running pip install SQLAlchemy from the command line.

Overview
--------

Now you're ready to get started learning about Samsara's Location APIs!

### Samsara APIs

You can access the Samsara Cloud to through REST APIs to build custom applications with your fleet management data. Samsara has a [developer webpage](https://www.samsara.com/api) that gives an introduction to REST APIs in general and detailed documentation on the Samsara APIs if you'd like to read more. Simply put, REST APIs are ways of accessing and manipulating data on an external service through the internet. You use URLs you point to which data you'd like to interact with and provide parameters for querying or manipulating that data. The data is returned to you in [JSON](http://www.json.org/) format (basically a combination of key-value pairs).

### Accessing the Samsara API

Samsara APIs can be accessed through URLs that look like this:

    https://api.samsara.com/<version>/<endpoint>

To access the APIs, you need an access token is then provided as a query string parameter as part of the URL. [Obtaining API keys](https://www.samsara.com/api#section/Authentication) is available to all Samsara administrators. For this sample app, an API key was provided in the email you received to get to this page.

### Location APIs

We're now ready to submit our first Samsara API!

Using your code editor, open a new file called overview.py, and type in the following code:

    import requests
    url = "https://api.samsara.com/v1/fleet/locations"
    querystring = {"access_token": YOUR_ACCESS_TOKEN}
    response = requests.request("GET", url, headers={}, params=querystring)
    print(response.text)

You can run this file by running python overview.py from the command line.

The response will look something like this:

{"vehicles":\[{"id":212014918388867,"name":"GXA9-2UC-T7H","time":1560540016668,"latitude":37.77327209,"longitude":-122.391486367,"heading":0,"speed":13.148805973116996,"location":"4th Street, San Francisco, CA","onTrip":true,"vin":"","odometerMeters":0}\]}

What happened here?

1.  We imported the Python `requests` module to call REST APIs
2.  We constructed the URL of our very first REST API call to Samsara: `https://api.samsara.com/v1/fleet/locations`.
3.  We formed the `querystring` or parameters for our REST API call. Samsara REST API calls will always require at least the `access_token` as a parameter. We'll see examples of adding more later on.
4.  We submitted at "GET" REST API call to the URL with our parameters using the Python `requests` module. "GET" REST API calls mean querying data from the server. There are other verbs like "POST" and "DELETE" that will manipulate data on the server, but we won't be using them in this sample app.
5.  We received a response.

The API we just called (and all Samsara APIs) are documented on the [developer website](https://www.samsara.com/api), but we'll go over the APIs here.

Let's inspect the response a bit further. The response is JSON, so we can use the `json` Python module to print it out a little prettier. Add the following line to the top of the file:

    import json

and change the last line of the file to

    print(json.dumps(response.json(), indent=2))

Rerun the program from the command line: python overview.py The response should now look something like:

    {
      "vehicles": [
        {
          "id": 212014918388867,
          "name": "GXA9-2UC-T7H",
          "time": 1560541230450,
          "latitude": 37.770485824,
          "longitude": -122.39122901,
          "heading": 0,
          "speed": 23.275665115724166,
          "location": "4th Street, San Francisco, CA",
          "onTrip": true,
          "vin": "",
          "odometerMeters": 0
        }
      ]
    }

We can now see that a list (`[]`) of length 1 of `"vehicles"` was returned. The one vehicle in this list contains a bunch of key-value pairs of location data. We can now use this data to build a custom application, such as plotting the vehicle on a map using the `"latitude"` and `"longitute"` fields.

There's only one vehicle in this list, but there could have been multipe - each with their own set of location information. One piece of information that gets returned about these vehicles is their ID. An ID like this can be used in other APIs to get information specific to a vehicle. For example, let's change our code to get the locations of a specific vehicle between a given start and end time.

First, let's save the vehicle ID to a variable. Add the following lines to the end of your overview.py file to parse the JSON response and save the ID of the first vehicle in the list to the `vehicle_id` variable.

    response_json = response.json()
    list_of_vehicles = response_json["vehicles"]
    first_vehicle = list_of_vehicles[0]
    vehicle_id = first_vehicle["id"]

Then, we can use this `vehicle_id` variable to submit another REST API query specific to that vehicle: Add

    import time

to the top of the file, and add the following the bottom:

    now = int(time.time() * 1000)
    then = now - 15000
    
    url = f"https://api.samsara.com/v1/fleet/vehicles/{vehicle_id}/locations"
    querystring = {"access_token": YOUR_ACCESS_TOKEN, "startMs": str(then), "endMs": str(now)}
    response = requests.request("GET", url, params=querystring)
    print(json.dumps(response.json(), indent=2))

Rerun the program by running python overview.py from the command line. The response will look something like this:

    [
      {
        "latitude": 37.773936252,
        "location": "4th Street, San Francisco, CA",
        "longitude": -122.391450442,
        "speedMilesPerHour": 9.618214626580768,
        "timeMs": 1560543257780
      },
      {
        "latitude": 37.773670955,
        "location": "4th Street, San Francisco, CA",
        "longitude": -122.391535277,
        "speedMilesPerHour": 13.148805973116996,
        "timeMs": 1560543264785
      },
      {
        "latitude": 37.773355198,
        "location": "Long Bridge Street, San Francisco, CA",
        "longitude": -122.391496558,
        "speedMilesPerHour": 13.148805973116996,
        "timeMs": 1560543270787
      }
    ]

Let's talk about what happened here. First, let's take a look at the new URL for the new REST API we called. You'll notice we have the `vehicle_id` variable squashed in there. We used [Python string formatting](https://docs.python.org/3.6/reference/lexical_analysis.html#f-strings) to squash the `vehicle_id` variable in the URL for the REST API call.

Let's also take a look at the `querystring`. You'll notice we have two more parameters this time: `startMs` and `endMs`. This is because this REST API queries for all locations of a particular vehicle between a start and an end time (`startMs` and `endMs`). The parameters are passed in as Unix millisecond timestamps, which is why we have the bit of code to calculate `now` and `then` (`now` is 15 seconds after `then`). These were calculated as integer values, but only strings can be passed into the `querystring` using the `requests` module, so we cast the integers to strings using `str()`.

Finally, the response we receive back is another JSON list of location data. This time, however, each item in the list is concerning the vehicle whose ID we passed into the REST API URL. Each item is location data for the vehicle every 5 seconds.

All of this is documented in the [developer website](https://www.samsara.com/api), such as what parameters this API is expecting and the data it returns.

Saving the data
---------------

When saving the location data to a database, let's use a different Samsara API to actually save the location data of all our vehicles between a certain start and end time.

Open a new file called save\_locations.py and type in the following code:

    import requests
    import json
    import time
    
    url = "https://api.samsara.com/v1/fleet/vehicles/locations"
    
    now = int(time.time() * 1000)
    then = now - 15000
    
    querystring = {"access_token": YOUR_ACCESS_TOKEN, "startMs": str(then), "endMs": str(now)}
    response = requests.request("GET", url, params=querystring)
    print(json.dumps(response.json(), indent=2))
    

Run the program with python save\_locations.py. The response will look familiar:

    [
      {
        "id": 212014918388867,
        "locations": [
          {
            "latitude": 37.772165081,
            "location": "4th Street, San Francisco, CA",
            "longitude": -122.391370425,
            "speedMilesPerHour": 19.869357949574482,
            "timeMs": 1560545598645
          },
          {
            "latitude": 37.7725639,
            "location": "4th Street, San Francisco, CA",
            "longitude": -122.391402451,
            "speedMilesPerHour": 19.869357949574482,
            "timeMs": 1560545603649
          },
          {
            "latitude": 37.772850553,
            "location": "4th Street, San Francisco, CA",
            "longitude": -122.391434677,
            "speedMilesPerHour": 13.148805973116996,
            "timeMs": 1560545608654
          },
          {
            "latitude": 37.773166311,
            "location": "4th Street, San Francisco, CA",
            "longitude": -122.391473396,
            "speedMilesPerHour": 13.148805973116996,
            "timeMs": 1560545614655
          }
        ],
        "name": "GXA9-2UC-T7H"
      }
    ]

If we inspect the API we called this time, it is very similar to the `/fleet/vehicles/{vehicle_id}/locations` API we submitted in our other file, but it lacks the `vehicle_id` variable. This is because this API still queries for location data between a start and end time, but for all vehicles in the fleet. The structure of the JSON response is as follows:

    [
      {
        "id": 0,
        "locations": [...list of location datapoints ...],
        "name": "vehicle-0"
      },
      {
        "id": 1,
        "locations": [...list of location datapoints ...],
        "name": "vehicle-1"
      }
    ]

In this case, we only have one vehicle in our fleet, but this API allows us to get the location data of all our vehicles between a certain start and end time. Hm, maybe we want to save this data? How can we do this?

### Incorporating the database

Now, it has finally come time for us to add the database code to our program. Let's first import SQLAlchemy at the top of our program to be able to talk to the [SQLite database we installed](#databse):

    from sqlalchemy import create_engine
    from sqlalchemy import Table, Column, Integer, Numeric, String, MetaData

Then, after we've retrieved the response from the REST API request, add the following code:

    response = response.json()
    ### Write to database
    engine = create_engine('sqlite:///locations.db')
    metadata = MetaData()
    locations = Table('locations', metadata,
      Column('vehicle_id', Integer, primary_key=True),
      Column('latitude', Numeric),
      Column('location', String),
      Column('longitude', Numeric),
      Column('speedMilesPerHour', Numeric),
      Column('timeMs', Integer, primary_key=True),
      Column('name', String)
    )
    metadata.create_all(engine)
    
    con = engine.connect()
    for vehicle in response:
      vehicle_id = vehicle['id']
      vehicle_name = vehicle['name']
      vehicle_locations = vehicle['locations']
      for location in vehicle_locations:
          con.execute(locations.insert(),
              vehicle_id = vehicle_id,
              latitude = location['latitude'],
              location = location['location'],
              longitude = location['longitude'],
              speedMilesPerHour = location['speedMilesPerHour'],
              timeMs = location['timeMs'],
              name = vehicle_name
          )

As always, you can run the program with python save\_locations.py. The first time you run the program, it will create a file called locations.db in the same directory you ran the program from. This is the SQLite database that gets created through our program. Upon subsequent runs of the program, SQLAlchemy will see that the database and locations table already exists and just add to it. (Simple right!?) We can verify that we've written our location data to the database by using the SQLite command-line tool. Run sqlite3 from the command line in the folder your locations.db file is. Then run the following SQL commands to view the table we've created:

    .open locations.db
    select * from locations;

You'll see rows of the table for all the location datapoints of all the vehicles that were returned by the REST API.

The `for` loops in the program are what iterate through the JSON response from the REST API to write the values to the database.
