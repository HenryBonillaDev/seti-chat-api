import re

PROHIBITED_WORDS = {"mala", "groseria", "spam"}

def is_inappropriate_content(text: str) -> bool:
    words = re.findall(r'\b\w+\b', text.lower())
    return any(word in PROHIBITED_WORDS for word in words)