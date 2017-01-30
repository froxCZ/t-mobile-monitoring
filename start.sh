#!/bin/bash


cd backend
npm run-script dev &
cd ..

cd frontend
npm start
