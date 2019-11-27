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

#add the correct folder for resourches. Uncomment if needed
# sv.setResourchesPath(Path("C:/Users/example/Desktop/verovio/data" ))

#build the linear representation of the score
score_lin1 = nlin.Score(score1)
score_lin2 = nlin.Score(score2)

#compute the complete score diff
op_list, cost=scl.complete_scorelin_diff(score_lin1,score_lin2)
#generate the list of annotations in json format
operation_json = scl.op_list2json(op_list)
#save them to a file
with open(Path('output/operations_test.json'), 'w') as outfile:
    json.dump(operation_json, outfile)

#compute the annotations for the two scores
ann1, ann2 = sv.oplist2annotations(op_list)
#display the annotations on the scores (color the involved elements)
sv.produce_annnot_svg(score1_path,ann1,out_path=Path("output/test1.svg"))
sv.produce_annnot_svg(score2_path,ann2,out_path=Path("output/test2.svg"))