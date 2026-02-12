from config import Config
from pymongo import MongoClient

conf = Config()

def MongoConnection():
    # Подключаем в база данных MONGODB
    # Создаем клиент для подключения
    mongoClient = MongoClient(
        host = conf.MONGODB_HOST_NAME,
        port = int(conf.MOGODB_PORT),
        username = conf.MONGODB_USER,
        password = conf.MONGODB_PASSWORD
    )

    # Выбираем (или создаем) базу данных
    database = mongoClient[conf.MONGODB_DB_NAME]
    # Проверка подключения MongoDB
    try:
        mongoClient.admin.command("ping")
        return database
    except Exception as e:
        print(e)
        return None
    