#!/bin/bash
# (return 0 2>/dev/null) && SOURCED=1 || SOURCED=0
# if [ $SOURCED == 0 ]
# then 
#	echo "must execute with \" source $0\""
# fi

# curl  -H "Content-Type: application/json" -d "$(cat mockPayload.json)" http://localhost:8080/api/v1/slot/2
source ./env/bin/activate
# . env/bin/activate on Mac

PROJECT_ID="es1320222105sm"
export PROJECT_ID=$PROJECT_ID
gcloud project create ${PROJECT_ID} --set-as-default
gcloud app create --project=$PROJECT_ID --region=europe-west3
touch .gcloudignore
echo ".gcloudignore
.git
.gitignore
__pycache__/
env/
/setup.cfg
credentials.json" > .gcloudignore

echo "runtime: python39
handlers:
- url: /.*
  secure: always
  script: auto" > app.yaml

echo "runtime: python39
service: api
entrypoint: gunicorn api:app
handlers:
  - url: /.*
    secure: always
    script: auto" > api.yaml

source ./create_user.sh

# Pub/Sub
export TOPIC="cpu_temperature"
