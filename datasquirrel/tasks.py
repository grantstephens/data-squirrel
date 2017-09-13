import logging
import time

from celery import Celery

from .squirrel import Squirrel

app = Celery()


logger = logging.getLogger(__name__)

@app.task()
def forrage(**kwargs):
    logger.debug('Data-Squirrel task started')
    squirrel = Squirrel(**kwargs)
    # squirrel.forrage()
    logger.debug('Data-Squirrel task finished')
