# Backend Code

# Document
https://docs.google.com/document/d/1FWC9HWRoB5Ia_0YNdqSbt8eS1ruDl6vkuyTW_db_hHE/

## Use your own google cloud key for dialogflow

### regist a google cloud account
Step by step according to the official document:
https://cloud.google.com/dialogflow/es/docs/quick/setup 

### creact your own dialogflow
creact and import your own dialogflow agent.

The trained agent data is in `../algorithms/dialogflow_agent.zip`;

Please import to get a trained agent.

### export the public keys to use the dialogflow
export your own key and download it.

change the keypath in `./app.py` file.

# Install

> cd backend

> pip install -r requirements.txt (py version 3.6)

> export FLASK_APP=app 

> flask run

