# nasanomics
code challenge for integrating data from two different APIs

---
### Instructions:
* hit [data.nasa.gov](https://data.nasa.gov/view/ak9y-cwf9) and [beta.data.worldbank.org](http://data.worldbank.org/indicator/IP.JRN.ARTC.SC/countries?display=default)
    - *do not* download any datasets
* only look at data from 2008 - 2010
* use the data to answer the questions
    - use other APIs if necessary
    - answers should be in the following format:

> Q: How many records are in the dataset? 
> A: 45,716

* ignoring irrelevant data is okay (for now..)
* use Python 3 and any libraries you feel are of use

---
### Usage:
* clone the repo
* run `make venv` (to create the virtualenv)
* activate the virtual env (e.g. `source venv/bin/activate`)
* run `make install`
* run `make dev-server` to demo on your machine
    - if you have any secrets, put them in a `.env` file at the project root like so:
        - `NASA_APP_TOKEN=thisisanapptoken...`
        - `NASA_SECRET_TOKEN=thisisasecret...`
    - be sure you have a redis instance up and running (e.g. `$ redis-server`)
    - `make shell` to sandbox ideas
    - travelling to the `/questions` endpoint will show all questions
    - travelling to the `/answers/<year>` will show pertinent data
* run `make dev-deploy` to demo on a debian/jessie64 box
    - nginx fields http requests and forwards them to a uwsgi app server hosting a Flask app
    - go to `localhost:8080` to access the app
    - `make clean` gets rid of everything
    - `vagrant ssh` to poke around the VPS, but you shouldn't need to :)
