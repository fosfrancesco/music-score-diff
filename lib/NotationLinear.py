import lib.m21utils as m21u
from fractions import Fraction
import music21 as m21


class AnnotatedNote:
    def __init__(self, general_note, enhanced_beam_list, tuple_list):
        """
        A class with the purpose to extend music21 GeneralNote
        :param note: the music21 generalNote
        :param enhanced_beam_list a list with beaming informations
        :tuple_info: a list with tuple info
        """
        self.general_note = general_note.id
        self.beamings = enhanced_beam_list
        self.tuplets = tuple_list
        ##compute the representaiton of NoteNode as in the paper
        #pitches is a list  of elements, each one is (pitchposition, accidental, tie)
        if general_note.isRest:
            self.pitches = [("R","None",False)] #accidental and tie are automaticaly set for rests
        elif general_note.isChord:
            self.pitches = [m21u.note2tuple(p) for p in general_note.sortDiatonicAscending().notes]
        elif general_note.isNote:
            self.pitches = [m21u.note2tuple(general_note)]
        else:
            raise TypeError("The generalNote must be a Chord, a Rest or a Note")
        #note head
        type_number= Fraction(m21.duration.convertTypeToNumber(general_note.duration.type))
        if type_number >= 4:
            self.note_head = 4
        else:
            self.note_head = type_number
        #dots
        self.dots = general_note.duration.dots
        # articulations
        self.articulations = general_note.articulations

    def notation_size(self):
        """a measure of how much symbols are display in the score

        Returns:
            [int] -- the notation size of the annotated note
        """
        size = 0
        # add for the pitches
        for pitch in self.pitches:
            size += m21u.pitch_size(pitch)
        # add for the dots
        size += self.dots * len(self.pitches)  # one dot for each note if it's a chord
        # add for the beamings
        size += len(self.beamings)
        # add for the tuplets
        size += len(self.tuplets)
        # add for the articulations
        size += len(self.articulations)
        return size

    def __repr__(self):
        # repr consider also the id!
        # (pitches, notehead, dots, beaming, tuplets,id)
        out = "{},{},{},{},{},{},{}".format(
            self.pitches,
            self.note_head,
            self.dots,
            self.beamings,
            self.tuplets,
            self.general_note,
            self.articulations,
        )
        return out

    def __str__(self):
        """
        Returns:
            str -- the representation of notehead with ties and dots, beamings and tuplets
        """
        string = "["
        for p in self.pitches:  # add for pitches
            string += p[0]
            if p[1] != "None":
                string += p[1]
            if p[2]:
                string += "T"
            string += ","
        string = string[:-1]  # delete the last comma
        string += "]"
        string += str(self.note_head)  # add for notehead
        for _ in range(self.dots):  # add for dots
            string += "*"
        if len(self.beamings) > 0:  # add for beaming
            string += "B"
            for b in self.beamings:
                if b == "start":
                    string += "sr"
                elif b == "continue":
                    string += "co"
                elif b == "stop":
                    string += "sp"
                elif b == "partial":
                    string += "pa"
                else:
                    raise Exception("Incorrect beaming type: {}".format(b))
        if len(self.tuplets) > 0:  # add for tuplets
            string += "T"
            for t in self.tuplets:
                if t == "start":
                    string += "sr"
                elif t == "continue":
                    string += "co"
                elif t == "stop":
                    string += "sp"
                else:
                    raise Exception("Incorrect tuplets type: {}".format(t))
        if len(self.articulations) > 0:  # add for articulations
            for a in self.articulations:
                string += a
        return string

    def get_note_id(self):
        return [self.general_note]

    def __eq__(self, other):
        # equality does not consider the MEI id!
        if not isinstance(other, AnnotatedNote):
            return False
        elif self.pitches != other.pitches:
            return False
        elif self.note_head != other.note_head:
            return False
        elif self.dots != other.dots:
            return False
        elif self.beamings != other.beamings:
            return False
        elif self.tuplets != other.tuplets:
            return False
        elif self.articulations != other.articulations:
            return False
        else:
            return True


class Voice:
    def __init__(self, voice):
        """
        :param measure: m21 voice for one measure
        """
        self.voice = voice.id
        self.note_list = m21u.get_notes(voice)
        self.en_beam_list = m21u.get_enhance_beamings(
            self.note_list
        )  # beams and type (type for note shorter than quarter notes)
        self.tuplet_list = m21u.get_tuplets_type(
            self.note_list
        )  # corrected tuplets (with "start" and "continue")
        self.tuple_info = m21u.get_tuplets_info(self.note_list)
        # create a list of notes with beaming and tuplets information attached
        self.annot_notes = []
        for i, n in enumerate(self.note_list):
            self.annot_notes.append(
                AnnotatedNote(n, self.en_beam_list[i], self.tuplet_list[i])
            )
        self.n_of_notes = len(self.annot_notes)

    def __eq__(self, other):
        # equality does not consider MEI id!
        if not isinstance(other, Voice):
            return False
        elif len(self.annot_notes) != len(other.annot_notes):
            return False
        else:
            return all(
                [an[0] == an[1] for an in zip(self.annot_notes, other.annot_notes)]
            )

    def notation_size(self):
        return sum([an.notation_size() for an in self.annot_notes])

    def __repr__(self):
        return self.annot_notes.__repr__()

    def __str__(self):
        string = "["
        for an in self.annot_notes:
            string += str(an)
            string += ","
        string = string[:-1]  # delete the last comma
        string += "]"
        return string

    def get_note_id(self):
        return [an.general_note for an in self.annot_notes]


class Bar:
    def __init__(self, measure):
        """
        :param measure: m21 measure
        """
        self.measure = measure.id
        self.voices_list = []
        if (
            len(measure.voices) == 0
        ):  # there is a single Voice ( == for the library there are no voices)
            self.voices_list.append(Voice(measure))
        else:  # there are multiple voices (or an array with just one voice)
            for voice in measure.voices:
                self.voices_list.append(Voice(voice))
        self.n_of_voices = len(self.voices_list)

    def __eq__(self, other):
        # equality does not consider MEI id!
        if not isinstance(other, Bar):
            return False
        elif len(self.voices_list) != len(other.voices_list):
            return False
        else:
            return all([v[0] == v[1] for v in zip(self.voices_list, other.voices_list)])

    def notation_size(self):
        return sum([v.notation_size() for v in self.voices_list])

    def __repr__(self):
        return self.voices_list.__repr__()

    def get_note_id(self):
        notes_id = []
        for v in self.voices_list:
            notes_id.extend(v.get_note_id())
        return notes_id


class Part:
    def __init__(self, part):
        """
        :param measure: m21 part
        """
        self.part = part.id
        self.bar_list = []
        for measure in part.getElementsByClass("Measure"):
            self.bar_list.append(Bar(measure))  # create the bar objects
        self.n_of_bars = len(self.bar_list)

    def __eq__(self, other):
        # equality does not consider MEI id!
        if not isinstance(other, Part):
            return False
        elif len(self.bar_list) != len(other.bar_list):
            return False
        else:
            return all([b[0] == b[1] for b in zip(self.bar_list, other.bar_list)])

    def notation_size(self):
        return sum([b.notation_size() for b in self.bar_list])

    def __repr__(self):
        return self.bar_list.__repr__()

    def get_note_id(self):
        notes_id = []
        for b in self.bar_list:
            notes_id.extend(b.get_note_id())
        return notes_id


class Score:
    def __init__(self, score):
        """
        Take a music21 score and store it a sequence of Full Trees
        The hierarchy is "score -> parts ->measures -> voices -> notes"
        Arguments:
            score {[music21 score]} a music21 score
        """
        self.score = score.id
        self.part_list = []
        for part in score.parts.stream():
            self.part_list.append(
                Part(part)
            )  # create and add the Part object to part_list
        self.n_of_parts = len(self.part_list)

    def __eq__(self, other):
        # equality does not consider MEI id!
        if not isinstance(other, Score):
            return False
        elif len(self.part_list) != len(other.part_list):
            return False
        else:
            return all([p[0] == p[1] for p in zip(self.part_list, other.part_list)])

    def notation_size(self):
        return sum([p.notation_size() for p in self.part_list])

    def __repr__(self):
        return self.part_list.__repr__()

    def get_note_id(self):
        notes_id = []
        for p in self.part_list:
            notes_id.extend(p.get_note_id())
        return notes_id

    # return the sequences of measures for a specified part
    def measures_from_part(self, part_number):
        if part_number not in range(0, len(self.part_list)):
            raise Exception(
                "parameter 'part_number' should be between 0 and {}".format(
                    len(self.part_list) - 1
                )
            )
        return self.part_list[part_number].bar_list
