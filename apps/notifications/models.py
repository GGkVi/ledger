from django.db import models


class Notification(models.Model):
    """
    유저에게 보여줄 알림 정보
    Analysis 생성 시 자동으로 생성
    """

    analysis = models.ForeignKey(
        "analysis.Analysis",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
        help_text="어떤 분석 결과로 생성된 알림인지 (없을 수도 있음)",
    )

    message = models.CharField(
        max_length=255,
        help_text="알림 메시지",
    )

    is_read = models.BooleanField(
        default=False,
        help_text="읽음 여부 (사용자가 확인하면 True)",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]
        verbose_name = "알림"
        verbose_name_plural = "알림 목록"

    def __str__(self):
        return f"Notification(id={self.id}, is_read={self.is_read})"
