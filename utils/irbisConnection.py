from config import Config
from cbsvibpyirbis import Connection

def iribisConnection():
    # Подключаем в база данных IRBIS
    # Создаем клиент для подключения
    irbisClient = Connection(
        Config.IRBIS_HOST, 
        int(Config.IRBIS_POST), 
        Config.IRBIS_DB_USER, 
        Config.IRBIS_DB_PASSWORD, 
        Config.IRBIS_DB_NAME
    )

    try:
        irbisClient.connect()
        return irbisClient
    
    except Exception as e:
        print(e)
        return None
