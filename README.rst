# Data Quirrel

# Installation


`pip install datasquirrel`

# Usage

Something along the lines of:
```
from datasquirrel import luno
from datasquirrel import btcc
import time

start = time.time()-(24*3600*404)

collector = luno.Collector()
collector.new_collection(start) # For new collection
collector.collect() # To continue where last one left off

collector = btcc.Collector()
collector.new_collection(start) # For new collection
collector.collect() # To continue where last one left off
```

# To Do

-   Write a better readme
-   Tests for some of the newly added endpoints
-   Tests for the rate limiter
