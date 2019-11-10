import lib.score_comparison_lib as scl

def test_lcs_diff():
    original = [1,2,3,4,5,6,7,8,9,10]
    compare_to = [0,0,2,3,4,5,6,4,5,9,10]
    diff_list, cost = scl.lcs_diff(original, compare_to)
    print(diff_list)


