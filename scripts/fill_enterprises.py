from faker import Faker
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from bson import ObjectId
import random

# Configuration
fake = Faker('es_ES')  # Spanish locale for Peru
N = 20  # Number of documents to generate
LOCATION_ID = ObjectId('688adcf90893d7636b68974b')  # Fixed location ID

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['tickets_master']
collection = db['enterprises']  # Collection name in lowercase plural

def generate_peruvian_ruc():
    """Generate a valid 11-digit Peruvian RUC"""
    return str(random.randint(10**10, 10**11-1))  # 11 random digits

def generate_enterprises(n):
    enterprises = []
    for _ in range(n):
        # Generate dates in UTC
        created_date = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=timezone.utc)
        updated_date = created_date + timedelta(days=random.randint(0, 365))
        
        enterprise = {
            '_id': ObjectId(),
            'business_name': fake.company(),
            'trade_name': fake.company_suffix(),
            'tax_id': generate_peruvian_ruc(),
            'fiscal_address': fake.address().replace('\n', ', '),
            'location_id': LOCATION_ID,
            'phone': f"9{fake.random_number(digits=8, fix_len=True)}",
            'email': fake.email(domain='empresa.pe'),
            'website': f"https://www.{fake.domain_name()}",
            'image_url': '/enterprise-default.png',
            'assets_ids': [],
            'employees_ids': [],
            'created': created_date,
            'updated': updated_date
        }
        enterprises.append(enterprise)
    return enterprises

# Generate and insert documents
try:
    enterprises_data = generate_enterprises(N)
    result = collection.insert_many(enterprises_data)
    
    print(f"✅ Successfully inserted {len(result.inserted_ids)} enterprises")
    print("Sample document:")
    print({
        k: v for k, v in enterprises_data[0].items() 
        if k not in ['_id', 'location_id', 'created', 'updated']
    } | {
        '_id': str(enterprises_data[0]['_id']),
        'location_id': str(enterprises_data[0]['location_id']),
        'created': enterprises_data[0]['created'].isoformat(),
        'updated': enterprises_data[0]['updated'].isoformat()
    })
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    client.close()