from multiprocessing import cpu_count



# Socket Path

bind = 'unix:/home/hope/Documents/Projects/Python_Project/buchi_app_fastapi/env/bin/buchi_app.sock'



# Worker Options    

workers = cpu_count() + 1

worker_class = 'uvicorn.workers.UvicornWorker'



# Logging Options

loglevel = 'debug'

accesslog = '/home/hope/Documents/Projects/Python_Project/buchi_app_fastapi/access_log'

errorlog =  '/home/hope/Documents/Projects/Python_Project/buchi_app_fastapi/error_log'
