
import os
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime


env_path = Path(__file__).parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

class DatabaseService:
    """
    Handles persistent storage and retrieval for HealthLens history.
    """
    
    def __init__(self):
        self.uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("MONGODB_DB", "healthlens")
        self.client = None
        self.db = None
        
        if self.uri and "mongodb" in self.uri:
            try:
                self.client = MongoClient(self.uri)
                self.db = self.client[self.db_name]
                print(f"DEBUG: Connected to MongoDB Database: {self.db_name}")
            except Exception as e:
                print(f"DEBUG: MongoDB connection failed: {e}")

    def save_screening(self, user_email, phone, symptoms, result_data):
        if self.db is None:
            return False
            
        try:
            record = {
                "user_email": user_email,
                "phone": phone,
                "timestamp": datetime.utcnow(),
                "timestamp_str": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "symptoms": symptoms,
                "condition": result_data['condition'],
                "urgency": result_data['urgency'],
                "recommendation": result_data['recommendation']
            }
            self.db.screenings.insert_one(record)
            return True
        except Exception as e:
            print(f"DEBUG: MongoDB save error: {e}")
            return False

    def get_recent_screenings(self, limit=10):
        """
        Retrieves the last X screenings from the database.
        """
        if self.db is None:
            
            return [
                {
                    "timestamp_str": "2026-04-02 10:30:15",
                    "user_email": "demo@example.com",
                    "condition": "Dermatitis (Mock)",
                    "urgency": "MODERATE",
                    "symptoms": "Itchy red bumps on arm."
                },
                {
                    "timestamp_str": "2026-04-02 09:12:45",
                    "user_email": "patient_001@atlas.ai",
                    "condition": "Allergy (Mock)",
                    "urgency": "LOW",
                    "symptoms": "Sneezing and itchy eyes."
                }
            ]
            
        try:
            cursor = self.db.screenings.find().sort("timestamp", DESCENDING).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"DEBUG: MongoDB fetch error: {e}")
            return []

database_service = DatabaseService()
