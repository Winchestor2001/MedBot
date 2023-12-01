from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.celery import app
from .models import MeetingRoom


@app.task
def check_meet():
    pass
