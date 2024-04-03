from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings

from kafka_producer import KafkaProducerService, EventType

from .models import User


@receiver(post_save, sender=User)
def user_saved(sender, instance: User, created, **kwargs):
    event_type = EventType.USER_CREATED.value if created else EventType.USER_UPDATED.value
    event = {
        'type': event_type,
        'public_id': str(instance.public_id),
        'email': instance.email,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'role': instance.role,
    }
    KafkaProducerService.send_event(settings.KAFKA_TOPIC, event)


@receiver(post_delete, sender=User)
def user_deleted(sender, instance: User, **kwargs):
    event = {
        'type': EventType.USER_DELETED.value,
        'public_id': str(instance.public_id),
    }
    KafkaProducerService.send_event(settings.KAFKA_TOPIC, event)


@receiver(pre_save, sender=User)
def check_role_changed(sender, instance, **kwargs):
    if instance.pk:
        old_user = User.objects.get(pk=instance.pk)
        if old_user.role != instance.role:
            KafkaProducerService.send_event(
                settings.KAFKA_TOPIC,
                {
                    'type': EventType.USER_ROLE_CHANGED.value,
                    "user_id": instance.pk,
                    "old_role": old_user.role,
                    "new_role": instance.role
                 }
            )
