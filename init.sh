#!/bin/bash


cd backend
npm install
nodemon server.js
cd ..

cd frontend
npm install
webpack
npm start
