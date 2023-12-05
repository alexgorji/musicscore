#: This dictionary is used for example to split unwritable chords into two writable ones. A chord may be unwritable because of its position inside the beat and its quarter duration. Sometimes are chords split only because of better readability. The structure of this dictionary is as follows: {position in Beat (or offset): {duration: [split durations]}}
SPLITTABLES = {
    (0, 1): {
        (5, 6): [(3, 6), (2, 6)],
        (5, 7): [(3, 7), (2, 7)],
        (5, 8): [(4, 8), (1, 8)],
        (5, 9): [(3, 9), (2, 9)],
        (5, 11): [(4, 11), (1, 11)],

        (7, 8): [(4, 8), (3, 8)],
        (7, 9): [(4, 9), (3, 9)],
        (7, 10): [(5, 10), (2, 10)],
        (7, 11): [(4, 11), (3, 11)],
    },
    (1, 6): {
        (4, 6): [(2, 6), (2, 6)],
        (5, 6): [(2, 6), (3, 6)],
    },
    (2, 6): {
        (3, 6): [(2, 6), (1, 6)],
        (5, 6): [(2, 6), (3, 6)],
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
        (5, 9): [(1, 9), (4, 9)]
    },
}
NOTETYPES = {
    (1, 12): '32nd',
    (1, 11): '32nd',
    (2, 11): '16th',
    (4, 11): 'eighth',
    (8, 11): 'quarter',
    (1, 10): '32nd',
    (1, 9): '32nd',
    (2, 9): '16th',
    (4, 9): 'eighth',
    (8, 9): 'quarter',
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
#: {offset: {quarter_duration: return value(s), ... }, ...}
BEATWISE_EXCEPTIONS = {0: {5: (3, 2), 6: (6,)}}
