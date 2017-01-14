#!/bin/bash


cd backend
nodemon server.js &
cd ..

cd frontend
npm start
