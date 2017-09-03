# from datasquirrel import btcc
import time

from datasquirrel import btcc, googlefinance, luno

start = time.time()-(24*3600*404)

luno_col = luno.LunoCollector()
# luno_col.new_collection(start)
luno_col.collect()

btcc_col = btcc.BTCCCollector()
# btcc_col.new_collect()
btcc_col.collect()

usdzar_col = googlefinance.GFCollector('USDZAR')
# usdzar_col.new_collect()
usdzar_col.collect()
