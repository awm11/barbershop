#Give notes a number

C, Cx, Db, D, Dx, Eb, E, F, Fx, Gb, G, Gx, Ab, A, Ax, Bb, B = 0, 1, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11
c, cx, db, d, dx, eb, e, f, fx, gb, g, gx, ab, a, ax, bb, b = 0, 1, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11


#list of all the keys

keys = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B'] #for turning n - > note name

# cmaj = [c, e, g, c]
# cmi = [c, eb, g, c]
# cdom7 = [c, e, g, bb]
# cdim = [c, eb, fx, a]
# cmin7 = [c, eb, g, bb]


maj2x1 = [[c-c, e-c, g-e, (c-g)%12], "maj2x1", [['1st', 0], ['1st', 0], ['3rd', -13],['5th', 2]]]
maj2x3 = [[e-c, e-e, g-e, (c-g)%12], "maj2x3", [['1st', 0],['3rd', -13], ['3rd', -13],['5th', 2]]]
maj2x5 = [[e-c, g-e, g-g, (c-g)%12], "maj2x5", [['1st', 0],['3rd', -13], ['5th', 2],['5th', 2]]]

min2x1 = [[c-c, eb-c, g-eb, (c-g)%12], "min2x1", [['1st', 0],['1st', 0],['m3rd', 15],['5th', 2]]]
min2x3 = [[eb-c, eb-eb, g-eb, (c-g)%12], "min2x3", [['1st', 0],['m3rd', 15],['m3rd', 15],['5th', 2]]]
min2x5 = [[eb-c, g-eb, g-g, (c-g)%12], "min2x5", [['1st', 0],['m3rd', 15],['5th', 2],['5th', 2]]]

aug = [[e-c, gx-e, (c-gx)%12], "aug", [['1st', 0],['m3rd', -33],['#5th', 2]]]
dom7 = [[e-c, g-e, (bb-g), (c-bb)%12], "dom7", [['1st', 0],['3rd', -13],['5th',2],['7th',-31]]]
dim = [[eb-c, fx-eb, a-fx, (c-a)%12], "dim7", [['1st', 0],['m3rd', 0],['b5th', 0],['7th', 0]]]
aug7 = [[e-c, gx-e, bb-gx, (c-bb)%12], "aug7", [['1st', 0],['3rd', -13],['#5th', -17],['7th', -31]]]
min7 = [[eb-c, g-eb, bb-g, (c-bb)%12], "min7", [['1st', 0],['m3rd', -33],['5th', 2],['7th', -31]]]
maj7 = [[e-c, g-e, b-g, (c-b)%12], "maj7", [['1st', 0],['3rd', -13],['5th', 2],['maj7th', -11]]]
maj6 = [[e-c, g-e, a-g, (c-a)%12], "maj6", [['1st', 0],['m3rd', -13],['5th', 2],['6th', -15]]]
min6 = [[eb-c, g-eb, a-g, (c-a)%12], "min6", [['1st', 2],['m3rd', -31],['5th', 4],['6th', -13]]]
maj9 = [[d-c, e-d, g-e, (c-g)%12], "maj9", [['1st', 0],['9th', 4],['3rd',-13],['5th',2]]]
dom9_no_5th = [[d-c, e-d, bb-e, (c-bb)%12], "dom9_no_5th", [['1st', 0],['9th', 4],['3rd',-13],['7th',-31]]]
chin7 = [[e-c, g-e, (bb-g), (c-bb)%12], "dom7", [['1st', 0],['3rd', -13],['5th',2],['7th',0]]]

three_note_chords = [maj2x1, maj2x3, maj2x5, min2x1, min2x3, min2x5]
four_note_chords = [dom7, dim, maj7, maj6, min6, maj9, dom9_no_5th, aug7]

def CircEquiv(inversion, standard):
        if len(inversion) != len(standard):
            return False

        str1 = ''.join(map(str, inversion))
        str2 = ''.join(map(str, standard))
        if len(inversion) != len(inversion):
            return False
        
        searchable_string = str2 + str2
        return searchable_string.find(str1)
    
def chord_categoriser(full_chord, duplicate=0):
    chord = []
    for note in full_chord:
        chord.append(note[3])
    if duplicate == 0:
        if 0 in chord:
            chords_to_check = three_note_chords
        else:
            chords_to_check = four_note_chords
    else:
        chords_to_check = [min7,chin7]
    for stan_chord in chords_to_check:
        if CircEquiv(chord, stan_chord[0]) is not -1:
            root = CircEquiv(chord, stan_chord[0])
            key = full_chord[root][1]
            i = root
            j = 0
            for note in full_chord:
                one_note=full_chord[j]
                one_note.append(stan_chord[2][i%4])
                if i%4 == 0:
                    key = full_chord[j][1]
                i = i + 1
                j = j + 1
            return [{'tunings': full_chord},{'stan_chord': stan_chord}, root, {'key': keys[key]}]
    return None

def dictionaryise(tunings):
    dict = {}
    for note in tunings:
        dictkey = note[0]
        value = note[4]
        dict[dictkey]=note
    return dict

def myKey(item):
    return item[1]

def normalise(chord):
    i=0
    for note in chord:
        normal = sorted(chord, key=myKey)[0][1]
#         normal = chord[0][1]
        note.append((note[1]-normal)%12)
    return chord

def getKey(item):
    return item[2]

def Order(chord):
    chord = sorted(chord, key=getKey)
    return chord

def difference(chord):
    i=0
    for note in chord:
        try:
            difference = chord[i+1][2] - chord[i][2]
        except:
            difference = (chord[0][2] - chord[3][2])%12
        note.append(difference)
        i = i + 1
    return chord


def tune(n1,n2,n3,n4):
    chord = [['b'],['br'],['ld'],['t']]
    notes = [n1,n2,n3,n4]
    for i in range (4):
        chord[i].append(notes[i])
    chord = normalise(chord)
    chord = Order(chord)
    full_chord = difference(chord)

    chord = []
    try:
        tunings = chord_categoriser(full_chord)[0]['tunings']
    except TypeError:
        return "Chord not found...we're barbershop purists here. If it's not barbershop, does it really exist?"
    tunings = dictionaryise(tunings)
    tuning_vector = [tunings['b'][4][1]-tunings['ld'][4][1],tunings['br'][4][1]-tunings['ld'][4][1],tunings['ld'][4][0],tunings['t'][4][1]-tunings['ld'][4][1]]

    chord_name = chord_categoriser(full_chord)[1]['stan_chord'][1]
    key = chord_categoriser(full_chord)[3]['key']

# 2 blocks below prepares the minor 7th equiv for printing.
    if chord_name == "maj6":
        #repeat of above
        chord = [['b'],['br'],['ld'],['t']]
        notes = [n1,n2,n3,n4]
        for i in range (4):
            chord[i].append(notes[i])
        chord = normalise(chord)
        chord = Order(chord)
        full_chord = difference(chord)
        
        tunings2 = chord_categoriser(full_chord, duplicate = 1)[0]['tunings']
        chord_name2 = chord_categoriser(full_chord, duplicate = 1)[1]['stan_chord'][1]
        key2 = chord_categoriser(full_chord, duplicate = 1)[3]['key']
        tunings2 = dictionaryise(tunings2)
        tuning_vector2 = [tunings2['b'][4][1]-tunings2['ld'][4][1],tunings2['br'][4][1]-tunings2['ld'][4][1],tunings2['ld'][4][0],tunings2['t'][4][1]-tunings2['ld'][4][1]]

        
    # below section checks for chinese 7 and, if so, overwrites the tunings accordingly.
    if chord_name == "dom7":
        b_note = tunings['b'][4][0]
        br_note = tunings['br'][4][0]
        ld_note = tunings['ld'][4][0]
        t_note = tunings['t'][4][0]
        
        if (ld_note == "7th" and t_note == "1st") or (ld_note == "1st" and t_note == "7th") or (ld_note == "7th" and br_note == "1st") or (ld_note == "1st" and br_note == "7th"):
            print("chinese 7th!")
            # chord = [['b'],['br'],['ld'],['t']]
            # notes = [n1,n2,n3,n4]
            # for i in range (4):
            #     chord[i].append(notes[i])
            # chord = normalise(chord)
            # chord = Order(chord)
            # full_chord = difference(chord)

            # tunings = chord_categoriser(full_chord, duplicate = 1)[0]['tunings']
            # chord_name = chord_categoriser(full_chord, duplicate = 1)[1]['stan_chord'][1]
            # key = chord_categoriser(full_chord, duplicate = 1)[3]['key']
            # tunings = dictionaryise(tunings)
            # tuning_vector = [tunings['b'][4][1]-tunings['ld'][4][1],tunings['br'][4][1]-tunings['ld'][4][1],tunings['ld'][4][0],tunings['t'][4][1]-tunings['ld'][4][1]]
        
    print("{} {}, \n{}".format(key, chord_name, tuning_vector))

    if chord_name == "maj6":
        print("\n\n  or\n\n{} {}, \n{}".format(key2, chord_name2, tuning_vector2))