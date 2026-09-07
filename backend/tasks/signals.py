from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Task


@receiver(pre_save, sender=Task)
def detect_reassignment(sender, instance, **kwargs):
    if not instance.pk:
        # New task being created, not a reassignment.
        return

    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    if old_instance.assignee_id != instance.assignee_id:
        instance._assignee_changed = True
        instance._old_assignee_id = old_instance.assignee_id
    else:
        instance._assignee_changed = False


@receiver(post_save, sender=Task)
def dispatch_reassignment_notification(sender, instance, created, **kwargs):
    if created:
        return  # No notification on initial creation, only reassignment.

    if getattr(instance, '_assignee_changed', False):
        from notifications.tasks import notify_task_reassigned
        notify_task_reassigned.delay(
            task_id=instance.id,
            new_assignee_id=instance.assignee_id,
            old_assignee_id=getattr(instance, '_old_assignee_id', None),
        )