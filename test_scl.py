import lib.score_comparison_lib as scl
from pathlib import Path
import lib.NotationLinear as nlin
import music21 as m21
from collections import Counter

def test_non_common_subsequences1():
    original = [1,2,3,4,5,6,7,8,9,10]
    compare_to = [0,0,2,3,4,5,6,4,5,9,10]
    non_common_subsequences = scl.non_common_subsequences(original, compare_to)
    expected_result = [{"original":[1],"compare_to":[0,0]},
        {"original":[7,8],"compare_to":[4,5]},
        ]  
    assert(non_common_subsequences== expected_result)

def test_non_common_subsequences2():
    original = [0,1,2,3]
    compare_to = [5,7,8,6,3]
    non_common_subsequences = scl.non_common_subsequences(original, compare_to)
    expected_result = [{"original":[0,1,2],"compare_to":[5,7,8,6]}]  
    assert(non_common_subsequences== expected_result)

def test_non_common_subsequences3():
    original = [0,1,2,3,4]
    compare_to = [0,1,2]
    non_common_subsequences = scl.non_common_subsequences(original, compare_to)
    expected_result = [{"original":[3,4],"compare_to":[]}]  
    assert(non_common_subsequences== expected_result)

def test_non_common_subsequences4():
    original = []
    compare_to = [0,1,2]
    non_common_subsequences = scl.non_common_subsequences(original, compare_to)
    expected_result = [{"original":[],"compare_to":[0,1,2]}]  
    assert(non_common_subsequences== expected_result)

def test_non_common_subsequences5():
    original = [0,1,2]
    compare_to = [0,1,2]
    non_common_subsequences = scl.non_common_subsequences(original, compare_to)
    expected_result = []  
    assert(non_common_subsequences== expected_result)

def test_non_common_subsequences6():
    #import scores
    score1_path = Path("test_scores/polyphonic_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/polyphonic_score_1b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build ScoreTrees
    score_tree1 = nlin.Score(score1)
    score_tree2 = nlin.Score(score2)
    #compute the non common_subsequences for part 0
    part = 0
    non_common_subsequences = scl.non_common_subsequences(score_tree1.part_list[part].bar_list, score_tree2.part_list[part].bar_list)
    assert(len(non_common_subsequences)==2)


def test_non_common_subsequences7():
    #import scores
    score1_path = Path("test_scores/monophonic_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/monophonic_score_1b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build ScoreTrees
    score_tree1 = nlin.Score(score1)
    score_tree2 = nlin.Score(score2)
    #compute the non common_subsequences for part 0
    part = 0
    non_common_subsequences = scl.non_common_subsequences(score_tree1.part_list[part].bar_list, score_tree2.part_list[part].bar_list)
    expected_non_common1 = {
        "original": [score_tree1.part_list[0].bar_list[1]],
        "compare_to": [score_tree2.part_list[0].bar_list[1]]
    }
    expected_non_common2 = {
        "original": [score_tree1.part_list[0].bar_list[5],score_tree1.part_list[0].bar_list[6],score_tree1.part_list[0].bar_list[7],score_tree1.part_list[0].bar_list[8]],
        "compare_to": [score_tree2.part_list[0].bar_list[5],score_tree2.part_list[0].bar_list[6],score_tree2.part_list[0].bar_list[7]]
    }
    assert(len(non_common_subsequences)==2)
    assert(non_common_subsequences[0] == expected_non_common1)
    assert(non_common_subsequences[1] == expected_non_common2)    

def test_non_common_subsequences8():
    #import scores
    score1_path = Path("test_scores/monophonic_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/monophonic_score_1b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build Score
    score_lin1 = nlin.Score(score1)
    score_lin2 = nlin.Score(score2)
    #compute the non common_subsequences for part 0
    part = 0
    non_common_subsequences = scl.non_common_subsequences(score_lin1.part_list[part].bar_list, score_lin2.part_list[part].bar_list)
    expected_non_common1 = {
        "original": [score_lin1.part_list[0].bar_list[1]],
        "compare_to": [score_lin2.part_list[0].bar_list[1]]
    }
    expected_non_common2 = {
        "original": [score_lin1.part_list[0].bar_list[5],score_lin1.part_list[0].bar_list[6],score_lin1.part_list[0].bar_list[7],score_lin1.part_list[0].bar_list[8]],
        "compare_to": [score_lin2.part_list[0].bar_list[5],score_lin2.part_list[0].bar_list[6],score_lin2.part_list[0].bar_list[7]]
    }
    assert(len(non_common_subsequences)==2)
    assert(non_common_subsequences[0] == expected_non_common1)
    assert(non_common_subsequences[1] == expected_non_common2)  

def test_pitches_diff1():
    n1 = m21.note.Note(nameWithOctave='D#5',quarterLength=1)
    n2 = m21.note.Note(nameWithOctave='D--5',quarterLength=1)
    #create AnnotatedNotes
    note1 = nlin.AnnotatedNote(n1,[],[])
    note2 = nlin.AnnotatedNote(n2,[],[])
    #pitches to compare
    pitch1 = note1.pitches[0]
    pitch2 = note2.pitches[0]
    #compare
    op_list, cost = scl.pitches_diff(pitch1,pitch2,note1,note2,(0,0))
    assert(cost == 1)
    assert(op_list == [("accidentedit",note1,note2,1,(0,0))])

def test_pitches_diff2():
    n1 = m21.note.Note(nameWithOctave='E5',quarterLength=2)
    n2 = m21.note.Note(nameWithOctave='D--5',quarterLength=1)
    note1 = nlin.AnnotatedNote(n1,[],[])
    note2 = nlin.AnnotatedNote(n2,[],[])
    #pitches to compare
    pitch1 = note1.pitches[0]
    pitch2 = note2.pitches[0]
    #compare
    op_list, cost = scl.pitches_diff(pitch1,pitch2,note1,note2,(0,0))
    assert(cost == 2)
    assert(len(op_list)==2)
    assert(("accidentins",None,note2,1,(0,0)) in op_list)
    assert(("pitchnameedit", note1,note2,1,(0,0)) in op_list)

def test_pitches_diff3():
    n1 = m21.note.Note(nameWithOctave='D--5',quarterLength=2)
    n1.tie = m21.tie.Tie('stop')
    n2 = m21.note.Rest(quarterLength=0.5)
    note1 = nlin.AnnotatedNote(n1,[],[])
    note2 = nlin.AnnotatedNote(n2,[],[])
    #pitches to compare
    pitch1 = note1.pitches[0]
    pitch2 = note2.pitches[0]
    #compare
    op_list, cost = scl.pitches_diff(pitch1,pitch2,note1,note2,(0,0))
    assert(cost == 3)
    assert(len(op_list)==3)
    assert(("accidentdel",note1,None,1,(0,0)) in op_list)
    assert(("pitchtypeedit", note1,note2,1,(0,0)) in op_list)
    assert(("tiedel", note1,None,1,(0,0)) in op_list)

def test_pitches_diff4():
    n1 = m21.note.Note(nameWithOctave='D5',quarterLength=2)
    n1.tie = m21.tie.Tie('stop')
    n2 = m21.note.Note(nameWithOctave='D#5',quarterLength=3)
    n2.tie = m21.tie.Tie('stop')
    note1 = nlin.AnnotatedNote(n1,[],[])
    note2 = nlin.AnnotatedNote(n2,[],[])
    #pitches to compare
    pitch1 = note1.pitches[0]
    pitch2 = note2.pitches[0]
    #compare
    op_list, cost = scl.pitches_diff(pitch1,pitch2,note1,note2,(0,0))
    assert(cost == 1)
    assert(len(op_list)==1)
    assert(("accidentins",None,note2,1,(0,0)) in op_list)

def test_block_diff1():
    score1_path = Path("test_scores/monophonic_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/monophonic_score_1b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build ScoreTrees
    score_lin1 = nlin.Score(score1)
    score_lin2 = nlin.Score(score2)
#   compute the blockdiff between all the bars (just for test, in practise we will run on non common subseq)
    op_list, cost = scl.block_diff_lin(score_lin1.measures_from_part(0),score_lin2.measures_from_part(0))
    assert(cost==8)

def test_multivoice_scorelin_diff1():
    score1_path = Path("test_scores/multivoice_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/multivoice_score_1b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build ScoreTrees
    score_lin1 = nlin.Score(score1)
    score_lin2 = nlin.Score(score2)
    #compute the complete score diff
    op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
    assert(cost==8)

def test_complete_scorelin_diff1():
    score1_path = Path("test_scores/monophonic_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/monophonic_score_1b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build ScoreTrees
    score_lin1 = nlin.Score(score1)
    score_lin2 = nlin.Score(score2)
    #compute the complete score diff
    op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
    assert(cost==8)




