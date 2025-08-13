from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import string

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tickets_master']
collection = db['assets']

# Nombres de activos tecnológicos
NOMBRES_COMPUTACION = [
    "Servidor Web", "Base de Datos", "API Gateway", 
    "Microservicio de Usuarios", "Sistema de Cache",
    "Balanceador de Carga", "Servidor de Archivos"
]

def generar_codigo_aleatorio():
    """Genera código alfanumérico de 5-20 caracteres"""
    longitud = random.randint(5, 20)
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(longitud))

def generar_descripcion_simple(nombre):
    """Genera un párrafo simple en markdown"""
    descripciones = [
        f"El {nombre} es un componente crítico de nuestra infraestructura tecnológica que actualmente se encuentra en versión {random.randint(1, 10)}.{random.randint(0, 9)}.",
        f"Este {nombre} proporciona servicios esenciales para las operaciones diarias, con una disponibilidad del {random.randint(95, 100)}%.",
        f"Implementación del {nombre} realizada en {random.choice(['AWS', 'Azure', 'Google Cloud'])} usando {random.choice(['Terraform', 'Kubernetes', 'Docker'])}.",
        f"El {nombre} fue configurado para manejar aproximadamente {random.randint(100, 10000)} peticiones por segundo."
    ]
    return random.choice(descripciones)

def generar_assets(n):
    assets = []
    for _ in range(n):
        now = datetime.utcnow()
        created_date = now - timedelta(days=random.randint(0, 365))
        
        nombre = random.choice(NOMBRES_COMPUTACION)
        
        asset = {
            "name": nombre,
            "code": generar_codigo_aleatorio(),
            "description": generar_descripcion_simple(nombre),
            "documents": [],
            "created": created_date,
            "updated": now
        }
        assets.append(asset)
    return assets

# Generar e insertar 5 assets
try:
    assets_data = generar_assets(317)
    result = collection.insert_many(assets_data)
    
    print(f"✅ {len(result.inserted_ids)} assets insertados")
    print("\nEjemplo de documento:")
    print({
        "name": assets_data[0]["name"],
        "code": assets_data[0]["code"],
        "description": assets_data[0]["description"],
        "created": assets_data[0]["created"].isoformat() + "Z",
        "updated": assets_data[0]["updated"].isoformat() + "Z"
    })
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    client.close()