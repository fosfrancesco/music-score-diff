import json
import operator
import lib.NotationTree as nt
import lib.m21utils as m21u
import copy

#memoizers to speed up the recursive computation
def memoize_inside_bars_diff(func):
    mem = {}
    def memoizer(original, compare_to):
        key = str(original) + str(compare_to)
        if key not in mem:
            mem[key] = func(original, compare_to)
        return copy.deepcopy(mem[key])
    return memoizer
def memoize_block_diff(func):
    mem = {}
    def memoizer(original, compare_to):
        key = str(original) + str(compare_to)
        if key not in mem:
            mem[key] = func(original, compare_to)
        return copy.deepcopy(mem[key])
    return memoizer
def memoize_lcs_diff(func):
    mem = {}
    def memoizer(original, compare_to):
        key = str(original) + str(compare_to)
        if key not in mem:
            mem[key] = func(original, compare_to)
        return copy.deepcopy(mem[key])
    return memoizer


# algorithm in section 3.2 
# INPUT: two lists of notationTree hashes (one part from the first score and one part from the second score)
# OUTPUT: the allignment between the two lists
@memoize_lcs_diff
def lcs_diff (original, compare_to):
    if (len(original) == 0 and len(compare_to)== 0):
        cost = 0
        return [], cost
    elif (len(original) == 0):
        cost = 0
        op_list = []
        #iterate on the rest instead of go recurively (for performances)
        for e in compare_to[::-1]: #reverse to simulate the recurstion
            op_list.append(("comparetostep",None,e,0))
        return op_list, cost
    elif (len(compare_to) == 0):
        cost = 0
        op_list = []
        #iterate on the rest instead of go recurively (for performances)
        for e in original[::-1]: #reverse to simulate the recurstion
            op_list.append(("originalstep",e,None,0))
        return op_list, cost
    elif original[0] == compare_to[0]:
        op_list, cost = lcs_diff(original[1:], compare_to[1:]) 
        cost += 1
        op_list.append(("equal",original[0], compare_to[0], 1))
        return op_list, cost
    else: 
        #compute the cost and the op_list for the many possibilities of recursion
        cost= {}
        op_list = {}
        #original-step
        op_list["originalstep"], cost["originalstep"]= lcs_diff(original[1:], compare_to) 
        cost["originalstep"]+= 0
        op_list["originalstep"].append(("originalstep",original[0], None, 0))
        #compare_to-step
        op_list["comparetostep"], cost["comparetostep"]= lcs_diff(original, compare_to[1:])
        cost["comparetostep"] += 0
        op_list["comparetostep"].append(("comparetostep",None, compare_to[0], 0))
        
        #compute the maximum of the possibilities
        max_key = max(cost, key=cost.get)
        out = op_list[max_key], cost[max_key]
        return out


# get the list of non common subsequence from the algorithm lcs_diff
# that will be used to proceed further
def non_common_subsequences(original,compare_to):
    #get the list of operations
    op_list, cost = lcs_diff(original,compare_to)
    #retrieve the non common subsequences
    non_common_subsequences= []
    non_common_subsequences.append({"original":[],"compare_to":[]})
    ind = 0
    for op in op_list[::-1]:
        if op[0] == "equal":
            non_common_subsequences.append({"original":[],"compare_to":[]})
            ind +=1
        elif op[0] == "originalstep":
            non_common_subsequences[ind]["original"].append(op[1])
        elif op[0] == "comparetostep":
            non_common_subsequences[ind]["compare_to"].append(op[2])
    #remove the empty dict from the list
    non_common_subsequences = [s for s in non_common_subsequences if s!={"original":[],"compare_to":[]} ]
    return non_common_subsequences


            


        


@memoize_block_diff
def block_diff (original, compare_to):
    if len(original) == 0 and len(compare_to) == 0:
        return [("empty",original,compare_to,0)], 0
    elif (len(original) == 0):
        cost = sum([tree.subtree_size() for voice in compare_to for tree in voice])
        return [("blockins",original,compare_to,cost)], cost
    elif (len(compare_to) == 0):
        cost = sum([tree.subtree_size() for voice in original for tree in voice])
        return [("blockdel",original,compare_to,cost)], cost
    else: 
        #compute the cost and the op_list for the many possibilities of recursion
        cost= {}
        op_list = {}
        #del-bar
        op_list["delbar"], cost["delbar"]= block_diff(original[1:], compare_to) 
        cost["delbar"]+= sum([voice.subtree_size() for voice in original[0]])
        op_list["delbar"].append(("delbar",original[0], None, sum([voice.subtree_size() for voice in original[0]])))
        #ins-bar
        op_list["insbar"], cost["insbar"]= block_diff(original, compare_to[1:])
        cost["insbar"] += sum([voice.subtree_size() for voice in compare_to[0]])
        op_list["insbar"].append(("insbar",None, compare_to[0], sum([voice.subtree_size() for voice in compare_to[0]])))
        #edit-bar
        op_list["editbar"], cost["editbar"]= block_diff(original[1:], compare_to[1:])
        if original[0] == compare_to[0]: #to avoid perform the inside_bars_diff if it's not needed
            inside_bar_op_list = []
            inside_bar_cost = 0
        else: 
            #consider all possible voice couples (one from score1 and one from score2)
            possible_couples = [(v1,v2) for v1 in original[0] for v2 in compare_to[0]]
            #compute the cost for all couples
            inside_bar_op_list_couples = []
            inside_bar_cost_couples = []
            for c in possible_couples:
                inside_bar_op_list_temp, inside_bar_cost_temp = inside_bars_diff(c[0].beams_tree.root.children, c[1].beams_tree.root.children) 
                #############to update with also the tuplet trees##########################
                ##########################################################################
                inside_bar_op_list_couples.append(inside_bar_op_list_temp)
                inside_bar_cost_couples.append(inside_bar_cost_temp)
            #select the couple that yield the minimum cost
            min_index = inside_bar_cost_couples.index(min(inside_bar_cost_couples))
            inside_bar_op_list = inside_bar_op_list_couples[min_index]
            inside_bar_cost = inside_bar_cost_couples[min_index]
        cost["editbar"] += inside_bar_cost
        op_list["editbar"].append(("editbar",original[0], compare_to[0], inside_bar_cost))
        op_list["editbar"].extend(inside_bar_op_list)
        #compute the minimum of the possibilities
        min_key = min(cost, key=cost.get)
        out = op_list[min_key], cost[min_key]
        return out



@memoize_inside_bars_diff
def inside_bars_diff (original, compare_to):
    #else compute it
    if len(original) == 0 and len(compare_to) == 0:
        return [("empty",original,compare_to,0)], 0
    elif (len(original) == 0):
        cost = sum([tree.subtree_size() for tree in compare_to])
        return [("forestins",original,compare_to,cost)], cost
    elif (len(compare_to) == 0):
        cost = sum([tree.subtree_size() for tree in original])
        return [("forestdel",original,compare_to,cost)], cost
    else: 
        #compute the cost and the op_list for the many possibilities of recursion
        cost= {}
        op_list = {}
        op_list["del"], cost["del"]= inside_bars_diff(original[1:], compare_to) 
        cost["del"]+= original[0].subtree_size()
        op_list["del"].append(("del",original[0], None, original[0].subtree_size()))
        op_list["ins"], cost["ins"]= inside_bars_diff(original, compare_to[1:])
        cost["ins"] += compare_to[0].subtree_size()
        op_list["ins"].append(("ins",None, compare_to[0], compare_to[0].subtree_size()))
        if (original[0].not_atomic() and compare_to[0].atomic()) or (original[0].unary() and compare_to[0].not_unary()):
            op_list["nodedel"], cost["nodedel"]= inside_bars_diff([c for c in original[0].children]+original[1:], compare_to) 
            cost["nodedel"] += 1
            op_list["nodedel"].append(("nodedel",original[0], None, 1))
        if (original[0].atomic() and compare_to[0].not_atomic()) or (original[0].not_unary() and compare_to[0].unary()):
            op_list["nodeins"], cost["nodeins"]= inside_bars_diff(original, [c for c in compare_to[0].children]+compare_to[1:]) 
            cost["nodeins"] += 1
            op_list["nodeins"].append(("nodeins",None, compare_to[0], 1))
        if (original[0].not_atomic() and compare_to[0].not_atomic()): #desc
            op_list["desc"], cost["desc"]= inside_bars_diff([c for c in original[0].children]+original[1:], [c for c in compare_to[0].children]+compare_to[1:])
            cost["desc"]  += 0 #to update for many tipes of arch
            op_list["desc"].append(("desc",original[0], compare_to[0], 0))
        if (original[0].atomic() and compare_to[0].atomic()): #leaf/sub
            op_list["leaf"], cost["leaf"]= inside_bars_diff(original[1:],compare_to[1:]) 
            leaf_op, leaf_cost = evaluate_noteNode_diff(original[0],compare_to[0])
            cost["leaf"] += leaf_cost 
            op_list["leaf"].extend(leaf_op)
        #compute the minimum of the possibilities
        min_key = min(cost, key=cost.get)
        out = op_list[min_key], cost[min_key]
        return out


def evaluate_noteNode_diff(noteNode1,noteNode2):
    #############work only with single notes and rests, not with chords#########
    """
        Evaluate how much one NoteNode is similar to another.
        0 is if they are equal and 4 is the maximum dissimilarity
        In particular 3 fields are compared with different weights:
            - note pitches (a chord have multiple pitches)
            - note head (black, white, long, etc.)
            - note dots
            - note ties
        Every difference will count for 1 point of dissimilarity
        WARNING!! Chords are still not supported
    """
    if (type(noteNode1) is not nt.NoteNode) or (type(noteNode2) is not nt.NoteNode)  : #if we are comparing object that are not NoteNode, fail
        raise TypeError("The type of noteNode1 and noteNode2  is {} and {}, but it must be NoteNode".format(type(noteNode1), type(noteNode2)))
    else: #we are comparing two NoteNode
        diff = 0
        op_list = [] #the list of differences between the two notes
        noteNode1_info = noteNode1.music_notation_repr
        noteNode2_info= noteNode2.music_notation_repr
        TO IMPLEMENT THE EDIT FOR NOTES AND THEN CHANGE THE DICT TO NORMAL LIST INDEX
        # add for the pitches
        if noteNode1_info[0][0][0] != noteNode2_info["pitches"][0][0]: #if the note pitch is different
            diff += 1
            op_list.append(("pitch",noteNode1,noteNode2,1))
        if noteNode1_info["pitches"][0][1] != noteNode2_info["pitches"][0][1]: #if the accident is different
            diff += 1
            if noteNode1_info["pitches"][0][1] is None:
                assert noteNode2_info["pitches"][0][1] is not None
                op_list.append(("accidentins",None,noteNode2,1))
            elif noteNode2_info["pitches"][0][1] is None:
                assert noteNode1_info["pitches"][0][1] is not None
                op_list.append(("accidentdel",noteNode1,None,1))
            else: #a different tipe of alteration is present
                op_list.append(("accidentedit",noteNode1,noteNode2,1))
        #add for the notehead
        if noteNode1_info["noteHead"] != noteNode2_info["noteHead"]: #add for the notehead
            diff += 1
            op_list.append(("headedit",noteNode1,noteNode2,1))
        #add for the dots
        dots_diff = abs(noteNode1_info["dots"]- noteNode2_info["dots"])
        diff += dots_diff
        if noteNode1_info["dots"] > noteNode2_info["dots"]:
            op_list.append(("dotsdel",noteNode1,None,dots_diff))
        elif noteNode1_info["dots"] < noteNode2_info["dots"]:
            op_list.append(("dotsins",None,noteNode2,dots_diff))
        #add for the ties
        if noteNode1.is_tied != noteNode2.is_tied: #exclusive or. Add if one is tied and not the other
            ################probably to revise for chords
            diff += 1
            if noteNode1.is_tied:
                assert not noteNode2.is_tied
                op_list.append(("tiedel",noteNode1,None,1))
            elif noteNode2.is_tied:
                assert not noteNode1.is_tied
                op_list.append(("tieins",None,noteNode2,1))

        return op_list, diff

        
def evaluate_pitch_list_diff(pitchList1, pitchList2):
    #chords are evaluate with levenstain distance, they are already sorted diatonically
    cost= pitches_iterative_levenshtein(pitchList1, pitchList2)
    return cost 

def pitches_iterative_levenshtein(s, t):
    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings 
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = i
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i   
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                 dist[row][col-1] + 1,      # insertion
                                 dist[row-1][col-1] + cost) # substitution
    return dist[row][col]

def iterative_levenshtein(s, t):
    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings 
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = i
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i   
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                 dist[row][col-1] + 1,      # insertion
                                 dist[row-1][col-1] + cost) # substitution
    return dist[row][col]


def score_diff(score1,score2):
    """
        Return a edite distance between the hash of the trees created by each bar in the scores. 
    """
    #get the ScoreMeasuresTrees from each score
    scoreTrees1 = nt.MonophonicScoreTrees(score1)
    scoreTrees2 = nt.MonophonicScoreTrees(score2)
    print("Score1 MeasuresTrees")
    print([t.en_beam_list for t in scoreTrees1.measuresTrees])
    print("Score2 MeasuresTrees")
    print([t.en_beam_list for t in scoreTrees2.measuresTrees])
    out = block_diff(scoreTrees1.measuresTrees, scoreTrees2.measuresTrees)
    return out


def polyph_score_diff(score1,score2):
    """
        Return a edite distance between the hash of the trees created by each bar in the scores. 
        The edite distance uses only insertion and deletion (not modifications)
    """
    #get the ScoreTree from each score
    scoreTrees1 = nt.ScoreTrees_single_voice(score1)
    scoreTrees2 = nt.ScoreTrees_single_voice(score2)
    total_operations = []
    total_cost = 0
    #for now we assume to have an equal number of parts
    assert(len(scoreTrees1.part_list)==len(scoreTrees2.part_list))
    number_of_parts = len(scoreTrees1.part_list)
    for part_index in range(number_of_parts):
        #we evaluate the list of voices because it make sense from music perspective
        #we hope the order is the same for now
        seq1=scoreTrees1.part_list[part_index]
        seq2=scoreTrees2.part_list[part_index]
        operations, cost = block_diff(seq1,seq2) #part is a seq of measures
        ############################## to change to retrieve more than one path
        total_operations.extend(operations)
        #############################
        total_cost += cost        
    return total_operations, total_cost