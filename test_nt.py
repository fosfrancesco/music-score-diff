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
