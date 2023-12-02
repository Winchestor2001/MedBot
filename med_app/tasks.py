from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.celery import app
from .models import MeetingRoom
from datetime import datetime


@app.task
def check_meet():
    now_time = datetime.now()
    meets = MeetingRoom.objects.all()
