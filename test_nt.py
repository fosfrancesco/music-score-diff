import lib.NotationTree as nt
import music21 as m21
from pathlib import Path

def test_scoretree1():
    #import score
    score1_path = Path("test_scores/polyphonic_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    #produce a ScoreTree
    score_trees1 = nt.ScoreTrees(score1)
    #number of parts
    assert(len(score_trees1.part_list)==2)
    #number of measures for each part
    assert(len(score_trees1.part_list[0])==5)
    assert(len(score_trees1.part_list[1])==5)
    #number of voices for each measure in part 0
    for m in score_trees1.part_list[0]:
        assert(len(m)==1)


def test_scoretree2():
    #import score
    score1_path = Path("test_scores/monophonic_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    #produce a ScoreTree
    score_trees1 = nt.ScoreTrees(score1)
    #number of parts
    assert(len(score_trees1.part_list)==1)
    #number of measures for each part
    assert(len(score_trees1.part_list[0])==11)
    #number of voices for each measure in part 0
    for m in score_trees1.part_list[0]:
        assert(len(m)==1)


def test_generalnotes1():
    #import score
    score1_path = Path("test_scores/chord_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    #produce a ScoreTree
    score_trees1 = nt.ScoreTrees(score1)
    #number of parts
    assert(len(score_trees1.part_list)==1)
    #number of measures for each part
    assert(len(score_trees1.part_list[0])==1)
    #number of voices for each measure in part 0
    for m in score_trees1.part_list[0]:
        assert(len(m)==1)


def test_ties1():
    #import score
    score1_path = Path("test_scores/tie_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    #produce a ScoreTree
    score_trees1 = nt.ScoreTrees(score1)
    #number of parts
    assert(len(score_trees1.part_list)==1)
    #number of measures for each part
    assert(len(score_trees1.part_list[0])==1)
    #number of voices for each measure in part 0
    for m in score_trees1.part_list[0]:
        assert(len(m)==1)
    expected_tree_repr = "(([E4]4,([E4T]4,[D4]4)),([C4,E4]4,([C4T]4,[D4]4)),[E4,G4,C5]4,([E4]4,[F4]4))"
    assert(str(score_trees1.part_list[0][0][0].beams_tree) == expected_tree_repr )


def test_noteNode1():
    n1 = m21.note.Note(nameWithOctave='D#5',quarterLength=1)
    #create noteNode
    parent = nt.Root()
    noteNode1 = nt.NoteNode(parent,n1)
    assert(noteNode1.music_notation_repr == ([("D5","sharp",False)],4,0))

def test_noteNode2():
    n1 = m21.note.Note(nameWithOctave='D5',quarterLength=2)
    n1.tie = m21.tie.Tie('stop')
    #create noteNode
    parent = nt.Root()
    noteNode1 = nt.NoteNode(parent,n1)
    assert(noteNode1.music_notation_repr == ([("D5","None",True)],2,0))

def test_noteNode_size1():
    n1 = m21.note.Note(nameWithOctave='D5',quarterLength=2)
    n1.tie = m21.tie.Tie('stop')
    #create noteNode
    parent = nt.Root()
    noteNode1 = nt.NoteNode(parent,n1)
    assert(noteNode1.subtree_size()== 2 )

def test_noteNode_size2():
    n1 = m21.note.Note(nameWithOctave='D#5',quarterLength=1.75)
    n1.tie = m21.tie.Tie('start')
    #create noteNode
    parent = nt.Root()
    noteNode1 = nt.NoteNode(parent,n1)
    assert(noteNode1.subtree_size()== 4 )

def test_noteNode_size3():
    d = m21.duration.Duration(1.5)
    n1 = m21.chord.Chord(['D', 'F#', 'A'],duration=d)
    #create noteNode
    parent = nt.Root()
    noteNode1 = nt.NoteNode(parent,n1)
    assert(noteNode1.subtree_size()== 5 )

def test_noteNode_size4():
    n1 = m21.note.Note(nameWithOctave='D5')
    n2 = m21.note.Note(nameWithOctave='F#5')
    n2.tie = m21.tie.Tie('stop')
    n3 = m21.note.Note(nameWithOctave='G#5')
    d = m21.duration.Duration(1.75)
    chord = m21.chord.Chord([n1,n2,n3],duration=d)
    #create noteNode
    parent = nt.Root()
    noteNode1 = nt.NoteNode(parent,chord)
    assert(noteNode1.subtree_size()== 8 )
