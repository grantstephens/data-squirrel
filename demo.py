from datasquirrel import luno
from datasquirrel import btcc
import time

start = time.time()-(24*3600*404)

collector = luno.Collector()
try:
    collector.new_collection(start)
except:
    collector.collect()

collector = btcc.Collector()
try:
    collector.new_collection(start)
except:
    collector.collect()
