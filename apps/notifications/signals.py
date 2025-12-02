from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.analysis.models import Analysis
from apps.notifications.models import Notification


@receiver(post_save, sender=Analysis)
def create_analysis_notification(sender, instance, created, **kwargs):
    if not created:
        return  # 생성될 때만 알림 발생

    Notification.objects.create(
        analysis=instance,
        message=f"{instance.period_start} ~ {instance.period_end} 분석이 완료되었습니다.",
        is_read=False,
    )
