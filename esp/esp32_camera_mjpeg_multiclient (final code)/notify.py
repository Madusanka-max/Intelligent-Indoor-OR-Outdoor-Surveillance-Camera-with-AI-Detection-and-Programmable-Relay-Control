from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from google.cloud import firestore
import requests
import json

# Load your service account credentials
SERVICE_ACCOUNT_FILE = 'camesp32-8d8ed-61129e96bc5e.json'
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

def get_access_token():
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/firebase.messaging'])
    scoped_credentials.refresh(Request())
    return scoped_credentials.token

def send_push_notification(registration_token, title, body):
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    message = {
        "message": {
            "token": registration_token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }
    project_id = 'camesp32-8d8ed'  # Replace with your project ID
    url = f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send'
    response = requests.post(url, headers=headers, json=message)

    print(f'Status Code: {response.status_code}')
    try:
        print(f'Response: {response.json()}')
    except json.JSONDecodeError:
        print(f'Response Content: {response.content}')

# Firestore setup
firestore_client = firestore.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

# Replace with your device registration token
DEVICE_TOKEN = 'eTE5I0fhRmeK5Poy8UZn3w:APA91bFbBNoSLRuh6KqCI29ErxF1IxO7jIGWchfNQH7ePzgBPJy_kz8_DM82IKVL0z0yiIHEmEDSYXzcLnxmK6CQLGwQpkxTxepUci9AqmX7o5bz67ODKKo'

# Define a callback for Firestore document changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        data = doc.to_dict()
        if data.get('con1', False):  # Alert: Intruder detected
            print("Triggering intruder alert notification...")
            send_push_notification(DEVICE_TOKEN, 'System Alert', 'Intruder detected in your home!')
        if data.get('con2', False):  # Alert: Baby not in frame
            print("Triggering baby alert notification...")
            send_push_notification(DEVICE_TOKEN, 'System Alert', 'Baby is not in the frame!')
        if data.get('con3', False):  # Alert: Animal detected
            print("Triggering animal alert notification...")
            send_push_notification(DEVICE_TOKEN, 'System Alert', 'Animal detected in the frame!')

# Listen to the Firestore document
collection_name = 'cam'  # Replace with your collection name
document_name = 'optionsdata'  # Replace with your document name

# Reference to the specific document
doc_ref = firestore_client.collection(collection_name).document(document_name)

doc_watch = doc_ref.on_snapshot(on_snapshot)

print("Listening for changes in Firestore... Press Ctrl+C to stop.")

try:
    while True:
        pass  # Keep the program running
except KeyboardInterrupt:
    doc_watch.unsubscribe()
    print("Stopped listening for changes.")
