import music21 as m21
from pathlib import Path
import lib.score_visualization as sv
import lib.m21utils as m21u
import lib.NotationLinear as nlin
import lib.score_comparison_lib as scl

def test_annotation_production1():
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
    score_lin1 = nlin.ScoreLinear(score1)
    score_lin2 = nlin.ScoreLinear(score2)
    #compute the complete score diff
    op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
    ann1, ann2 = sv.oplist2annotations(op_list)
    sv.produce_annnot_svg(score1_path,ann1,out_path=Path("output/monophonic_score_1a.svg"))
    sv.produce_annnot_svg(score2_path,ann2,out_path=Path("output/monophonic_score_1b.svg"))
    assert(1==1)


def test_annotation_production2():
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
    score_lin1 = nlin.ScoreLinear(score1)
    score_lin2 = nlin.ScoreLinear(score2)
    #compute the complete score diff
    op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
    ann1, ann2 = sv.oplist2annotations(op_list)
    sv.produce_annnot_svg(score1_path,ann1,out_path=Path("output/multivoice_score_1a.svg"))
    sv.produce_annnot_svg(score2_path,ann2,out_path=Path("output/multivoice_score_1b.svg"))
    assert(1==1)

def test_annotation_production3():
    score1_path = Path("test_scores/chord_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/chord_score_1b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build ScoreTrees
    score_lin1 = nlin.ScoreLinear(score1)
    score_lin2 = nlin.ScoreLinear(score2)
    #compute the complete score diff
    op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
    ann1, ann2 = sv.oplist2annotations(op_list)
    sv.produce_annnot_svg(score1_path,ann1,out_path=Path("output/chord_score_1a.svg"))
    sv.produce_annnot_svg(score2_path,ann2,out_path=Path("output/chord_score_1b.svg"))
    assert(1==1)

def test_annotation_production4():
    score1_path = Path("test_scores/chord_score_2a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/chord_score_2b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build ScoreTrees
    score_lin1 = nlin.ScoreLinear(score1)
    score_lin2 = nlin.ScoreLinear(score2)
    #compute the complete score diff
    op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
    ann1, ann2 = sv.oplist2annotations(op_list)
    sv.produce_annnot_svg(score1_path,ann1,out_path=Path("output/chord_score_2a.svg"))
    sv.produce_annnot_svg(score2_path,ann2,out_path=Path("output/chord_score_2b.svg"))
    assert(1==1)


def test_annotation_production4():
    score1_path = Path("test_scores/chord_score_3a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/chord_score_3b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build ScoreTrees
    score_lin1 = nlin.ScoreLinear(score1)
    score_lin2 = nlin.ScoreLinear(score2)
    #compute the complete score diff
    op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
    ann1, ann2 = sv.oplist2annotations(op_list)
    sv.produce_annnot_svg(score1_path,ann1,out_path=Path("output/chord_score_3a.svg"))
    sv.produce_annnot_svg(score2_path,ann2,out_path=Path("output/chord_score_3b.svg"))
    assert(1==1)

def test_annotation_production5():
    score1_path = Path("test_scores/tie_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/tie_score_1b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build ScoreTrees
    score_lin1 = nlin.ScoreLinear(score1)
    score_lin2 = nlin.ScoreLinear(score2)
    #compute the complete score diff
    op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
    ann1, ann2 = sv.oplist2annotations(op_list)
    sv.produce_annnot_svg(score1_path,ann1,out_path=Path("output/tie_score_1a.svg"))
    sv.produce_annnot_svg(score2_path,ann2,out_path=Path("output/tie_score_1b.svg"))
    assert(1==1)

def test_annotation_production6():
    score1_path = Path("test_scores/tuplet_score_1a.mei")
    with open(score1_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("test_scores/tuplet_score_1b.mei")
    with open(score2_path, 'r') as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    #build ScoreTrees
    score_lin1 = nlin.ScoreLinear(score1)
    score_lin2 = nlin.ScoreLinear(score2)
    #compute the complete score diff
    op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
    ann1, ann2 = sv.oplist2annotations(op_list)
    sv.produce_annnot_svg(score1_path,ann1,out_path=Path("output/tuplet_score_1a.svg"))
    sv.produce_annnot_svg(score2_path,ann2,out_path=Path("output/tuplet_score_1b.svg"))
    assert(1==1)

def test_annotation_production7():
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
    score_lin1 = nlin.ScoreLinear(score1)
    score_lin2 = nlin.ScoreLinear(score2)
    #compute the complete score diff
    op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
    ann1, ann2 = sv.oplist2annotations(op_list)
    sv.produce_annnot_svg(score1_path,ann1,out_path=Path("output/polyphonic_score_1a.svg"))
    sv.produce_annnot_svg(score2_path,ann2,out_path=Path("output/polyphonic_score_1b.svg"))
    assert(1==1)