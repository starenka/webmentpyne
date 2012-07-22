import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
backlog = 2048
#worker_class ="sync"
worker_class =  "gevent"
debug = True
#daemon = True
pidfile = "app.pid"
logfile = "app.log"
