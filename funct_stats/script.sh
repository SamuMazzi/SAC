#!/bin/bash
(return 0 2>/dev/null) && SOURCED=1 || SOURCED=0
if [ $SOURCED == 0 ]
then 
	echo "must execute with \" source $0\""
fi

source ./env/bin/activate

export PROJECT_ID="pubsub20222105sm"
export GOOGLE_APPLICATION_CREDENTIALS="${pwd}/credentials.json"

# Pub/Sub
export TOPIC="cpu_temperature"
export TOKEN="123token"
export SUBSCRIPTION_NAME="cpu_alert_sub"
export TOPIC2="cpu_temperature_alert"

# specify region
# gcloud functions deploy update_db --runtime=python39 --trigger-event="providers/cloud.firestore/eventTypes/document.write" --trigger-resource="projects/$PROJECT_ID/databases/(default)/documents/temperature/{day}"