# Django houm Docker

This project is a coding test for applying to HOUM.

#CONCEPT
This is the concept to be implemented:

Create a REST API that allows the user to:

- Send Houmer's coordinates from the mobile application to the backend and save it.
- Given a date, returns all the coordinates of the properties that the houmer visited and how long he was in each one. 
- Given a date, returns all times when the Houmer moved from one place to another with a speed greater than a parameter.

#SOLUTION

Explanation of solution:

- A houmer is a person who wants to rent or buy a new house, so, he or she wants to visit some properties for taking a decision.
- 
- The company agent  is the one who is in charge of showing the properties and scheduling visits.
- 
- The houmer opens the app and the app send automatically the coordinates to the endpoint `/api/v1/houm/historical_locations/`
  (POST) this happens each certain time, the params are:
  - `point: -> str, containing the coordinates, example: '11.54466, -76.987633'`
  - the user is taken automatically by the token in serializer
  - the datetime is auto_now_add
  - the speed between the last location and current is automatically calculated and saved, except the first one because there is not a previous location.
- 
- When arriving to the property, the company agent creates the record with the visit of the Houmer and the arrival datetime is auto_now_add,
then, when the houmer finishes the visit, the company agent updates the record with the leaving datetime and the model has a hook which get executed automatically and calculates the elapsed time since the houmer arrives and leaves and save it. 
the `endpoint` used for this is: `/api/v1/houm/visits` (POST for creating) 
  - `id: -> int` of the property
  - `id: -> int` of the houmer (this endpoint is used by the company agent)
  - `optional: leaving_time: str 'YYYY-MM-DD'` (this is sent when the houmer leaves)
  - GET method for retrieving data: `/api/v1/houm/visits/get_data_by_user_and_day`). 
  - params:
    - `date -> str: the date for querying: YYYY-MM-DD`
  
- 
- For getting the moments which in the houmer moved from one place to another to a higher speed than a parameter, the system calculates the speed that took to the houmer arrives to the current property from his last position (which is saved in the Houmer model), then, using `POSTGIS` the system calculates the distance between two coordinates (`PointField`), then gets the time that the houmer spent in the path, then with math the speed is calculated.  this calculations are done while the app sends the locations of the houmer so we don't need to put logic in views and spent time every request. 
  - endpoint `/api/v1/houm/historical_locations/get_data_by_user_and_velocity` (GET)
  - params: 
    - `date: str -> YYYY-MM-DD format`
    - `velocity: float -> speed limit`

#STEPS 

## create superuser

    docker-compose exec backend python3 manage.py createsuperuser
- First, you need to login, using rest-auth, make a `POST` call to `http://localhost:4500/auth/login/` and send params (with the user you created in the previous step):
  - `'username': -> str`
  - `'password': -> str`
  - You will receive a token that you need to include in all the request as an authorization header: `Token + yourtoken`.
- You can even use the endpoints documented in the swagger documentation at `http://localhost:4500` for creating test records,
or you can go to django admin in `http://localhost:4500/admin` and create them.
- You need:
  - create a property
  - create a houmer
  - create a company agent
- at this point you can start 'sending' the locations of the houmer and all the calculation will be done as well as you can use all the functionalities described before in `'SOLUTION'`. In django admin go to `'Houmers historical locations'` and you can list the entries, create, update or delete them, or by using the endpoint with postman.

#RUNNING TESTS
    docker-compose exec backend python3 manage.py test

#THE PROJECT
This is a beautiful Django image simple to configure, run and deploy, it was made with a lot of love and dedication for all human beings who love simple things.

this project contains the next libraries

 - Django==2.2
 - uWSGI==2.0.18
 - asgiref==3.2.7
 - channels==2.4.0
 - django-celery-beat==1.1.1
 - django-celery-results==1.1.0
 - django-cors-headers==3.2.1
 - django-environ==0.4.5
 - django-extensions==2.2.9
 - django-rest-swagger==2.2.
 - djangorestframework==3.11.0
 - djangorestframework-gis==0.15
 - djangorestframework-jwt==1.11.0
 - django-leaflet==0.26.0
 - django-map-widgets==0.3.0
 - djangorestframework-simplejwt==4.4.0
 - psycopg2==2.8.4
 - postgis==1.0.4
 - channels-redis==2.4.2
 - django-rest-knox==4.1.0
 - redis==3.4.1
 - Pillow==7.1.1
 - django-storages==1.9.1
 - boto3==1.12.39  
 - botocore==1.15.39
 - s3transfer==0.3.3
 
and more pretty stuff like
 - Docker compose
 - Postgis 
 - Geo Django
 - Leaflet and Google Maps
 - Celery Worker and Celery Beat
 - Nginx with WebSockets channel support and django static files
 - Static files working fine !
 - AWS S3 Storage
 - Natural structure, **like you weren't using docker**
 - Production deploy steps [click here](https://gist.github.com/jaishirb/ee6d40f5a61610504f5a2bbeeacce2e4)

Simple and beautiful structure

 ![enter image description here](https://i.imgur.com/rUXVwk6.png)

to run  the image follow the next instructions, just for local environment

## Create Environment file

    cp .env_template .env

## build image

    docker-compose build

## up image

    docker-compose up -d 

## create migrations

    docker-compose exec backend python3 manage.py migrate

## restart celery beat

    docker-compose restart beat

## create superuser

    docker-compose exec backend python3 manage.py createsuperuser

## collect statics

    docker-compose exec backend python3 manage.py collectstatic


## Pycharm Support
first, we need to setup the common stuff to active the autocomplete adding the Django Support choosing the manage.py and settings.py files location.

![enter image description here](https://i.imgur.com/yxaLtUc.png)

now we need add the python interpreter what live inside the docker container to the project

Go to preferences and to click in Interpreter then in Project Interpreter and press add

![enter image description here](https://i.imgur.com/DwKsssx.png)

now, do click in Docker, select the image what contains the project name, then write python3 and press ok

![enter image description here](https://i.imgur.com/pI86DZb.png)

press apply and ok, done!.

![enter image description here](https://i.imgur.com/lmpULSQ.png)

now we have configured the interpreter what lives inside our Docker Container in our project

Please, DON'T UPDATE THE DEPENDENCIES ! **unless necessary**

if you wanna deploy this project in production, [go to here](https://gist.github.com/jaishirb/ee6d40f5a61610504f5a2bbeeacce2e4)


**Thanks for using my project, if you need something else, feel you free to contact me**
**jaisirenterprise@gmail.com**