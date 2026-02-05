"""
Viktorina sualları bazası - müxtəlif kateqoriyalar
"""
QUESTIONS_DATABASE = {
    "riyaziyyat": [
        {
            "question": "2 + 2 neçədir?",
            "options": ["3", "4", "5", "6"],
            "correct": 1
        },
        {
            "question": "5 × 5 neçədir?",
            "options": ["20", "25", "30", "35"],
            "correct": 1
        },
        {
            "question": "100-ün kvadrat kökü neçədir?",
            "options": ["8", "9", "10", "11"],
            "correct": 2
        },
        {
            "question": "Bir dairənin sahəsi necə hesablanır?",
            "options": ["πr²", "2πr", "πd", "r²"],
            "correct": 0
        },
        {
            "question": "15-in 20%-i neçədir?",
            "options": ["2", "3", "4", "5"],
            "correct": 1
        }
    ],
    "tarix": [
        {
            "question": "Azərbaycan Respublikası nə vaxt müstəqillik qazanıb?",
            "options": ["1990", "1991", "1992", "1993"],
            "correct": 1
        },
        {
            "question": "İkinci Dünya Müharibəsi nə vaxt başlayıb?",
            "options": ["1937", "1938", "1939", "1940"],
            "correct": 2
        },
        {
            "question": "Bakı neçə ildir paytaxtdır?",
            "options": ["1000+", "500+", "200+", "100+"],
            "correct": 0
        },
        {
            "question": "Azərbaycan Xalq Cümhuriyyəti nə vaxt yaradılıb?",
            "options": ["1917", "1918", "1919", "1920"],
            "correct": 1
        },
        {
            "question": "Qədim Roma İmperiyası nə vaxt dağılıb?",
            "options": ["400-cü il", "476-cı il", "500-cü il", "600-cü il"],
            "correct": 1
        }
    ],
    "elm": [
        {
            "question": "Su neçə dərəcədə qaynayır?",
            "options": ["90°C", "100°C", "110°C", "120°C"],
            "correct": 1
        },
        {
            "question": "Yer planetinin ətrafında fırlanma müddəti neçədir?",
            "options": ["23 saat 56 dəqiqə", "24 saat", "25 saat", "26 saat"],
            "correct": 0
        },
        {
            "question": "H2O nə deməkdir?",
            "options": ["Oksigen", "Hidrogen", "Su", "Karbon dioksid"],
            "correct": 2
        },
        {
            "question": "İnsan qanında neçə qrup var?",
            "options": ["2", "4", "6", "8"],
            "correct": 1
        },
        {
            "question": "Fotosintez prosesində nə istehsal olunur?",
            "options": ["Karbon dioksid", "Oksigen", "Azot", "Hidrogen"],
            "correct": 1
        }
    ],
    "ədəbiyyat": [
        {
            "question": "Nizami Gəncəvi hansı əsərin müəllifidir?",
            "options": ["Leyli və Məcnun", "Xosrov və Şirin", "Hər ikisi", "Heç biri"],
            "correct": 2
        },
        {
            "question": "Şekspirin ən məşhur pyesi hansıdır?",
            "options": ["Hamlet", "Romeo və Culyetta", "Makbet", "Hamısı"],
            "correct": 3
        },
        {
            "question": "Azərbaycanın ən məşhur şairi kimdir?",
            "options": ["Nizami", "Füzuli", "Nəsimi", "Hamısı"],
            "correct": 3
        },
        {
            "question": "Don Quixote kimin əsəridir?",
            "options": ["Servantes", "Dante", "Homer", "Vergili"],
            "correct": 0
        },
        {
            "question": "Məhəmməd Füzuli hansı əsərin müəllifidir?",
            "options": ["Leyli və Məcnun", "Xosrov və Şirin", "Yeddi Gözəl", "Heç biri"],
            "correct": 0
        }
    ],
    "idman": [
        {
            "question": "Futbolda komanda neçə oyunçu ilə oynayır?",
            "options": ["10", "11", "12", "13"],
            "correct": 1
        },
        {
            "question": "Olimpiya oyunları neçə ildə bir keçirilir?",
            "options": ["2", "3", "4", "5"],
            "correct": 2
        },
        {
            "question": "Tennis meydançada neçə oyunçu oynayır?",
            "options": ["1", "2", "2 və ya 4", "4"],
            "correct": 2
        },
        {
            "question": "Basketbolda komanda neçə oyunçu ilə oynayır?",
            "options": ["4", "5", "6", "7"],
            "correct": 1
        },
        {
            "question": "Marafon yarışı neçə kilometrdir?",
            "options": ["38", "40", "42.195", "45"],
            "correct": 2
        }
    ],
    "coğrafiya": [
        {
            "question": "Dünyanın ən böyük okeanı hansıdır?",
            "options": ["Atlantik", "Hind", "Şimal Buzlu", "Sakit"],
            "correct": 3
        },
        {
            "question": "Azərbaycanın paytaxtı haradır?",
            "options": ["Gəncə", "Bakı", "Sumqayıt", "Mingəçevir"],
            "correct": 1
        },
        {
            "question": "Dünyanın ən yüksək dağı hansıdır?",
            "options": ["K2", "Everest", "Kanchenjunga", "Lhotse"],
            "correct": 1
        },
        {
            "question": "Avropanın ən böyük ölkəsi hansıdır?",
            "options": ["Almaniya", "Fransa", "Rusiya", "Ukrayna"],
            "correct": 2
        },
        {
            "question": "Azərbaycanın ən yüksək dağı hansıdır?",
            "options": ["Bazardüzü", "Şahdağ", "Tufandağ", "Babadağ"],
            "correct": 0
        }
    ]
}


def get_questions(category, count=10):
    """Kateqoriyadan sualları qaytarır"""
    if category not in QUESTIONS_DATABASE:
        return []
    
    questions = QUESTIONS_DATABASE[category]
    import random
    return random.sample(questions, min(count, len(questions)))


def get_categories():
    """Bütün kateqoriyaları qaytarır"""
    return list(QUESTIONS_DATABASE.keys())