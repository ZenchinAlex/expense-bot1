CATEGORIES = {
    "еда": ["кофе", "хлеб", "молоко", "обед", "ужин", "продукты"],
    "машина": ["дизель", "бензин", "мойка", "парковка"],
    "дом": ["свет", "вода", "интернет", "аренда"],
}


def detect_category(title):
    text = title.lower()
    for category, words in CATEGORIES.items():
        for word in words:
            if word in text:
                return category
    return "другое"