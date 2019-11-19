import lib.m21utils as m21u
from fractions import Fraction
import music21 as m21

class AnnotatedNote:
    def __init__(self, general_note, enhanced_beam_list, tuple_info):
        """
        A class with the purpose to extend music21 GeneralNote
        :param note: the music21 generalNote
        :param enhanced_beam_list a list with beaming informations
        :tuple_info: a list with tuple info
        """
        self.general_note = general_note
        self.beamings = enhanced_beam_list
        self.tuplets = tuple_info
        ##compute the representaiton of NoteNode as in the paper
        #pitches is a list  of elements, each one is (pitchposition, accidental, tie)
        if self.general_note.isRest:
            self.pitches = [("R","None",False)] #accidental and tie are automaticaly set for rests
        elif self.general_note.isChord:
            self.pitches = [m21u.note2tuple(p) for p in self.general_note.sortDiatonicAscending().notes]
        elif self.general_note.isNote:
            self.pitches = [m21u.note2tuple(self.general_note)]
        else:
            raise TypeError("The generalNote must be a Chord, a Rest or a Note")
        #note head
        type_number= Fraction(m21.duration.convertTypeToNumber(self.general_note.duration.type))
        if type_number >= 4:
            self.note_head = 4
        else: 
            self.note_head = type_number
        #dots
        self.dots = self.general_note.duration.dots

    def notation_size(self):
        """a measure of how much symbols are display in the score
        
        Returns:
            [int] -- the notation size of the annotated note
        """
        size = 0
        #add for the pitches
        for pitch in self.pitches:
            size += m21u.pitch_size(pitch)
        #add for the dots
        size+= self.dots*len(self.pitches) #one dot for each note if it's a chord
        #add for the beamings
        size+= len(self.beamings)
        #add for the tuplets
        size+= len(self.tuplets)
        return size

    def __repr__(self):
        "(pitches, notehead, dots, beaming, tuplets)"
        out = "{},{},{},{},{}".format(self.pitches,self.note_head, self.dots, self.beamings, self.tuplets)
        return out

    def __str__(self):
        """
        Returns:
            str -- the representation of notehead with ties and dots, beamings and tuplets
        """
        string = "["
        for p in self.pitches: #add for pitches
            string += p[0]
            if p[1] != "None":
                string += p[1]
            if p[2]:
                string += "T"
            string+= ","
        string = string[:-1] # delete the last comma
        string += "]"
        string+= str(self.note_head) #add for notehead
        for _ in range(self.dots): #add for dots
            string+= "*"
        if len(self.beamings) > 0:# add for beaming
            string += "B"
            for b in self.beamings: 
                if b == "start": string += "sr"
                elif b == "continue": string += "co"
                elif b == "stop": string += "sp"
                elif b == "partial": string += "pa"
                else: raise Exception ("Incorrect beaming type: {}".format(b))
        if len(self.tuplets) > 0: # add for tuplets
            string += "T"
            for t in self.tuplets: 
                if t == "start": string += "sr"
                elif t == "continue": string += "co"
                elif t == "stop": string += "sp"
                else: raise Exception ("Incorrect tuplets type: {}".format(t))     
        return string

    def get_note_id(self):
        return [self.general_note.id]


class VoiceLinear:
    def __init__(self, voice, bar_reference = None, mei_id = None):
        """
        :param measure: m21 voice for one measure
        """
        self.note_list = m21u.get_notes(voice)
        self.en_beam_list = m21u.get_enhance_beamings(self.note_list) #beams and type (type for note shorter than quarter notes)
        self.tuplet_list = m21u.get_tuplets_type(self.note_list) #corrected tuplets (with "start" and "continue")
        self.tuple_info = m21u.get_tuplets_info(self.note_list)
        #create a list of notes with beaming and tuplets information attached
        self.annot_notes = []
        for i, n in enumerate(self.note_list):
                self.annot_notes.append(AnnotatedNote(n,self.en_beam_list[i],self.tuple_info[i]))
        #set references for pointing at that specific measure
        self.bar_reference = bar_reference
        self.mei_id = mei_id
    
    def __eq__(self, other):
        if not isinstance(other, VoiceLinear):
            return False
        else: 
            return self.__repr__() == other.__repr__()

    def notation_size(self):
        return sum([an.notation_size() for an in self.annot_notes])

    def __repr__(self):
        return  (self.annot_notes.__repr__())

    def __str__(self):
        string = "["
        for an in self.annot_notes:
            string += str(an)
            string += ","
        string = string[:-1] # delete the last comma
        string += "]"
        return string

    def get_note_id(self):
        return [an.general_note.id for an in self.annot_notes]



class ScoreLinear:
    def __init__(self,score):
        """
        Take a music21 score and store it a sequence of Full Trees
        The hierarchy is "score -> parts ->measures -> voices -> notes"
        Arguments:
            score {[music21 score]} a music21 score
        """
        self.part_list = [] 
        for part in score.parts.stream():
            measures_list = [] 
            for measure_index, measure in enumerate(part.getElementsByClass('Measure')):
                voices_list = [] 
                if len(measure.voices) == 0:  # there is a single Voice ( == for the library there are no voices)
    #                print("Part {}, measure {}".format(part_index,measure_index))
                    voices_list.append(VoiceLinear(measure,bar_reference=measure_index, mei_id=[note.id for note in m21u.get_notes(measure)]))
                else:  # there are multiple voices (or an array with just one voice)
                    for voice in measure.voices:
    #                    print("Part {}, measure {}".format(part_index,measure_index))
                        voices_list.append(VoiceLinear(voice, bar_reference=measure_index, mei_id=[note.id for note in m21u.get_notes(voice)]))
                measures_list.append(voices_list) #add the list of voices to the list of measures
            self.part_list.append(measures_list) #add the complete part to part_list
        
        self.n_of_parts = len(self.part_list)

    #return the sequences of measures for a specified part
    def measures_from_part(self,part_number):
        if part_number not in range(0,len(self.part_list)):
            raise Exception("parameter 'part_number' should be between 0 and {}".format(len(self.part_list)-1))
        return self.part_list[part_number]