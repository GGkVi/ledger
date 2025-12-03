from django.db import migrations

BANK_CODES = [
    ("002", "KDB산업은행"),
    ("003", "IBK기업은행"),
    ("004", "KB국민은행"),
    ("005", "KEB하나은행"),
    ("007", "수협은행"),
    ("011", "NH농협은행"),
    ("020", "우리은행"),
    ("023", "SC은행"),
    ("027", "씨티은행"),
    ("031", "대구은행"),
    ("032", "부산은행"),
    ("034", "광주은행"),
    ("035", "제주은행"),
    ("037", "전북은행"),
    ("039", "경남은행"),
    ("045", "MG새마을금고"),
    ("048", "신협"),
    ("050", "저축은행"),
    ("064", "산림조합"),
    ("071", "우체국"),
    ("081", "하나은행"),
    ("088", "신한은행"),
    ("089", "케이뱅크"),
    ("090", "카카오뱅크"),
    ("092", "토스뱅크"),
    ("103", "SBI저축은행"),
    ("218", "KB증권"),
    ("230", "미래에셋증권"),
    ("238", "미래에셋증권"),
    ("240", "삼성증권"),
    ("243", "한국투자증권"),
    ("247", "NH투자증권"),
    ("261", "교보증권"),
    ("262", "하이투자증권"),
    ("263", "현대차투자증권"),
    ("264", "키움증권"),
    ("265", "이베스트증권"),
    ("266", "SK증권"),
    ("267", "대신증권"),
    ("269", "한화투자증권"),
    ("270", "하나증권"),
    ("271", "토스증권"),
    ("278", "신한투자증권"),
    ("279", "DB금융투자"),
    ("280", "유진투자"),
    ("287", "메리츠증권"),
    ("888", "토스머니"),
    ("889", "토스포인트"),
]


def forwards(apps, schema_editor):
    BankCodes = apps.get_model("accounts", "BankCodes")
    for code, name in BANK_CODES:
        BankCodes.objects.update_or_create(code=code, defaults={"name": name})


def backwards(apps, schema_editor):
    BankCodes = apps.get_model("accounts", "BankCodes")
    for code, _ in BANK_CODES:
        BankCodes.objects.filter(code=code).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
