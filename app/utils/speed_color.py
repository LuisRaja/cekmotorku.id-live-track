__all__ = ['speed_to_color']

STOPS = [
    (0,   '#0055FF'),
    (20,  '#00AAFF'),
    (40,  '#00FF55'),
    (60,  '#AAFF00'),
    (80,  '#FFD000'),
    (100, '#FF6600'),
    (120, '#FF0044'),
]

def speed_to_color(kmh: float) -> str:
    spd = max(0.0, min(140.0, kmh))
    for i in range(len(STOPS) - 1):
        lo, hi = STOPS[i][0], STOPS[i + 1][0]
        if lo <= spd <= hi:
            t = (spd - lo) / (hi - lo) if hi != lo else 0
            c1, c2 = STOPS[i][1], STOPS[i + 1][1]
            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
            r = round(r1 + t * (r2 - r1))
            g = round(g1 + t * (g2 - g1))
            b = round(b1 + t * (b2 - b1))
            return f'#{r:02x}{g:02x}{b:02x}'
    return STOPS[-1][1]
