cp /home/frox/school/thesis/nodejs/bigmon/backend . -r
cp /home/frox/school/thesis/nodejs/bigmon/frontend . -r
docker build -t mediation-monitoring .
docker tag mediation-monitoring udrzalv/mediation-monitoring:latest
docker push udrzalv/mediation-monitoring    