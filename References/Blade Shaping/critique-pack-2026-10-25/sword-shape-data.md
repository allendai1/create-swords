# Sword silhouettes: shape data

Game: a Roblox sword-smithing game (stylised, mostly played on phones). These are the seven current blade blueprints, the finished ("refined") shape each forge ends on. Images: `all-swords-one-scale.png` (all seven at one scale) and one PNG per blade. Hilts/guards are chosen separately and aren't shown; the grey bar is the tang.

Scale in game: 0.05 studs per cm, so 100 cm = 5 studs, about one Roblox player's height.

## How the outline is built

- Units are cm. `u` runs from 0 (blade base) to 1 (point).
- `spine` and `edge` are `[u, value]` points giving the distance from the centreline to the back (positive) and to the cutting edge (negative). Points are joined with a monotone cubic (Fritsch-Carlson), flat outside the first/last point, and sampled at 64 stations.
- `length` is the length along the centreline. `curve.sori` is the total bend in radians, spread over the blade with a gaussian around `center` (width `spread`). Positive bends the point toward the spine.
- `ridge` (fraction of the way from spine to edge), `thickness`, `edgeThickness` and `spineThickness` set the cross-section, not the silhouette.
- `doubleEdged: true` makes the back a second edge.
- Measured values are taken the way sword catalogues measure them: nagasa is the straight line from the back of the base to the point; sori is the largest gap between the back and that line (negative on straight blades whose back narrows toward the point).
- Numbers come from general knowledge of real blades, slightly exaggerated for readability. Only the Japanese lengths and curves (nagasa, sori) were researched.

## Tantō

Measured: nagasa 25.8 cm, sori -0.10 cm, width at base 2.60 cm, widest 2.60 cm.

Spec note: Researched 2026-10-19: standard Kamakura tantō length (jōsun) about 25–26 cm; hira-zukuri with a little inward curve (uchizori). Inward curve amount is an estimate.

```json
{
  "tang": {
    "length": 6,
    "width": 1.8
  },
  "spec": {
    "note": "Researched 2026-10-19: standard Kamakura tantō length (jōsun) about 25–26 cm; hira-zukuri with a little inward curve (uchizori). Inward curve amount is an estimate.",
    "nagasa": 25.8,
    "sori": -0.1,
    "motohaba": 2.6,
    "sakihaba": 1.96,
    "kasane": 0.7,
    "kissaki": 4.7
  },
  "refined": {
    "length": 25.79,
    "curve": {
      "sori": -0.0117,
      "center": 0.6,
      "spread": 0.35
    },
    "spine": [
      [
        0,
        1.3
      ],
      [
        0.9,
        1.21
      ],
      [
        1,
        1.17
      ]
    ],
    "edge": [
      [
        0,
        -1.3
      ],
      [
        0.7,
        -1.05
      ],
      [
        0.88,
        -0.98
      ],
      [
        0.93,
        -0.77
      ],
      [
        0.965,
        -0.3
      ],
      [
        0.985,
        0.3
      ],
      [
        1,
        1.12
      ]
    ],
    "ridge": [
      [
        0,
        0.22
      ]
    ],
    "thickness": [
      [
        0,
        0.7
      ],
      [
        0.8,
        0.55
      ],
      [
        0.95,
        0.35
      ],
      [
        1,
        0.12
      ]
    ],
    "edgeThickness": [
      [
        0,
        0.03
      ]
    ],
    "spineThickness": [
      [
        0,
        0.8
      ]
    ]
  }
}
```

## Wakizashi

Measured: nagasa 50.0 cm, sori 1.20 cm, width at base 2.90 cm, widest 2.90 cm.

Spec note: Researched 2026-10-19: wakizashi are 30.3–60.6 cm (1–2 shaku), about 50 cm on average; Edo examples show sori from 0.2 to 1.7 cm. Widths, thickness and kissaki are exploratory.

```json
{
  "tang": {
    "length": 10,
    "width": 2
  },
  "spec": {
    "note": "Researched 2026-10-19: wakizashi are 30.3–60.6 cm (1–2 shaku), about 50 cm on average; Edo examples show sori from 0.2 to 1.7 cm. Widths, thickness and kissaki are exploratory.",
    "nagasa": 50,
    "sori": 1.2,
    "motohaba": 2.9,
    "sakihaba": 2.15,
    "kasane": 0.72,
    "kissaki": 2.9
  },
  "refined": {
    "length": 50.3,
    "curve": {
      "sori": 0.1845,
      "center": 0.55,
      "spread": 0.35
    },
    "spine": [
      [
        0,
        1.45
      ],
      [
        0.9,
        1.18
      ],
      [
        0.95,
        1.1
      ],
      [
        1,
        0.8
      ]
    ],
    "edge": [
      [
        0,
        -1.45
      ],
      [
        0.5,
        -1.22
      ],
      [
        0.92,
        -1.05
      ],
      [
        0.955,
        -0.86
      ],
      [
        0.985,
        -0.28
      ],
      [
        1,
        0.7
      ]
    ],
    "ridge": [
      [
        0,
        0.32
      ],
      [
        0.93,
        0.32
      ],
      [
        1,
        0.5
      ]
    ],
    "thickness": [
      [
        0,
        0.72
      ],
      [
        0.9,
        0.55
      ],
      [
        0.96,
        0.45
      ],
      [
        1,
        0.12
      ]
    ],
    "edgeThickness": [
      [
        0,
        0.03
      ]
    ],
    "spineThickness": [
      [
        0,
        0.72
      ]
    ]
  }
}
```

## Katana

Measured: nagasa 70.0 cm, sori 1.80 cm, width at base 3.20 cm, widest 3.20 cm.

Spec note: Researched 2026-10-19: katana are over 60.6 cm (2 shaku), commonly about 70 cm (2 shaku 3 sun); sori ranges from under 1 cm (Kanbun era) to about 2.4 cm. Widths, thickness and kissaki are exploratory.

```json
{
  "tang": {
    "length": 14,
    "width": 2.2
  },
  "spec": {
    "note": "Researched 2026-10-19: katana are over 60.6 cm (2 shaku), commonly about 70 cm (2 shaku 3 sun); sori ranges from under 1 cm (Kanbun era) to about 2.4 cm. Widths, thickness and kissaki are exploratory.",
    "nagasa": 70,
    "sori": 1.8,
    "motohaba": 3.2,
    "sakihaba": 2.3,
    "kasane": 0.78,
    "kissaki": 3.6
  },
  "refined": {
    "length": 70.36,
    "curve": {
      "sori": 0.1865,
      "center": 0.55,
      "spread": 0.35
    },
    "spine": [
      [
        0,
        1.6
      ],
      [
        0.9,
        1.25
      ],
      [
        0.95,
        1.17
      ],
      [
        1,
        0.85
      ]
    ],
    "edge": [
      [
        0,
        -1.6
      ],
      [
        0.5,
        -1.32
      ],
      [
        0.93,
        -1.13
      ],
      [
        0.96,
        -0.95
      ],
      [
        0.985,
        -0.35
      ],
      [
        1,
        0.75
      ]
    ],
    "ridge": [
      [
        0,
        0.32
      ],
      [
        0.94,
        0.32
      ],
      [
        1,
        0.5
      ]
    ],
    "thickness": [
      [
        0,
        0.78
      ],
      [
        0.9,
        0.6
      ],
      [
        0.96,
        0.5
      ],
      [
        1,
        0.12
      ]
    ],
    "edgeThickness": [
      [
        0,
        0.03
      ]
    ],
    "spineThickness": [
      [
        0,
        0.72
      ]
    ]
  }
}
```

## Longsword

Measured: nagasa 90.0 cm, sori -1.27 cm, width at base 5.00 cm, widest 5.00 cm.

Spec note: Knightly longsword: about 90 cm, straight, double-edged, tapering to an ogive point. Not researched.

```json
{
  "doubleEdged": true,
  "tang": {
    "length": 18,
    "width": 1.6
  },
  "spec": {
    "note": "Knightly longsword: about 90 cm, straight, double-edged, tapering to an ogive point. Not researched.",
    "nagasa": 90,
    "sori": -1.27,
    "motohaba": 5
  },
  "refined": {
    "length": 89.97,
    "curve": {
      "sori": 0,
      "center": 0.5,
      "spread": 0.35
    },
    "spine": [
      [
        0,
        2.5
      ],
      [
        0.5,
        2.1
      ],
      [
        0.85,
        1.6
      ],
      [
        0.93,
        1.05
      ],
      [
        0.98,
        0.4
      ],
      [
        1,
        0.06
      ]
    ],
    "edge": [
      [
        0,
        -2.5
      ],
      [
        0.5,
        -2.1
      ],
      [
        0.85,
        -1.6
      ],
      [
        0.93,
        -1.05
      ],
      [
        0.98,
        -0.4
      ],
      [
        1,
        -0.06
      ]
    ],
    "ridge": [
      [
        0,
        0.5
      ]
    ],
    "thickness": [
      [
        0,
        0.75
      ],
      [
        0.85,
        0.5
      ],
      [
        1,
        0.12
      ]
    ],
    "edgeThickness": [
      [
        0,
        0.03
      ]
    ],
    "spineThickness": [
      [
        0,
        0.06
      ],
      [
        0.85,
        0.09
      ],
      [
        1,
        0.33
      ]
    ]
  }
}
```

## Falchion

Measured: nagasa 72.0 cm, sori -1.00 cm, width at base 3.60 cm, widest 6.49 cm.

Spec note: Cleaver-like falchion (Conyers type): straight back, edge widening to about 6.5 cm before the point (exaggerated for readability). Not researched.

```json
{
  "tang": {
    "length": 12,
    "width": 1.6
  },
  "spec": {
    "note": "Cleaver-like falchion (Conyers type): straight back, edge widening to about 6.5 cm before the point (exaggerated for readability). Not researched.",
    "nagasa": 72,
    "sori": -1,
    "motohaba": 3.6
  },
  "refined": {
    "length": 71.99,
    "curve": {
      "sori": 0,
      "center": 0.5,
      "spread": 0.35
    },
    "spine": [
      [
        0,
        1.8
      ],
      [
        0.75,
        1.8
      ],
      [
        0.88,
        1.65
      ],
      [
        0.96,
        1.15
      ],
      [
        1,
        0.6
      ]
    ],
    "edge": [
      [
        0,
        -1.8
      ],
      [
        0.3,
        -2.5
      ],
      [
        0.6,
        -3.8
      ],
      [
        0.8,
        -4.7
      ],
      [
        0.88,
        -4.3
      ],
      [
        0.94,
        -2.9
      ],
      [
        0.98,
        -1.1
      ],
      [
        1,
        0.5
      ]
    ],
    "ridge": [
      [
        0,
        0.3
      ]
    ],
    "thickness": [
      [
        0,
        0.7
      ],
      [
        0.8,
        0.5
      ],
      [
        0.95,
        0.35
      ],
      [
        1,
        0.12
      ]
    ],
    "edgeThickness": [
      [
        0,
        0.03
      ]
    ],
    "spineThickness": [
      [
        0,
        0.75
      ]
    ]
  }
}
```

## Gladius

Measured: nagasa 52.0 cm, sori -1.77 cm, width at base 5.60 cm, widest 5.60 cm.

Spec note: Roman gladius (Mainz type): about 52 cm, broad, slightly waisted, long triangular point. Not researched.

```json
{
  "doubleEdged": true,
  "tang": {
    "length": 10,
    "width": 1.6
  },
  "spec": {
    "note": "Roman gladius (Mainz type): about 52 cm, broad, slightly waisted, long triangular point. Not researched.",
    "nagasa": 52,
    "sori": -1.77,
    "motohaba": 5.6
  },
  "refined": {
    "length": 51.92,
    "curve": {
      "sori": 0,
      "center": 0.5,
      "spread": 0.35
    },
    "spine": [
      [
        0,
        2.8
      ],
      [
        0.35,
        2.55
      ],
      [
        0.6,
        2.7
      ],
      [
        0.72,
        2.55
      ],
      [
        0.85,
        1.6
      ],
      [
        0.95,
        0.6
      ],
      [
        1,
        0.06
      ]
    ],
    "edge": [
      [
        0,
        -2.8
      ],
      [
        0.35,
        -2.55
      ],
      [
        0.6,
        -2.7
      ],
      [
        0.72,
        -2.55
      ],
      [
        0.85,
        -1.6
      ],
      [
        0.95,
        -0.6
      ],
      [
        1,
        -0.06
      ]
    ],
    "ridge": [
      [
        0,
        0.5
      ]
    ],
    "thickness": [
      [
        0,
        0.8
      ],
      [
        0.7,
        0.6
      ],
      [
        0.9,
        0.4
      ],
      [
        1,
        0.12
      ]
    ],
    "edgeThickness": [
      [
        0,
        0.03
      ]
    ],
    "spineThickness": [
      [
        0,
        0.05
      ],
      [
        0.7,
        0.07
      ],
      [
        0.9,
        0.1
      ],
      [
        1,
        0.33
      ]
    ]
  }
}
```

## Zanbatō

Measured: nagasa 100.0 cm, sori -0.53 cm, width at base 18.46 cm, widest 18.46 cm.

Spec note: Not researched: proportions read off the references (about 5.4 : 1 long to wide), scaled to 100 cm (Allen 2026-10-23: about 6.5 studs with the grip).

```json
{
  "doubleEdged": false,
  "tang": {
    "length": 26,
    "width": 3
  },
  "spec": {
    "note": "Not researched: proportions read off the references (about 5.4 : 1 long to wide), scaled to 100 cm (Allen 2026-10-23: about 6.5 studs with the grip).",
    "nagasa": 100,
    "sori": -0.5299,
    "motohaba": 18.462
  },
  "refined": {
    "length": 99.9986,
    "curve": {
      "sori": 0,
      "center": 0.5,
      "spread": 0.35
    },
    "spine": [
      [
        0,
        9.231
      ],
      [
        0.985,
        9.231
      ],
      [
        1,
        8.923
      ]
    ],
    "edge": [
      [
        0,
        -9.231
      ],
      [
        0.82,
        -9.231
      ],
      [
        0.865,
        -4.808
      ],
      [
        0.91,
        -0.385
      ],
      [
        0.955,
        4.038
      ],
      [
        1,
        8.462
      ]
    ],
    "ridge": [
      [
        0,
        0.78
      ]
    ],
    "thickness": [
      [
        0,
        1.231
      ],
      [
        0.8,
        1.077
      ],
      [
        0.97,
        0.692
      ],
      [
        1,
        0.231
      ]
    ],
    "edgeThickness": [
      [
        0,
        0.05
      ]
    ],
    "spineThickness": [
      [
        0,
        1.231
      ]
    ]
  }
}
```
