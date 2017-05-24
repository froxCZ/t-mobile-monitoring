# Mediation Monitoring #


### [Video Demo](https://goo.gl/Wg5sQQ) ###

### Tech stack ###

* React + Redux
* Python (Flask)
* MongoDB
* supervisord
* Apache Kafka for messaging

## Mediation system ##
Mediation is a core system of telecommunication provider, where metadata about any activity on any service (SMS, call, internet, ...) are periodically collected, encoded, transformed and sent to other subsequent systems such as billing, fraud detection etc. in appropriate formats. Think Apache Kamel but for telecommunication. If the data are not sent to billing, the services' usages will not get accounted and clients won't be billed (for text messages, calls, ...). It is therefore crucial that the system is working correctly. The mediation system processes data from Germany, Austria, the Netherlands and the Czech Republic. There are over 4500 channels (flows) in the system that must be monitored. 
  
## Monitoring application ##
Data about traffic of each mediation channel is sent to this monitoring application. The application analyses and learns past traffic, detects anomalies and triggers outage alarms in real-time.

### Architecture ###
 The application composes of 4 services.
 * API service communicates with Frontend app and offers API for use by other systems.
 * Monitoring daemon runs in the background and periodically analyses flows.
 * MongoDB stores traffic data as well as configuration of the flows and application in general.
 * Frontend service only provides JS application to the client

![mon_architecture.png](https://bitbucket.org/repo/bGypxq/images/1574827955-mon_architecture.png)


# Manual #
## Requirements ##

- Python3 
- npm
- installed Supervisor 3.2.0 [supervisord.org](supervisord.org)
- globally installed node module `pushstate-server` (or any other server configured for hosting single page apps)
- MongoDB 

## Installing backend ##
- install Python modules `pip3 install -r backend/requirements.txt`
- set database credentials in `config.json`  (you can use `config.json.template`)

## Building frontend ##
- in `frontend` directory run `npm install`
- build frontend with `npm run build`

## Running app ##
- in `deployment/supervisor.conf` set paths to your `backend`, `frontend/build` and MongoDB directories and set log paths
- start by `supervisord -c deployment/supervisor.conf`. It will start MongoDB, monitoring daemon, API service and frontend server
- Monitoring app will be available at port 8080 and Supervisor console at port 9001