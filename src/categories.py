"""Allowed lead categories for MVP."""

CATEGORIES = [
    "Металлообработка",
    "Производственные компании",
    "Строительные компании",
    "Оптовая торговля",
    "Грузоперевозки",
    "Склады",
    "Автосервисы",
    "Юридические компании",
    "Бухгалтерские услуги",
    "Медицинские центры",
]


def list_categories() -> list[str]:
    return CATEGORIES


def validate_category(category: str) -> str:
    if category not in CATEGORIES:
        allowed = ", ".join(CATEGORIES)
        raise ValueError(f"Unknown category: {category}. Allowed categories: {allowed}")
    return category
