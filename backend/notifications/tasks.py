import logging
from django.utils import timezone

from celery import shared_task
from .models import Notification
from tasks.models import Task

logger = logging.getLogger(__name__)


@shared_task
def notify_task_reassigned(task_id, new_assignee_id, old_assignee_id=None):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        logger.warning(f"notify_task_reassigned: task {task_id} no longer exists")
        return

    if not new_assignee_id:
        return

    notification = Notification.objects.create(
        task=task,
        recipient_id=new_assignee_id,
        notification_type=Notification.Type.REASSIGNED,
        message=f"You have been assigned to task '{task.title}'.",
    )
    logger.info(f"Notification created (reassignment): {notification}")


@shared_task
def check_overdue_tasks():
    """
    Periodic sweep (run via Celery Beat): find tasks whose due_date has
    passed, aren't done, and don't already have a due_date_passed
    notification, then create one.

    Simple approach: check for existing notification of this type per task
    to avoid duplicate notifications on every sweep run.
    """
    now = timezone.now()
    overdue_tasks = Task.objects.filter(
        due_date__lt=now,
    ).exclude(status=Task.Status.DONE)

    created_count = 0
    for task in overdue_tasks:
        already_notified = Notification.objects.filter(
            task=task,
            notification_type=Notification.Type.DUE_DATE_PASSED,
        ).exists()

        if already_notified or not task.assignee_id:
            continue

        notification = Notification.objects.create(
            task=task,
            recipient_id=task.assignee_id,
            notification_type=Notification.Type.DUE_DATE_PASSED,
            message=f"Task '{task.title}' is overdue and not marked done.",
        )
        created_count += 1
        logger.info(f"Notification created (overdue): {notification}")

    logger.info(f"check_overdue_tasks: created {created_count} notification(s)")
    return created_count