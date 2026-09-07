from django.conf import settings
from django.db import models

from tasks.models import Task


class Notification(models.Model):
    class Type(models.TextChoices):
        DUE_DATE_PASSED = 'due_date_passed', 'Due date passed'
        REASSIGNED = 'reassigned', 'Task reassigned'

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    notification_type = models.CharField(max_length=30, choices=Type.choices)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.notification_type}] {self.task.title} -> {self.recipient.username}"