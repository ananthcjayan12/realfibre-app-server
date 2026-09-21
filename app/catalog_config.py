"""Catalogue and production configuration for door ordering.

Keep user-facing catalogue rules in one place so the order form, production
batching and tests use the same normalized values.
"""

DOOR_MODEL_CHOICES = [
    ("orbit", "Orbit"),
    ("petra", "Petra"),
    ("triangle", "Triangle"),
    ("astonia", "Astonia"),
    ("cloud", "Cloud"),
    ("delta", "Delta"),
    ("flora", "Flora"),
    ("hexa", "Hexa"),
    ("horizon", "Horizon"),
    ("liva", "Liva"),
    ("mars", "Mars"),
    ("milton", "Milton"),
    ("narrow", "Narrow"),
    ("periyar", "Periyar"),
    ("rectaglass", "Recta Glass"),
    ("regal", "Regal"),
    ("regency", "Regency"),
    ("richmond", "Richmond"),
    ("rivera", "Rivera"),
    ("simplon", "Simplon"),
    ("skill", "Skill"),
    ("spasio", "Spasio"),
    ("vector", "Vector"),
    ("venues", "Venues"),
    ("vetrix", "Vetrix"),
    ("wayanad", "Wayanad"),
    ("wexco", "Wexco"),
    ("wexcoglass", "Wexco Glass"),
    ("venuesglass", "Venues Glass"),
    ("plainglass", "Plain Glass"),
    ("classic", "Classic"),
    ("galaxy", "Galaxy"),
    ("queen", "Queen"),
    ("royal", "Royal"),
    ("dynamic", "Dynamic"),
    ("spider", "Spider"),
    # 2026 catalogue additions
    ("plain", "Plain"),
    ("lyka", "Lyka"),
    ("electra", "Electra"),
    ("kenz", "Kenz"),
    ("willo", "Willo"),
    ("stripes", "Stripes"),
    ("grace", "Grace"),
    ("olive", "Olive"),
    ("recta", "Recta"),
    ("other", "Other"),
]

COLOUR_CHOICES = [
    ("black", "Black"),
    ("darkgrey", "Dark Grey"),
    ("eeti", "Eeti"),
    ("leatherfinish", "Leather Finish"),
    ("lightgrey", "Light Grey"),
    ("mahagani", "Mahagani"),
    ("teakwooddark", "Teakwood Dark"),
    ("teakwoodlight", "Teakwood Light"),
    ("white", "White"),
    ("coffee", "Coffee"),
    ("offwhite", "Off White"),
    ("ivory", "Ivory"),
    # 2026 catalogue additions
    ("beigegrey", "Beige Grey"),
    ("olivegreen", "Olive Green"),
    ("goldenbrown", "ColourTech Golden Brown"),
    ("coffeebrown", "Coffee Brown"),
    ("chocolatebrown", "Chocolate Brown"),
    ("beige", "Beige"),
    ("oakwood", "Oak Wood"),
]

# Plain and Recta intentionally have no default colour until confirmed.
DEFAULT_COLOUR_BY_MODEL = {
    "lyka": "beigegrey",
    "electra": "olivegreen",
    "kenz": "goldenbrown",
    "willo": "coffeebrown",
    "stripes": "chocolatebrown",
    "grace": "beige",
    "olive": "oakwood",
}

FRAME_ADJUSTMENTS = {
    "Small": (-7.1, -7.1, -4.3),
    "Normal": (-8.0, -8.0, -4.8),
    "Medium": (-7.0, -7.0, -4.3),
    "Heavy": (-10.4, -10.4, -6.3),
    "Door Without Clearence": (0, 0, 0),
    "Door With Clearence": (-0.7, -0.7, -0.8),
}


def calculate_frame_measurements(frame_type, top, bottom, height):
    """Return adjusted (top, bottom, height) measurements for a frame type."""
    adjustment = FRAME_ADJUSTMENTS.get(frame_type)
    if adjustment is None:
        return None

    return (
        round(float(top) + adjustment[0], 2),
        round(float(bottom) + adjustment[1], 2),
        round(float(height) + adjustment[2], 2),
    )
