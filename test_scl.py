import lib.score_comparison_lib as scl
from pathlib import Path
import lib.NotationTree as nt
import music21 as m21

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
    score_tree1 = nt.ScoreTrees(score1)
    score_tree2 = nt.ScoreTrees(score2)
    #compute the non common_subsequences
    part = 0
    non_common_subsequences = scl.non_common_subsequences(score_tree1.part_list[part], score_tree2.part_list[part])
    assert(1 == 1)



