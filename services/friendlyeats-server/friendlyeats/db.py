from google.cloud import firestore
from friendlyeats.settings import PROJECT_ID

db = firestore.Client(project=PROJECT_ID)
