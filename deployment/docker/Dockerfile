FROM python:3.5-slim
RUN apt-get update
RUN apt-get install screen
RUN apt-get --assume-yes install python2.7
RUN apt-get --assume-yes install python-pip
RUN pip2 install supervisor
RUN apt-get --assume-yes install nodejs
RUN apt-get --assume-yes install npm
RUN npm install express
EXPOSE 27017 28017
VOLUME /data/db
ENV appDir /home/app
RUN mkdir ${appDir}
WORKDIR ${appDir}

ADD mongodb-linux-x86_64-debian81-3.4.1.tar mongodb
ADD defaultRequirements.txt .
RUN pip3 install -r ${appDir}/defaultRequirements.txt
ADD backend backend
RUN pip3 install -r ${appDir}/backend/requirements.txt
ADD frontend frontend
ADD supervisor.conf supervisor.conf
EXPOSE 5000 9000 9001
RUN mkdir -p log
CMD supervisord -c ${appDir}/supervisor.conf