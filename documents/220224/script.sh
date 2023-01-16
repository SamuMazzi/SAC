#!/bin/bash
# (return 0 2>/dev/null) && SOURCED=1 || SOURCED=0
# if [ $SOURCED == 0 ]
# then 
#	echo "must execute with \" source $0\""
# fi

# curl  -H "Content-Type: application/json" -d "$(cat mockPayload.json)" http://localhost:8080/api/v1/slot/2
source ./env/bin/activate
# . env/bin/activate on Mac

PROJECT_ID="es220224sm"
export PROJECT_ID=$PROJECT_ID
gcloud projects create ${PROJECT_ID} --set-as-default
gcloud app create --project=$PROJECT_ID --region=europe-west3
touch .gcloudignore
echo ".gcloudignore
.git
.gitignore
__pycache__/
env/
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
export TOPIC_IRR="irrigazione"
export SUB_IRR="irrigazione"
export TOPIC_UMI="umidita"
export SUB_UMI="umidita"

gcloud pubsub topics create ${TOPIC_IRR}
gcloud pubsub subscriptions create ${SUB_IRR} --topic ${TOPIC_IRR}
gcloud pubsub topics create ${TOPIC_UMI}
gcloud pubsub subscriptions create ${SUB_UMI} --topic ${TOPIC_UMI}