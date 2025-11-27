# 이미지 저장 경로
# 인스턴스 뭐 받는지 정확하게 알아두기
def analysis_image_path(instance, filename):
    return f"analysis/{instance.created_at:%Y/%m}/user_{instance.user_id}/{filename}"