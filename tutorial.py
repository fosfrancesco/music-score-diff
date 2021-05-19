import music21 as m21
from pathlib import Path
import lib.score_visualization as sv
import lib.m21utils as m21u
import lib.NotationLinear as nlin
import lib.score_comparison_lib as scl
import json

#load score1 in music21
score1_path = Path("test_scores/polyphonic_score_1a.mei")
with open(score1_path, 'r') as f:
    mei_string = f.read()
    conv = m21.mei.MeiToM21Converter(mei_string)
    score1 = conv.run()

#load score2 in music21
score2_path = Path("test_scores/polyphonic_score_1b.mei")
with open(score2_path, 'r') as f:
    mei_string = f.read()
    conv = m21.mei.MeiToM21Converter(mei_string)
    score2 = conv.run()

#build the linear representation of the score
score_lin1 = nlin.Score(score1)
score_lin2 = nlin.Score(score2)

#compute the complete score diff
op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)

#generate the list of annotations in json format
# operation_json = scl.op_list2json(op_list)
#save them to a file
# with open(Path('output/operations_test.json'), 'w') as outfile:
#     json.dump(operation_json, outfile)

#annotate the differences between the two scores (color the involved elements)
sv.annotate_differences(score1, score2, op_list)

sv.show_differences(score1, score2)
