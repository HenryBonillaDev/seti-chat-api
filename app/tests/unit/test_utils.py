from app.utils.filter import is_inappropriate_content


def test_filter_inappropriate_content():
    words = [
        "Este es un mensaje limpio",
        "Este mensaje tiene una groseria",
        "Otro mensaje con mala palabra",
        "Este es spam total",
        "Todo bien aquí"
    ]
    count = 0
    for text in words:
        if is_inappropriate_content(text):
            count += 1

    assert count == 3