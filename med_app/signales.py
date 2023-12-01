from django.db.models.signals import post_save
from django.dispatch import receiver

from med_app.models import MeetingRoom
from med_app.utils import generate_room_code


@receiver(post_save, sender=MeetingRoom)
def generate_meet_code(sender, instance, created, **kwargs):
    if created:
        instance.meet_code = generate_room_code()
        instance.save()
