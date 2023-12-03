from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.celery import app
from .models import MeetingRoom
from datetime import datetime, timedelta

from .utils import send_message_with_web_app, create_hash
from core.settings import env
import logging

logger = logging.getLogger(__name__)


@shared_task
def check_meet():
    now_time = datetime.now()
    threshold_time = timedelta(minutes=10)

    meets = MeetingRoom.objects.filter(start_meet_date__gte=now_time, start_meet_date__lte=now_time + threshold_time)
    w = None
    logger.info(meets)
    for meet in meets:
        hash_data = create_hash(
            {"doctor": meet.doctor.id, "patient": meet.patient.id, "type": "doctor"}
        )
        webapp_url = f"{env.str('API_URL')}/meeting/{meet.meet_code}/{hash_data}"
        w = webapp_url
        send_message_with_web_app(
            user_id=meet.patient.user.user_id,
            url=webapp_url,
            message="Soon meet start",
        )

    return meets, w
