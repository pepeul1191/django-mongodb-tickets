# database.py
from mongoengine import connect
from dotenv import load_dotenv
import os

def init_db():
  load_dotenv()
  connect(
    db=os.getenv("MONGO_DB_NAME"),
    host=os.getenv("MONGO_HOST")
  )