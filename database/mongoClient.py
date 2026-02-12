from bson import ObjectId


class MongoDBClient():
    def __init__(self, database):
        self.database = database
    ### ==========================================================================================================================================###
    ### ==========================================================================================================================================###
    ### User могут только админ создать
    def Add_User(self, data):
        try:
            collection = self.database["users"]
            user_id = collection.insert_one(data).inserted_id
            return user_id
        except Exception as e:
            #!
            return None

    def Find_User_By_Id(self, user_id):
        print()
    def Find_User_By_Login(self, user_login):
        try:
            collection = self.database["users"]
            user = collection.find_one({"login" : user_login})
            return user
        except Exception as e:
            return None
    
    def Delete_User(self):
        print("")
    ### Обнавление пароли или пероналный данных
    def Update_User(self):
        print("")
    
    ### ==========================================================================================================================================###
    ### ==========================================================================================================================================###    
    ## ОБРАБОТКА ГЕЗЫ
    ### Добавить получинный данный на База данных
    ### data это у нас JSON | ИНФОР газеты
    def Add_Info_Newspapers(self, data):
        try:
            collection = self.database["newspapers"]
            _ = collection.insert_one(data).inserted_id
            print("true add newspapers !!!")
            return True
        
        except Exception as e:
            # Нужно поставить логер
            return None
    
    
    
    def Get_ByID_Newspapers(self, newspapers_id):
        try:
            collection = self.database["cache_newspapers"]
            newspapers = collection.find_one({"_id" :  ObjectId(newspapers_id)})
            return newspapers
        except Exception as e:
            return None
    

    ### ==========================================================================================================================================###
    ### ==========================================================================================================================================###
    ### Добавить кеш в База данных
    ### Data это кеш | path на файл
    def Add_Cache_NewSpapers(self, data):
        try:
            collection = self.database["cache_newspapers"]

            _ = collection.insert_one(data)
            return True
        
        except Exception as e:
            print(e)
           # Нужно поставить логер
            return None
    ### Получить кеш данных по ID или по PATH файлу
    ### Обычно нужно передать один из двух варианттов. 
    ### Если перевать обе перевенных тогда функция исползует newspapers_id
    ### newspapers_id это ID в База данных
    ### newspapers_path это путь к файлу
    def Get_Cache_NewSpapers(self, newspapers_id="", newspapers_path=""):
        try:
            collection = self.database["cache_newspapers"]
            newspapers = None
            ### Проверить newspapers_id не пустой и строка
            
            if newspapers_id != "" and type(newspapers_id) == str:
                print("if new spaper id")
                newspapers = collection.find_one({"_id" :  ObjectId(newspapers_id)})
                return newspapers
            
            ### Проверить newspapers_path не пустой и строка 
            if newspapers_path != "" and type(newspapers_path) == str:
                print("if new spaper path")
                newspapers = collection.find_one({"newspapers_path" :  newspapers_path})
                return newspapers

            return False
        
        except Exception as e:
            # Нужно поставить логер
            return None
    
    ### Получить кеш данный с конца таблицы
    def Get_Cache_From_End_NewSpapers(self):
        try:
            collection = self.database["cache_newspapers"]
            cache_data = collection.find_one(sort=[("_id", -1)])
            return cache_data
        
        except Exception as e:
            # Нужно поставить логер
            return None
        
    def Get_Count_Cache_NewSpapers(self):
        try:
            collection = self.database["cache_newspapers"]
            count = collection.count_documents({})
            return count
        except Exception as e:
            # Нужно поставить логер
            return None

    ### Удалить кеш данных по ID или по PATH файлу
    ### Обычно нужно передать один из двух варианттов. 
    ### Если перевать обе перевенных тогда функция исползует newspapers_id
    ### newspapers_id это ID в База данных
    ### newspapers_path это путь к файлу
    def Delete_Cache_NewSpapers(self, newspapers_id, newspapers_path=""):
        try:
            collection = self.database["cache_newspapers"]
            print("delete cache path")
            ### Проверить newspapers_id не пустой и строка
            if newspapers_id != "" and isinstance(newspapers_id, ObjectId):
                newspapers = collection.delete_one({"_id" :  ObjectId(newspapers_id)})
                print("delete cache path by ID")
                return True
            ### Проверить newspapers_path не пустой и строка 
            if newspapers_path != "" and type(newspapers_path) == str:
                newspapers = collection.delete_one({"newspapers_path" :  ObjectId(newspapers_path)})
                print("delete cache path by PATH")
                return True
            return False
        
        except Exception as e:
            print("eeee!! database")
            # Нужно поставить логер
            return None