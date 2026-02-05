"""
Söz bazası - müxtəlif kateqoriyalar və çətinlik səviyyələri
"""
WORDS_DATABASE = {
    "asan": {
        "heyvanlar": ["it", "pişik", "at", "qoyun", "inək", "quş", "balıq", "tülkü", "ayı", "şir"],
        "şəhərlər": ["bakı", "gəncə", "sumqayıt", "lənkəran", "şəki", "qəbələ", "şuşa", "xankəndi", "mərdəkan", "masazır"],
        "meyvələr": ["alma", "armud", "banan", "portağal", "üzüm", "qarpız", "şaftalı", "gilas", "ərik", "nar"],
        "rənglər": ["qırmızı", "mavi", "yaşıl", "sarı", "qara", "ağ", "bənövşəyi", "narıncı", "çəhrayı", "boz"]
    },
    "orta": {
        "heyvanlar": ["fil", "zürafə", "pələng", "aslan", "bəbir", "qartal", "delfin", "kərtənkələ", "timsah", "pələng"],
        "şəhərlər": ["istanbul", "ankara", "moskva", "london", "paris", "berlin", "roma", "madrid", "amsterdam", "praha"],
        "meyvələr": ["ananas", "qreypfrut", "avokado", "kivi", "mango", "papaya", "liçi", "rambutan", "durian", "qovun"],
        "idman": ["futbol", "basketbol", "voleybol", "tennis", "üzgüçülük", "atletika", "güləş", "boks", "karate", "cüdo"]
    },
    "çətin": {
        "heyvanlar": ["hippopotam", "rhinoceros", "chimpanzee", "kangaroo", "penguin", "octopus", "jellyfish", "butterfly", "scorpion", "tarantula"],
        "şəhərlər": ["barcelona", "stockholm", "copenhagen", "brussels", "vienna", "budapest", "warsaw", "athens", "lisbon", "dublin"],
        "elm": ["kimya", "fizika", "riyaziyyat", "biologiya", "astronomiya", "geologiya", "meteorologiya", "psixologiya", "sosiologiya", "filosofiya"],
        "texnologiya": ["kompyuter", "proqramlaşdırma", "alqoritm", "verilənlər bazası", "şəbəkə", "server", "brauzer", "aplikasiya", "platforma", "sistem"]
    }
}


def get_word(difficulty, category):
    """Verilən çətinlik və kateqoriyadan söz qaytarır"""
    import random
    
    if difficulty not in WORDS_DATABASE:
        difficulty = "asan"
    
    if category not in WORDS_DATABASE[difficulty]:
        category = list(WORDS_DATABASE[difficulty].keys())[0]
    
    words = WORDS_DATABASE[difficulty][category]
    return random.choice(words).upper()


def get_categories(difficulty):
    """Verilən çətinlik üçün kateqoriyaları qaytarır"""
    if difficulty not in WORDS_DATABASE:
        return []
    return list(WORDS_DATABASE[difficulty].keys())


def get_difficulties():
    """Bütün çətinlik səviyyələrini qaytarır"""
    return list(WORDS_DATABASE.keys())