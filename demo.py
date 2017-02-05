from datasquirrel import luno
import time

start = time.time()-3600
collector = luno.LunoCollector()
collector.new_collection(start)
