# SAC


gcloud project create ${PROJECT_ID} --set-as-default

# gcloud config set project ${PROJECT_ID}

gcloud app create --project=${PROJECT_ID}

---------------
File .gcloudignore
.gcloudignore
.git
.gitignore
__pycache__/
env/
/setup.cfg
credentials.json
---------------

gcloud app deploy
gcloud app browse

gcloud project delete ${PROJECT_ID}

# Credential setup
export NAME=webuser
gcloud iam service-accounts create ${NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/owner"
touch credentials.json
gcloud iam service-accounts keys create credentials.json --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com

(c'è già nello script)
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"

# API
export ENDPOINTS_SERVICE_NAME=$(grep 'host:' ${SERVICE_NAME}.yaml | cut -d : -f2 | sed 's/"//g')
gcloud services enable ${ENDPOINT_SERVICE_NAME}
(validate)
gcloud endpoints services deploy ${SERVICE_NAME}.yaml --validate-only
(deploy)
gcloud endpoints services deploy ${SERVICE_NAME}.yaml

# PubSub
export TOPIC=name_topic
export SUBSCRIPTION_NAME=sub_name
gcloud pubsub topics create ${TOPIC}
(PULL-LOGIC)
gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME} --topic ${TOPIC}

(send message)
gcloud pubsub topics publish testTopic --attribute=from="cli" --message="Test Message"
(receive message)
gcloud pubsub subscriptions pull ${SUBSCRIPTION_NAME}

(push_logic)
gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME} --topic ${TOPIC} --push-endpoint "https://${PROJECT_ID}.appspot.com/pubsub/push?token=${TOKEN}" --ack-deadline 10

# Trigger events
def myFunction(event_data, context)

gcloud functions deploy name_fn --runtime=python39 --trigger-event="providers/cloud.firestore/eventTypes/document.write" --trigger-resource="projects/${PROJECT_ID}/databases/(default)/documents/cars/{car}"

# Test
gcloud functions call ${FUNCTION_NAME} --data '{"name": "Boba"}'


# Info
Lezione 5 dic (b) -> PubSub