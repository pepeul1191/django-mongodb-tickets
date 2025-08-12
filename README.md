# Gestión de Tickets con MongoDB y DJango

Congiruación de amibente para desarrollar:

    $ npm install
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.tx
    $ npm run dev

Crear backup de la base de datos MongoDB:

    $ sudo mongodump --db tickes_master --out db/

Restaurar backup de la base de datos MongoDB:

    $ sudo mongorestore --db tickes_master db/tickes_master

.env

    MONGO_DB_NAME=tickets_master
    MONGO_HOST=mongodb://localhost:27017/
    MONGO_USER=usuario_mongo
    MONGO_PASS=contraseña_segura
    MONGO_AUTH_SOURCE=admin