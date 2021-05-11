import re
import music21 as m21
import operator
import copy
import math
from pathlib import Path
import os
from collections.abc import Iterable

import lib.NotationLinear as nlin


RESOURCES_PATH = None

INS_COLOR = "green"
DEL_COLOR = "red"
SUB_COLOR = "blue"

def setResourchesPath(path):
    global RESOURCES_PATH
    RESOURCES_PATH = path


def annotate_differences(operations):
    for op in operations:
        # bar
        if op[0] == "insbar":
            assert type(op[2]) == nlin.Bar
            # color all the notes in the inserted score2 measure using INS_COLOR
            for el in op[2].measure.recurse().notesAndRests:
                el.style.color = INS_COLOR

        elif op[0] == "delbar":
            assert type(op[1]) == nlin.Bar
            # color all the notes in the deleted score1 measure using DEL_COLOR
            for el in op[1].measure.recurse().notesAndRests:
                el.style.color = DEL_COLOR

        # voices
        elif op[0] == "voiceins":
            assert type(op[2]) == nlin.Voice
            # color all the notes in the inserted score2 voice using INS_COLOR
            for el in op[2].voice.recurse().notesAndRests:
                el.style.color = INS_COLOR

        elif op[0] == "voicedel":
            assert type(op[1]) == nlin.Voice
            # color all the notes in the deleted score1 voice using DEL_COLOR
            for el in op[1].voice.recurse().notesAndRests:
                el.style.color = DEL_COLOR

        # note
        elif op[0] == "noteins":
            assert type(op[2]) == nlin.AnnotatedNote
            # color the inserted score2 general note (note, chord, or rest) using INS_COLOR
            op[2].general_note.style.color = INS_COLOR

        elif op[0] == "notedel":
            assert type(op[1]) == nlin.AnnotatedNote
            # color the deleted score1 general note (note, chord, or rest) using DEL_COLOR
            op[1].general_note.style.color = DEL_COLOR

        # pitch
        elif op[0] == "pitchnameedit":
            assert type(op[1]) == nlin.AnnotatedNote
            assert type(op[2]) == nlin.AnnotatedNote
            assert len(op) == 5  # the indices must be there
            # color the changed note (in both scores) using SUB_COLOR
            note1 = op[1].general_note
            if 'Chord' in note1.classes:
                # color just the indexed note in the chord
                idx = op[4][0]
                note1 = note1.notes[idx]
            note1.style.color = SUB_COLOR

            note2 = op[2].general_note
            if 'Chord' in note2.classes:
                # color just the indexed note in the chord
                idx = op[4][1]
                note2 = note2.notes[idx]
            note2.style.color = SUB_COLOR

        elif op[0] == "inspitch":
            assert type(op[2]) == nlin.AnnotatedNote
            assert len(op) == 5  # the indices must be there
            # color the inserted note in score2 using INS_COLOR
            note2 = op[2].general_note
            if 'Chord' in note2.classes:
                # color just the indexed note in the chord
                idx = op[4][1]
                note2 = note2.notes[idx]
            note2.style.color = INS_COLOR

        elif op[0] == "delpitch":
            assert type(op[1]) == nlin.AnnotatedNote
            assert len(op) == 5  # the indices must be there
            # color the deleted note in score1 using DEL_COLOR
            note1 = op[1].general_note
            if 'Chord' in note1.classes:
                # color just the indexed note in the chord
                idx = op[4][0]
                note1 = note1.notes[idx]
            note1.style.color = DEL_COLOR

        elif op[0] == "headedit":
            assert type(op[1]) == nlin.AnnotatedNote
            assert type(op[2]) == nlin.AnnotatedNote
            # color the changed note/rest/chord (in both scores) using SUB_COLOR
            note1 = op[1].general_note
            note1.style.color = SUB_COLOR
            note2 = op[2].general_note
            note2.style.color = SUB_COLOR

        # beam
        elif op[0] == "insbeam":
            assert type(op[2]) == nlin.AnnotatedNote
            # color the inserted beam in score2 using INS_COLOR
            note = op[2].general_note
            for beam in note.beams:
                beam.style.color = INS_COLOR

        elif op[0] == "delbeam":
            assert type(op[1]) == nlin.AnnotatedNote
            # color the deleted beam in score1 using DEL_COLOR
            note = op[1].general_note
            for beam in note.beams:
                beam.style.color = DEL_COLOR

        elif op[0] == "editbeam":
            assert type(op[1]) == nlin.AnnotatedNote
            assert type(op[2]) == nlin.AnnotatedNote
            # color the changed beam (in both scores) using SUB_COLOR
            note = op[1].general_note
            for beam in note.beams:
                beam.style.color = SUB_COLOR

            note = op[2].general_note
            for beam in note.beams:
                beam.style.color = SUB_COLOR

        # accident
        elif op[0] == "accidentins":
            assert type(op[2]) == nlin.AnnotatedNote
            assert len(op) == 5  # the indices must be there
            # color the inserted accidental in score2 using INS_COLOR
            note = op[2].general_note
            if 'Chord' in note.classes:
                # color only the indexed note's accidental in the chord
                idx = op[4][1]
                note = note.notes[idx]
            if note.pitch.accidental:
                note.pitch.accidental.style.color = INS_COLOR

        elif op[0] == "accidentdel":
            assert type(op[1]) == nlin.AnnotatedNote
            assert len(op) == 5  # the indices must be there
            # color the deleted accidental in score1 using DEL_COLOR
            note = op[1].general_note
            if 'Chord' in note.classes:
                # color only the indexed note's accidental in the chord
                idx = op[4][0]
                note = note.notes[idx]
            if note.pitch.accidental:
                note.pitch.accidental.style.color = DEL_COLOR

        elif op[0] == "accidentedit":
            assert type(op[1]) == nlin.AnnotatedNote
            assert type(op[2]) == nlin.AnnotatedNote
            assert len(op) == 5  # the indices must be there
            # color the changed accidental (in both scores) using SUB_COLOR
            note1 = op[1].general_note
            if 'Chord' in note1.classes:
                # color just the indexed note in the chord
                idx = op[4][0]
                note1 = note1.notes[idx]
            if note1.pitch.accidental:
                note1.pitch.accidental.style.color = SUB_COLOR

            note2 = op[2].general_note
            if 'Chord' in note2.classes:
                # color just the indexed note in the chord
                idx = op[4][1]
                note2 = note2.notes[idx]
            if note2.pitch.accidental:
                note2.pitch.accidental.style.color = SUB_COLOR

        elif op[0] == "dotins":
            assert type(op[1]) == nlin.AnnotatedNote
            assert type(op[2]) == nlin.AnnotatedNote
            # In music21, the dots are not separately colorable from the note,
            # so we will just color the modified note here in both scores, using SUB_COLOR
            op[1].general_note.style.color = SUB_COLOR
            op[2].general_note.style.color = SUB_COLOR

        elif op[0] == "dotdel":
            assert type(op[1]) == nlin.AnnotatedNote
            assert type(op[2]) == nlin.AnnotatedNote
            # In music21, the dots are not separately colorable from the note,
            # so we will just color the modified note here in both scores, using SUB_COLOR
            op[1].general_note.style.color = SUB_COLOR
            op[2].general_note.style.color = SUB_COLOR

        # tuplets TODO
        elif op[0] == "instuplet":
            pass
        elif op[0] == "deltuplet":
            pass
        elif op[0] == "edittuplet":
            pass
        elif op[0] == "instuplet":
            pass
        elif op[0] == "deltuplet":
            pass
        elif op[0] == "edittuplet":
            pass

        # ties TODO
        elif op[0] == "tieins":
            assert type(op[1]) == nlin.AnnotatedNote
            assert type(op[2]) == nlin.AnnotatedNote
            assert len(op) == 5  # the indices must be there
            # In music21, ties are not colorable, so we will just pretend the note was
            # modified.
            # Color the modified note here in both scores, using SUB_COLOR
            note1 = op[1].general_note
            if 'Chord' in note1.classes:
                # color just the indexed note in the chord
                idx = op[4][0]
                note1 = note1.notes[idx]
            note1.style.color = SUB_COLOR

            note2 = op[2].general_note
            if 'Chord' in note2.classes:
                # color just the indexed note in the chord
                idx = op[4][1]
                note2 = note2.notes[idx]
            note2.style.color = SUB_COLOR

        elif op[0] == "tiedel":
            assert type(op[1]) == nlin.AnnotatedNote
            assert type(op[2]) == nlin.AnnotatedNote
            assert len(op) == 5  # the indices must be there
            # In music21, ties are not colorable, so we will just pretend the note was
            # modified.
            # Color the modified note here in both scores, using SUB_COLOR
            note1 = op[1].general_note
            if 'Chord' in note1.classes:
                # color just the indexed note in the chord
                idx = op[4][0]
                note1 = note1.notes[idx]
            note1.style.color = SUB_COLOR

            note2 = op[2].general_note
            if 'Chord' in note2.classes:
                # color just the indexed note in the chord
                idx = op[4][1]
                note2 = note2.notes[idx]
            note2.style.color = SUB_COLOR

        else:
            print(
                "Annotation type {} not yet supported for visualization".format(op[0])
            )
