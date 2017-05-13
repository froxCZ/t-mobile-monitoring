# Mediation Monitoring #
### [Video Demo](https://goo.gl/Wg5sQQ) ###
work in progress

### Tech stack ###

* React + Redux
* Python (Flask)
* MongoDB
* supervisord
* Apache Kafka for messaging

## Mediation system ##
Mediation is a core system of T-Mobile where metadata about any activity on any service (SMS, call, internet, ...) are periodically collected, encoded, transformed and sent to other subsequent systems such as billing, fraud detection etc. in appropriate formats. Think Apache Kamel but for telecommunication. If the data are not sent to billing, the services' usages will not get accounted and clients won't be billed (for text messages, calls, ...). It is therefore crucial that the system is working correctly. The mediation system processes data from Germany, Austria, the Netherlands and the Czech Republic. There are over 4500 channels (flows) in the system that must be monitored. 
  
## Monitoring application ##
Data about traffic on each channel is sent to this monitoring application. The application analyses and learns past traffic, detects anomalies and triggers outage alarms.

### Architecture ###
 The application composes of 4 services.
 * API service communicates with Frontend app and offers API for use by other systems.
 * Monitoring daemon runs in the background and periodically analyses flows.
 * MongoDB stores traffic data as well as configuration of the flows and application in general.
 * Frontend service only provides JS application to the client

![mon_architecture.png](https://bitbucket.org/repo/bGypxq/images/1211732785-mon_architecture.png)