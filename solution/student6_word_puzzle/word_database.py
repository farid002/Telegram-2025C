"""
Söz bazası - müxtəlif sözlər
"""
WORDS_DATABASE = [
    # Asan sözlər
    "alma", "kitab", "ev", "gül", "su", "gün", "ay", "qələm", "masa", "stul",
    "qapı", "pəncərə", "dost", "ana", "ata", "bacı", "qardaş", "uşaq", "böyük", "kiçik",
    
    # Orta sözlər
    "kompyuter", "proqramlaşdırma", "telefon", "internet", "məlumat", "verilənlər", "sistem", "aplikasiya",
    "müəllim", "tələbə", "məktəb", "universitet", "təhsil", "elm", "riyaziyyat", "fizika",
    "şəhər", "kənd", "ölkə", "dünya", "planet", "kainat", "təbiət", "heyvan",
    
    # Çətin sözlər
    "alqoritm", "verilənlər bazası", "proqramlaşdırma dili", "operasiya sistemi", "şəbəkə protokolu",
    "kriptoqrafiya", "süni intellekt", "maşın öyrənməsi", "neural şəbəkə", "big data",
    "mikroprosessor", "qrafik prosessor", "operativ yaddaş", "sabit disk", "ssd",
    "axtarış alqoritmi", "sıralama alqoritmi", "ağac strukturu", "qraf nəzəriyyəsi"
]


def get_words_by_length(min_length=None, max_length=None):
    """Uzunluğa görə sözləri qaytarır"""
    words = WORDS_DATABASE
    
    if min_length:
        words = [w for w in words if len(w) >= min_length]
    if max_length:
        words = [w for w in words if len(w) <= max_length]
    
    return words


def get_random_word(min_length=None, max_length=None):
    """Təsadüfi söz qaytarır"""
    import random
    words = get_words_by_length(min_length, max_length)
    return random.choice(words) if words else None


def is_valid_word(word):
    """Sözün etibarlı olub olmadığını yoxlayır"""
    return word.lower() in [w.lower() for w in WORDS_DATABASE]