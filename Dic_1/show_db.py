from pymongo import MongoClient
import time


client = MongoClient('localhost', 27017)
result_db = client.DataStored
cache_db = client.html_cache

result_db_tab = result_db.Data_Store
cache_db_tab = cache_db.ChPage_Cache

while True:
    print 'data_num:   ', result_db_tab.find().count()
    print 'Cache Num:   ', cache_db_tab.find().count()
    time.sleep(5)




