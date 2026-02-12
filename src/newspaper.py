import random
from datetime import datetime, timedelta
from database.mongoClient import MongoDBClient
from src.fileManager import FileManager
from src.geminiManager import Status_Analyze_NewSpaper, Analyze_newspaper


class NewSpaperManager:
    def __init__(self, mongoClient, file_tmp_path):
        self.file_manager = FileManager(file_tmp_path)
        self.mongodb = MongoDBClient(mongoClient)
        self.tmp_path = file_tmp_path
        pass
    ## Функция для обработки Гезы
    ### передаеться пут к файлу pdf
    ### path_pdf_file : пут к файлу pdf
    def Get_Data_From_Newspapers(self, cache_id, path_pdf_file):
        print("Get_Data_From_Newspapers")
        print(f"cache_id: {cache_id}")
        status_ai = Status_Analyze_NewSpaper()
        ### Получаем изображение из PDF файла
        ### Каждый страница PDF файла это 1 (одно) файл изображение
        list_img_names = self.file_manager.convertor_pdf_to_png(path_pdf_file)
        print(list_img_names)
        ### Статус записе на База Данных
        write_status = True
        ### Уменшить размер файл изображение
        ### Так как само файл вести > 10МБ. AI сможет только до 10мб файлов обработать
        ### У нас может получиться несколько файлов при умножении их получиться x = n*>10M
        for img_name in list_img_names:
            res_com = self.file_manager.compress_image(f"{self.tmp_path}/{img_name}", f"{self.tmp_path}/{img_name}")
        ### Проверка полученный файл нету ли в кэш Базе Данных 
        ### Что бы при запписе или удаленне из Базы данных не было конфликт
        #is_cache = self.mongodb.Get_Cache_NewSpapers(newspapers_id="", newspapers_path=path_pdf_file)
        
        ### В Ollama есть ограничение на размер файлов: можно отправить не более 10 МБ. 
        ### Если передаваемый файл весит больше 10 МБ, то он передается частично.
        ### Если AI свободен тогда статус TRUE
        if status_ai:
            analyze_data, _ = Analyze_newspaper([f"{self.tmp_path}/{list_img_names[0]}"])

            if analyze_data != False and analyze_data != None:
                write_status = self.mongodb.Add_Info_Newspapers(analyze_data)
                print(f"write_status: ${write_status}")
                ### write_status == True значить данный записалься на База Данных
                ### И можно удалить из КЭШ таблицы
                if write_status:
                    self.mongodb.Delete_Cache_NewSpapers(newspapers_id=cache_id)
                    
            elif analyze_data == False:
                # 
                print()
            elif analyze_data == None:
                # 
                print()
        else:
            write_status = False
        ### Проверка стастус записе на База данных
        ### Если TRUE тогда записалия
        if write_status:
            ### Удалить временный изобретение
            for img_name in list_img_names:
                self.file_manager.delete_file(f"{self.tmp_path}/{img_name}")
    
    
    
    def Get_End_Cache_Newspapers(self):
        cache_data = self.mongodb.Get_Cache_From_End_NewSpapers()
        if cache_data == None:
            return None
        return cache_data

    def Get_Count_Cache_Newspapers(self):
        count = self.mongodb.Get_Count_Cache_NewSpapers()
        if count == None:
            return 0
        return count
    
    def Get_ByID_Newspapers(self, newSpapers_id):
        data = self.mongodb.Get

    ## Регистрация КЭШ
    ### передаеться пут к файлу pdf
    def Register_Newspapers(self, path_pdf_file):
        ### Сперва нужно узнать КЭШ зарегистрировано или нет
        is_cache = self.mongodb.Get_Cache_NewSpapers(newspapers_path=path_pdf_file)
        ### Если не зарегистрировано тогда зарегистрируем
        if is_cache != False:
            print("is_cache")
            ### Запис в Базе Данных
            created_at = datetime.now()
            verification_time = created_at + timedelta(minutes=random.randint(1, 5))

            result_registor = self.mongodb.Add_Cache_NewSpapers({
                "newspapers_path" : path_pdf_file,
                "created_at" : created_at,
                "verification_time" : created_at
            })

            print(result_registor)
            ### Проверка записе в Базе Данных
            if result_registor != False and result_registor != None:
                return True
            ### Если при записе в Базе Данных превзошел ошибка 
            return False
        ### Если при записе в Базе Данных превзошел ошибка 
        ### или данный КЭШ уже зарегистрированый тогда возвращаем ответ FALSE
        return False
