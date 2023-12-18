#: This dictionary is used for example to split unwritable chords into two writable ones. A chord may be unwritable because of its position inside the beat and its quarter duration. Sometimes are chords split only because of better readability. The structure of this dictionary is as follows: {position in Beat (or offset): {duration: [split durations]}}

SPLITTABLES = {
    (0, 1): {
        # (4, 9): [(3, 9), (1, 9)],

        (5, 6): [(3, 6), (2, 6)],
        (5, 7): [(3, 7), (2, 7)],
        (5, 8): [(4, 8), (1, 8)],
        (5, 9): [(3, 9), (2, 9)],
        # (5, 11): [(4, 11), (1, 11)],

        (7, 8): [(4, 8), (3, 8)],
        (7, 9): [(6, 9), (1, 9)],
        # (7, 10): [(5, 10), (2, 10)],
        # (7, 11): [(4, 11), (3, 11)],

        (8, 9): [(6, 9), (2, 9)]
    },
    (1, 6): {
        (4, 6): [(2, 6), (2, 6)],
        (5, 6): [(2, 6), (3, 6)],
    },
    (2, 6): {
        (3, 6): [(2, 6), (1, 6)],
    },
    (1, 8): {
        (4, 8): [(3, 8), (1, 8)],
        (5, 8): [(3, 8), (2, 8)],
        (6, 8): [(3, 8), (3, 8)],
        (7, 8): [(3, 8), (4, 8)],
    },
    (2, 8): {
        (3, 8): [(2, 8), (1, 8)],
        (5, 8): [(2, 8), (3, 8)],
    },
    (1, 7): {
        (5, 7): [(3, 7), (2, 7)],
        (6, 7): [(3, 7), (3, 7)],
    },
    (2, 7): {
        (5, 7): [(3, 7), (2, 7)],
    },
    (3, 8): {
        (2, 8): [(1, 8), (1, 8)],
        (3, 8): [(1, 8), (2, 8)],
        (4, 8): [(1, 8), (3, 8)],
        (5, 8): [(1, 8), (4, 8)],
    },
    (1, 9): {
        # (3, 9): [(2, 9), (1, 9)],
        # (4, 9): [(2, 9), (2, 9)],
        (5, 9): [(2, 9), (3, 9)],
        # (6, 9): [(2, 9), (3, 9), (1, 9)],
        (7, 9): [(1, 9), (6, 9)],
        (8, 9): [(2, 9), (6, 9)],
    },
    (2, 9): {
        # (2, 9): [(1, 9), (1, 9)],
        # (3, 9): [(1, 9), (2, 9)],
        # (4, 9): [(1, 9), (3, 9)],
        # (5, 9): [(1, 9), (3, 9), (1, 9)],
        (5, 9): [(1, 9), (4, 9)],
        # (6, 9): [(1, 9), (3, 9), (2, 9)],
        (7, 9): [(1, 9), (6, 9)],
    },
    (3, 9): {
        # (4, 9): [(3, 9), (1, 9)],
        (5, 9): [(3, 9), (2, 9)],
    },
    (4, 9): {
        # (3, 9): [(2, 9), (1, 9)],
        # (4, 9): [(2, 9), (2, 9)],
        (5, 9): [(2, 9), (3, 9)],
    },
    (5, 9): {
        # (2, 9): [(1, 9), (1, 9)],
        # (3, 9): [(1, 9), (2, 9)],
        # (4, 9): [(1, 9), (3, 9)],
    }
}

GENERALSPLITTABLES = {
    5: (3, 2),
    7: (4, 3),
    9: (8, 1),
    10: (8, 2),
    11: (8, 3),
    13: (8, 3, 2),
    14: (8, 6),
    15: (8, 4, 3),
    17: (16, 1),
    19: (16, 3),
    21: (16, 3, 2),
    23: (16, 4, 3),
    25: (16, 8, 1),
    27: (16, 8, 3),
    29: (16, 8, 3, 2),
    30: (16, 8, 6),
    31: (16, 8, 4, 3),
}
# {beat_duration: {beat_subdivision: {quarter_duration as integer ratio: [split durations]}}
SPLITTEXCEPTIONS = {
    1: {
        10: {(1, 2): [(3, 10), (2, 10)]},
        12: {(3, 4): [(6, 12), (3, 12)]},
        14: {(1, 2): [(4, 14), (3, 14)]},
        15: {
            (1, 3): [(3, 15), (2, 15)],
            (3, 5): [(8, 15), (1, 15)],
            (2, 3): [(8, 15), (2, 15)],
        }
    }

}

NOTETYPES = {
    (1, 32): '128th',
    (1, 16): '64th',
    (1, 15): '32nd',
    (1, 14): '32nd',
    (1, 13): '32nd',
    (1, 12): '32nd',
    (1, 11): '32nd',
    (2, 15): '16th',
    (2, 13): '16th',
    (2, 11): '16th',
    (4, 15): 'eighth',
    (4, 13): 'eighth',
    (4, 11): 'eighth',
    (8, 15): 'quarter',
    (8, 11): 'quarter',
    (1, 10): '32nd',
    (1, 9): '32nd',
    (2, 9): '16th',
    (4, 9): 'eighth',
    (8, 9): 'quarter',
    (8, 13): 'quarter',
    (1, 8): '32nd',
    (1, 7): '16th',
    (2, 7): 'eighth',
    (4, 7): 'quarter',
    (1, 6): '16th',
    (1, 5): '16th',
    (2, 5): 'eighth',
    (4, 5): 'quarter',
    (8, 5): 'half',
    (1, 4): '16th',
    (2, 4): 'eighth',
    (1, 3): 'eighth',
    (2, 3): 'quarter',
    (4, 3): 'half',
    (1, 2): 'eighth',
    (1, 1): 'quarter',
    (2, 1): 'half',
    (4, 1): 'whole',
    (8, 1): 'breve',
}

TYPEANDDOTEXCEPTIONS = {
    1: {
        6: {(1, 2): ('eighth', 1)},
        9: {
            (1, 3): ('16th', 1),
            (2, 3): ('eighth', 1)},
        12: {
            (1, 4): ('16th', 1),
            (1, 2): ('eighth', 1)
        },
        15: {
            (1, 5): ('16th', 1),
            (2, 5): ('eighth', 1),
            (4, 5): ('quarter', 1)
        }
    }
}

#: {offset: {quarter_duration: return value(s), ... }, ...}
BEATWISE_EXCEPTIONS = {0: {5: (3, 2), 6: (6,)}}

DOTEDTUPLETRATIO = {2: 3, 4: 3, 5: 3, 7: 6, 8: 6}

# number of beams:
NUMBEROFBEAMS = {'eighth': 1, '16th': 2, '32nd': 3, '64th': 4, '128th': 5}

TYPEDURATION = {
    'breve': 8,
    'whole': 4,
    'half': 2,
    'quarter': 1,
    'eighth': 1 / 2,
    '16th': 1 / 4,
    '32nd': 1 / 8,
    '64th': 1 / 16,
    '128th': 1 / 32,
}
