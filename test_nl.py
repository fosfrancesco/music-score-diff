import lib.NotationLinear as nlin
import music21 as m21
from pathlib import Path

def test_annotNote1():
    n1 = m21.note.Note(nameWithOctave='D#5',quarterLength=1)
    #create annotated note
    anote = nlin.AnnotatedNote(n1,[],[])
    assert(anote.__repr__() == "[('D5', 'sharp', False)],4,0,[],[]")
    assert(str(anote) == "[D5sharp]4")

def test_annotNote2():
    n1 = m21.note.Note(nameWithOctave='E#5',quarterLength=0.5)
    #create annotated note
    anote = nlin.AnnotatedNote(n1,["start"],["start"])
    assert(anote.__repr__() == "[('E5', 'sharp', False)],4,0,['start'],['start']" )
    assert(str(anote)=="[E5sharp]4BsrTsr")

def test_annotNote3():
    n1 = m21.note.Note(nameWithOctave='D5',quarterLength=2)
    n1.tie = m21.tie.Tie('stop')
    #create annotated note
    anote = nlin.AnnotatedNote(n1,[],[])
    assert(anote.__repr__() == "[('D5', 'None', True)],2,0,[],[]")
    assert(str(anote) == "[D5T]2")

def test_annotNote_size1():
    n1 = m21.note.Note(nameWithOctave='D5',quarterLength=2)
    n1.tie = m21.tie.Tie('stop')
    #create annotated note
    anote = nlin.AnnotatedNote(n1,[],[])
    assert(anote.notation_size()== 2 )

def test_annotNote_size2():
    n1 = m21.note.Note(nameWithOctave='D#5',quarterLength=1.5)
    n1.tie = m21.tie.Tie('stop')
    #create annotated note
    anote = nlin.AnnotatedNote(n1,[],[])
    assert(anote.notation_size()== 4 )

def test_noteNode_size3():
    d = m21.duration.Duration(1.5)
    n1 = m21.chord.Chord(['D', 'F#', 'A'],duration=d)
    #create annotated note
    anote = nlin.AnnotatedNote(n1,[],[])
    assert(anote.notation_size()== 7 )

def test_noteNode_size4():
    n1 = m21.note.Note(nameWithOctave='D5')
    n2 = m21.note.Note(nameWithOctave='F#5')
    n2.tie = m21.tie.Tie('stop')
    n3 = m21.note.Note(nameWithOctave='G#5')
    d = m21.duration.Duration(1.75)
    chord = m21.chord.Chord([n1,n2,n3],duration=d)
    #create annotated note
    anote = nlin.AnnotatedNote(chord,[],[])
    assert(anote.notation_size()== 12 )

def test_scorelin1():
    #import score
    score1_path = Path("test_scores/polyphonic_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    #produce a ScoreTree
    score_lin1 = nlin.ScoreLinear(score1)
    #number of parts
    assert(len(score_lin1.part_list)==2)
    #number of measures for each part
    assert(len(score_lin1.part_list[0])==5)
    assert(len(score_lin1.part_list[1])==5)
    #number of voices for each measure in part 0
    for m in score_lin1.part_list[0]:
        assert(len(m)==1)

def test_scorelin2():
    #import score
    score1_path = Path("test_scores/monophonic_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    #produce a ScoreTree
    score_lin1 = nlin.ScoreLinear(score1)
    #number of parts
    assert(len(score_lin1.part_list)==1)
    #number of measures for each part
    assert(len(score_lin1.part_list[0])==11)
    #number of voices for each measure in part 0
    for m in score_lin1.part_list[0]:
        assert(len(m)==1)

def test_generalnotes1():
    #import score
    score1_path = Path("test_scores/chord_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    #produce a ScoreTree
    score_lin1 = nlin.ScoreLinear(score1)
    #number of parts
    assert(len(score_lin1.part_list)==1)
    #number of measures for each part
    assert(len(score_lin1.part_list[0])==1)
    #number of voices for each measure in part 0
    for m in score_lin1.part_list[0]:
        assert(len(m)==1)
    assert(score_lin1.part_list[0][0][0].notation_size() == 14)

def test_ties1():
    #import score
    score1_path = Path("test_scores/tie_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    #produce a ScoreTree
    score_lin1 = nlin.ScoreLinear(score1)
    #number of parts
    assert(len(score_lin1.part_list)==1)
    #number of measures for each part
    assert(len(score_lin1.part_list[0])==1)
    #number of voices for each measure in part 0
    for m in score_lin1.part_list[0]:
        assert(len(m)==1)
    expected_tree_repr = "[[E4]4Bsr,[E4T]4Bcosr,[D4]4Bspsp,[C4,E4]4Bsr,[C4T]4Bcosr,[D4]4Bspsp,[E4,G4,C5]4,[E4]4Bsr,[F4]4Bsp]"
    assert(str(score_lin1.part_list[0][0][0]) == expected_tree_repr )
    assert(score_lin1.part_list[0][0][0].notation_size() == 26)
