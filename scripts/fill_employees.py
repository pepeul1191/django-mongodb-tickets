from faker import Faker
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import pytz  # Nueva librería para manejo de timezones

# Configuración
fake = Faker('es_ES')
N = 23  # Cantidad de documentos a generar
DOCUMENT_TYPES = ['DNI', 'CE', 'PAS']  # Solo estos 3 tipos

# Conexión MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tickets_master']
collection = db['employees']

def generar_numero_documento(tipo):
    """Genera número de documento según el tipo"""
    if tipo == 'DNI':
        return str(fake.random_number(digits=8, fix_len=True))  # 8 dígitos
    elif tipo == 'CE':
        return fake.bothify(text='?########').upper()  # Letra + 8 dígitos (Ej: A12345678)
    else:  # PAS
        return fake.bothify(text='??######').upper()  # 2 letras + 6 dígitos (Ej: PA123456)

def generar_empleados(n):
    empleados = []
    for _ in range(n):
        doc_type = random.choice(DOCUMENT_TYPES)
        
        # Generar fechas en UTC explícitamente
        fecha_creacion = fake.date_time_between(start_date='-2y', end_date='now', tzinfo=pytz.UTC)
        fecha_actualizacion = fecha_creacion + timedelta(hours=random.randint(1, 5000))
        
        empleado = {
            "names": fake.first_name(),
            "last_names": f"{fake.last_name()} {fake.last_name()}",
            "document_number": generar_numero_documento(doc_type),
            "document_type": doc_type,
            "phone": f"9{fake.random_number(digits=8, fix_len=True)}",
            "email": fake.email(domain="certus.edu.pe"),
            "user_id": "",
            "image_url": "/user-default.png",
            "created": fecha_creacion,  # Objeto datetime con timezone UTC
            "updated": fecha_actualizacion  # Objeto datetime con timezone UTC
        }
        empleados.append(empleado)
    return empleados

# Generar e insertar
try:
    empleados = generar_empleados(N)
    resultado = collection.insert_many(empleados)
    
    print(f"✅ {len(resultado.inserted_ids)} documentos insertados")
    print("\nEjemplo de documento:")
    print({
        **empleados[0],
        "created": empleados[0]["created"].isoformat(),
        "updated": empleados[0]["updated"].isoformat()
    })
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    client.close()