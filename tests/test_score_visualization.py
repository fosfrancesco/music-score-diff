import music21 as m21
from pathlib import Path
import lib.score_visualization as sv
import lib.m21utils as m21u
import lib.NotationLinear as nlin
import lib.score_comparison_lib as scl


def test_json_production1():
    score1_path = Path("tests/test_scores/tie_score_2a.mei")
    with open(score1_path, "r") as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("tests/test_scores/tie_score_2b.mei")
    with open(score2_path, "r") as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    # build ScoreTrees
    score_lin1 = nlin.Score(score1)
    score_lin2 = nlin.Score(score2)
    # compute the complete score diff
    op_list, cost = scl.complete_scorelin_diff(score_lin1, score_lin2)
    operation_json = scl.op_list2json(op_list)
    assert len(operation_json) == 1
    sv.annotate_differences(score1, score2, op_list)
    # sv.show_differences(score1, score2)


def test_json_production2():
    score1_path = Path("tests/test_scores/polyphonic_score_2a.mei")
    with open(score1_path, "r") as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score1 = conv.run()
    score2_path = Path("tests/test_scores/polyphonic_score_2b.mei")
    with open(score2_path, "r") as f:
        mei_string = f.read()
        conv = m21.mei.MeiToM21Converter(mei_string)
        score2 = conv.run()
    # build ScoreTrees
    score_lin1 = nlin.Score(score1)
    score_lin2 = nlin.Score(score2)
    # compute the complete score diff
    op_list, cost = scl.complete_scorelin_diff(score_lin1, score_lin2)
    operation_json = scl.op_list2json(op_list)
    assert 1 == 1
    sv.annotate_differences(score1, score2, op_list)
    # sv.show_differences(score1, score2)


def test_json_production3():
    score1_path = Path("tests/test_scores/musicxml/articulation_score_1a.xml")
    score1 = m21.converter.parse(str(score1_path))
    score2_path = Path("tests/test_scores/musicxml/articulation_score_1b.xml")
    score2 = m21.converter.parse(str(score2_path))
    # build ScoreTrees
    score_lin1 = nlin.Score(score1)
    score_lin2 = nlin.Score(score2)
    # compute the complete score diff
    op_list, cost = scl.complete_scorelin_diff(score_lin1, score_lin2)
    operation_json = scl.op_list2json(op_list)
    assert 1 == 1
    sv.annotate_differences(score1, score2, op_list)
    # sv.show_differences(score1, score2)

