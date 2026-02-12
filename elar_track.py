import os
import time
import queue
import threading

from config import Config
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils.mongoConnection import MongoConnection
from database.mongoClient import MongoDBClient
from src.newspaper import NewSpaperManager
from src.geminiManager import Status_Analyze_NewSpaper, Chache_Status_True_Analyze_Processing, Chache_Status_False_Analyze_Processing

# Конфигурация проектта
config = Config()

class Deep_Handler(FileSystemEventHandler):
    def __init__(self, database, result_queue):
        self.newSpaperManager = NewSpaperManager(database, config.DIR_TMP_FILES)
        self.result_queue = result_queue
        self.cache_count = 0
        super().__init__()
    # Срабатывает при создании файла или папки
    # Метод сработает при любом изменении (создание, удаление, правка)
    def on_created(self, event):
        # Проверяем, что событие — это файл, а не создание новой папки
        if not event.is_directory:
            # Получаем путь к файлу
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            # Фильтруем только PDF
            if file_name.lower().endswith('.pdf'):
                ### Регистрация path .pdf файл
                result_registor = self.newSpaperManager.Register_Newspapers(file_path)
                ### Если регистрация кэш в Базе данных прошло успешно
                if result_registor:
                    ### cache_count добавить + 1 
                    self.cache_count = self.cache_count + 1 
                ### Проверка cache_count если > 1. отправим в другой поток
                if self.cache_count >= 1:
                    self.result_queue.put({
                        "count_cache" : self.cache_count
                    })
                    ### После отправки cache_count = 0
                    self.cache_count = 0


## Поток обработки газы
## Получам База данных
def Deep_Ai_Handler(event_queue, mongoClient):
    print("Рабочий поток запущен || поток для AI")
    newSpaperManager = NewSpaperManager(mongoClient, config.DIR_TMP_FILES)
    mongoDBManager = MongoDBClient(mongoClient)

    ai_status = Status_Analyze_NewSpaper()
    print(ai_status)

    ### Переменный для работы с потоками  
    message_ai = None

    ### Количества КЭШ данный
    counter_cache = 0
    check_status = True
    tmp_cache_data = None

    while True:
        try:
            ### Ожидаем событие из очереди
            message_ai = event_queue.get_nowait()
        except queue.Empty:
            # Если очередь пуста, продолжаем ждать
            pass

        if message_ai != None:
            if "count_cache" in message_ai and message_ai["count_cache"] >= 1:
                counter_cache = newSpaperManager.Get_Count_Cache_Newspapers()
                print(counter_cache)
            message_ai = None
        
        if counter_cache >= 1 and check_status == True and tmp_cache_data == None:
            tmp_cache_data = newSpaperManager.Get_End_Cache_Newspapers()
           
            if tmp_cache_data == None:
                tmp_cache_data = None
                check_status = True
                counter_cache = 0
                continue
            print("11111")
            check_status = False

        
        if tmp_cache_data != None and tmp_cache_data["verification_time"] <= datetime.now() and Status_Analyze_NewSpaper() == True:
            print("if Deep_Ai_Handler")
            
            Chache_Status_False_Analyze_Processing()
            
            newSpaperManager.Get_Data_From_Newspapers(cache_id=tmp_cache_data["_id"], path_pdf_file=tmp_cache_data["newspapers_path"])
            counter_cache = counter_cache - 1

            Chache_Status_True_Analyze_Processing()

            ai_status = True
            tmp_cache_data = None
            check_status = True



# Главный фунция
def main():
    mongoClient = MongoConnection()
    if mongoClient == None:
        return
    
    result_queue = queue.Queue()
    
    ### Создаем обработчик событий watchdog
    event_handler = Deep_Handler(mongoClient, result_queue)
    observer = Observer()
    observer.schedule(event_handler, config.DIR_PDF_FILES, recursive=True)
    # Создаем и запускаем рабочий поток
    deep_ai_handler = threading.Thread(target=Deep_Ai_Handler, args=(result_queue, mongoClient, ),daemon=True)
    deep_ai_handler.start()
    # Запускаем watchdog
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nОстановка...")
        observer.stop()

    observer.join()

    deep_ai_handler.join(timeout=2)
    

if __name__ == "__main__":
    main()

