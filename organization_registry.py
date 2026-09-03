"""Stable organization registry used as the record grouping key."""

ORGANIZATIONS = (
    {"code": "JUNGNANG_WOLGYE_BUREAU", "name": "중랑월계교육국", "type": "교육국"},
    {"code": "WOLGYE_CENTER", "name": "월계 러닝센터", "type": "러닝센터"},
    {"code": "MYEONMOK_CENTER", "name": "면목 러닝센터", "type": "러닝센터"},
    {"code": "SINNAE_CENTER", "name": "신내 러닝센터", "type": "러닝센터"},
    {"code": "GWAGIDAE_CENTER", "name": "과기대 러닝센터", "type": "러닝센터"},
    {"code": "GONGNEUNG_CENTER", "name": "공릉 러닝센터", "type": "러닝센터"},
    {"code": "JUNGNANG_CENTER", "name": "중랑 러닝센터", "type": "러닝센터"},
)

ORGANIZATION_BY_CODE = {item["code"]: item for item in ORGANIZATIONS}


def get_organization(code):
    return ORGANIZATION_BY_CODE.get(code)


def filter_records(records, organization_code):
    """Exclude legacy null-org records and records from other organizations."""
    return [record for record in records or [] if record.get("organization_code") == organization_code]


def validate_organizations():
    if len(ORGANIZATIONS) != 7:
        raise ValueError("조직은 정확히 7개여야 합니다.")
    codes = [item["code"] for item in ORGANIZATIONS]
    names = [item["name"] for item in ORGANIZATIONS]
    if len(set(codes)) != len(codes) or len(set(names)) != len(names):
        raise ValueError("조직 code/name은 중복될 수 없습니다.")
    if any(not item.get("code") or not item.get("name") or not item.get("type") for item in ORGANIZATIONS):
        raise ValueError("조직 code/name/type은 비어 있을 수 없습니다.")
    if len(ORGANIZATION_BY_CODE) != len(ORGANIZATIONS):
        raise ValueError("알 수 없는 조직이 registry에 등록되었습니다.")
    return True


validate_organizations()