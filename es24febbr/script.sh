#!/bin/bash
# (return 0 2>/dev/null) && SOURCED=1 || SOURCED=0
# if [ $SOURCED == 0 ]
# then 
#	echo "must execute with \" source $0\""
# fi

# curl  -H "Content-Type: application/json" -d "$(cat mockPayload.json)" http://localhost:8080/api/v1/slot/2
source ./env/bin/activate
# . env/bin/activate on Mac
# gcloud app deploy

PROJECT_ID="es2febbra2022sm"
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

source ./create_user.sh

# Pub/Sub
export TOPIC="cpu_temperature"
export TOKEN="123token"
export SUBSCRIPTION_NAME="cpu_alert_sub"
export TOPIC2="cpu_temperature_alert"
