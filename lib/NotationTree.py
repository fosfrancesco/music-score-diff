# from music21 import *
from lib.m21utils import get_enhance_beamings, get_notes, get_ties, get_tuplets_type, get_tuplets_info, generalNote_to_string, generalNote_to_string_with_pitch, generalNote_info
from fractions import Fraction

#Digraph and the show() function are not useful for the website, so they are commented to reduce the dependencies
from graphviz import Digraph


class AnnotatedNote:
    def __init__(self, note, is_tied, enhanced_beam_list, tuple_info = None):
        """
        A class with the purpose to extend music21 GeneralNote
        :param note: the music21 generalNote
        :param is_tied: boolean value that indicate if the note is tied to the previous
        :param enhanced_beam_list a list with beaming informations
        :tuple_info: a list with tuple info
        """
        self.note = note
        self.is_tied = is_tied
        self.grouping = enhanced_beam_list
        self.tuple_info = tuple_info

    def head_to_string(self):
        """
        Return the string representation of the notehead
        """
        #retrieve the notehead (or rest) type and dots
        out_string = generalNote_to_string_with_pitch(self.note)
        #now add the tie information
        if self.is_tied:
            out_string = "-" + out_string
        return out_string


class Node:
    def __init__(self, parent, type):
        """
        The generic Tree node class
        :param parent: a Node instance
        :param type: a String that can be "root", "internal", "note"
        """
        self.type = type
        self.children = [] #each child is a Node
        self.parent = parent
        self.duration = None #we initialize that when the tree is builded and complete
        self.subtree_hash = None #we initialize that when the tree is builded and complete
        if self.type != "root":
            parent.add_child(self) #add a child in the parent Node if the parent is not the root

    def get_parent(self):
        return self.parent

    def get_type(self):
        return self.type

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        """
        :return: an array of Node
        """
        return self.children

    def get_children_node(self):
        return [c for c in self.children]

    def get_duration(self):
        return self.duration

    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def to_string(self):
        """
        Return the string representation of the subtree under the Node
        This class is override in InternalNode and NoteNode to make the recursion stop
        """
        out_string= "("
        for c in self.get_children():
            out_string= out_string + c.to_string() + ","
        out_string = out_string[0:-1] #remove the last comma
        out_string += ")" #close the grouping
        return out_string

    def subtree_size(self):
        """
        Return the size (number of nodes) of the subtree under the node (taking into accunt the node)
        This class is override in NoteNode to make the recursion stop
        """
        size = 1
        for c in self.get_children():
            size+=c.subtree_size()
        return size

    def has_children(self):
        if len(self.children) == 0:
            return False
        else:
            return True
    
    def _all_nodes(self, node, children_list):
        for c in node.get_children_node():
            self._all_nodes(c, children_list)
        children_list.append(node)  # add the current node
        return children_list
    
    def get_subtree_nodes(self):
        return self._all_nodes(self, [])

    def get_note_nodes(self):
        return [n for n in self.get_subtree_nodes() if n.get_type() == "note"]

    def atomic(self):
        return len(self.children) == 0

    def not_atomic(self):
        return len(self.children) != 0
    
    def unary(self):
        return len(self.children) == 1

    def not_unary(self):
        return len(self.children) != 1
    
    def __eq__(self, other):
        return self.to_string() == other.to_string()


class Root(Node):
    def __init__(self):
        Node.__init__(self, None,"root")
        self.name = "Root"

    def get_parent(self):
        raise TypeError('Root nodes have no parent')


class InternalNode(Node):
    def __init__(self, parent, n_of_divisions):
        assert isinstance( n_of_divisions, str)
        Node.__init__(self, parent, "internal")
        self.n_of_divisions = n_of_divisions
        self.name = str(n_of_divisions) #for node2note comparison

    def get_n_of_divisions(self):
        return self.n_of_divisions

    def to_string(self):
        """
        Return the string representation of the subtree under the Node
        """
        out_string= str(self.n_of_divisions)
        return out_string + super(InternalNode, self).to_string()


class NoteNode(Node):
    def __init__(self, parent, note, is_tied):
        Node.__init__(self, parent, "note")
        self.note = note
        self.is_tied = is_tied
        self.name = self.to_string()

    def get_note(self):
        return self.note

    def get_is_tied(self):
        return self.is_tied
    
    def subtree_size(self):
        """
        Return 1 since the note node cannot have children
        """
        size = 1
        return size

    def to_string(self):
        """
        Returns:
            str -- the representation of notehead with ties and dots
        """
        if self.is_tied:
            return "-" + generalNote_to_string_with_pitch(self.note)
        else:
            return generalNote_to_string_with_pitch(self.note)


class NoteTree:
    def __init__(self, measure = None, tree_type = None):
        """
        :param measure: m21 measure
        :param type: either 'beams' or 'tuplets'
        """
        self.root = Root()
        self.tree_type = tree_type
        self.duration_initialized = False
        if measure is not None:
            self.note_list = get_notes(measure)
            if tree_type == 'beams':
                self.en_beam_list = get_enhance_beamings(self.note_list) #beams and type (type for note shorter than quarter notes)
                # print(self.en_beam_list)
                ties_list = get_ties(self.note_list)
                #create a list of notes with ties and beaming information attached
                self.annot_notes = []
                #create a fake tuple info in order to assign names
                self.tuple_info = get_enhance_beamings(self.note_list)
                for i in range(len(self.tuple_info)):
                    for ii in range(len(self.tuple_info[i])):
                        self.tuple_info[i][ii] = ""
                for i, n in enumerate(self.note_list):
                    self.annot_notes.append(AnnotatedNote(n, ties_list[i], self.en_beam_list[i],tuple_info = self.tuple_info[i]))
                self._recursive_tree_generation(self.annot_notes,self.root,0)
            elif tree_type == 'tuplets':
                self.tuplet_list = get_tuplets_type(self.note_list) #corrected tuplets (with "start" and "continue")
                ties_list = get_ties(self.note_list)
                self.tuple_info = get_tuplets_info(self.note_list)
                # create a list of notes with ties and tuplets information attached
                self.annot_notes = []
                for i, n in enumerate(self.note_list):
                    self.annot_notes.append(AnnotatedNote(n, ties_list[i], self.tuplet_list[i], tuple_info = self.tuple_info[i]))
                self._recursive_tree_generation(self.annot_notes, self.root, 0)
            else:
                raise TypeError("Invalid tree_type")

    def get_root(self):
        return self.root

    def get_nodes(self, local_root = None):
        if local_root is None:
            local_root = self.root
        return self._all_nodes(local_root, [])

    def get_note_nodes(self, local_root = None):
        if local_root is None:
            local_root = self.root
        return [n for n in self.get_nodes(local_root = local_root) if n.get_type() == "note"]

    def _all_nodes(self, node, children_list):
        for c in node.get_children_node():
            self._all_nodes(c, children_list)
        children_list.append(node)  # add the current node
        return children_list
    
    def __eq__(self, other):
        if not isinstance(other, NoteTree):
            return False
        else: 
            return(str(self) == str(other))

    #Comment to reduce the dependencies from graphviz
    def show(self, save=False, name = ""):
        """Print a graphical version of the tree"""
        tree_repr = Digraph(comment='Duration Tree')
        tree_repr.node("1", "root")  # the root
        self._recursive_tree_display(self.get_root(), tree_repr, "11")
        if save:
            tree_repr.render('test-output/' + str(self.tree_type) + name, view=True)
        return tree_repr

    def _recursive_tree_display(self, node, _tree, name):
        """The actual recursive function called by show() """
        for l in node.get_children():
            if l.get_type() == "note":  # if it is a leaf
                _tree.node(name, l.to_string(), shape='box')
                _tree.edge(name[:-1], name ,constraint='true')
                name = name[:-1] + str(int(name[-1]) + 1)
            else:
                _tree.node(name, str(l.get_n_of_divisions()))
                # _tree.node(name, str(l.get_duration()))
                _tree.edge(name[:-1], name, constraint='true')
                self._recursive_tree_display(l, _tree, name + "1")
                name = name[:-1] + str(int(name[-1]) + 1)

    def _recursive_tree_generation(self, annot_notes, local_root, depth):
        temp_int_node = None
        start_index = None
        stop_index = None
        for i, n in enumerate(annot_notes):
            if len(n.grouping[depth:]) == 0: #no beaming
                assert (start_index is None)
                assert (stop_index is None)
                NoteNode(local_root, n.note, n.is_tied)
            elif n.grouping[depth] == 'partial': #partial beaming
                assert (start_index is None)
                assert (stop_index is None)
                #there are more levels of beam otherwise we would be on the previous case
                temp_int_node = InternalNode(local_root, n.tuple_info[depth])
                self._recursive_tree_generation([n], temp_int_node, depth+1)
                temp_int_node = None
            elif n.grouping[depth] == 'start': #start of a beam
                assert (start_index is None)
                assert(stop_index is None)
                start_index = i
            elif n.grouping[depth] == 'continue':
                assert (start_index is not None)
                assert (stop_index is None)

            elif n.grouping[depth] == 'stop':
                assert (start_index is not None)
                assert (stop_index is None)
                stop_index = i
                temp_int_node = InternalNode(local_root, n.tuple_info[depth])
                self._recursive_tree_generation(annot_notes[start_index:stop_index+1],temp_int_node, depth+1)
                #reset the variables
                temp_int_node = None
                start_index = None
                stop_index = None

    def compute_internal_node_duration(self):
        self.duration_initialized = True
        self._recursive_compute_duration(self.root)

    def _recursive_compute_duration(self,local_root):
        if local_root.get_type() == "note":
            local_root.duration = Fraction(local_root.note.duration.quarterLength)
            return local_root.duration
        else:
            local_root.duration = Fraction(sum([self._recursive_compute_duration(child) for child in local_root.get_children()]))
            return local_root.duration
    
    def to_string(self):
        """
        Returns the string unique representation of the tree
        """
        return self.root.to_string()

    def __repr__(self):
        return  self.root.to_string()

    def __str__(self):
        return  self.root.to_string()


class FullNoteTree:
    def __init__(self,measure, bar_reference = None, mei_id = None ):
        self.beams_tree = NoteTree(measure = measure, tree_type='beams')
        self.tuplets_tree = NoteTree(measure = measure, tree_type='tuplets')
        self.en_beam_list = self.beams_tree.en_beam_list
        self.tuplets_list = self.tuplets_tree.tuplet_list
        self.bar_reference = bar_reference
        self.mei_id = mei_id
    
    def __eq__(self, other):
        if not isinstance(other, FullNoteTree):
            return False
        else: 
            return (self.beams_tree == other.beams_tree) and (self.tuplets_tree == other.tuplets_tree)
    
    def subtree_size(self):
        ######################to update with also the tuplet tree############
        ######################################################################
        return self.beams_tree.root.subtree_size() 


    # Comment to reduce dependencies (from graphviz)
    def show(self, name=""):
        self.beams_tree.show(name=name)
        self.tuplets_tree.show(name=name)

    def __repr__(self):
        return str((str(self.beams_tree), str(self.tuplets_tree)))
    
    def __str__(self):
        return str((str(self.beams_tree), str(self.tuplets_tree)))


class MonophonicScoreTrees:
    def __init__(self,score):
        """
        Take a monophonic music21 score and store it a sequence of Full Trees
        Arguments:
            score {[music21 score]} a monofonic music21 score
        Raises:
            Exception -- [if there is more than 1 part]
            Exception -- [if the part has more than 1 voice]
        """
        self.measuresTrees = [] #contains a FullNoteTree for each measure
        if len(score.parts) !=1: #check that the score have just one part
            raise Exception("The score have more than one part")
        for measure_index, measure in enumerate(score.parts[0].getElementsByClass('Measure')):
            if len(measure.voices) == 0:  # there is a single Voice ( == for the library there are no voices)
                self.measuresTrees.append(FullNoteTree(measure,bar_reference=measure_index, mei_id=[note.id for note in get_notes(measure)]))
            else:  # there are multiple voices (or an array with just one voice)
                if len(measure.voices) !=1:
                    raise Exception("The part 1 has more than one voice")
                for voice in measure.voices:
                    self.measuresTrees.append(FullNoteTree(voice, bar_reference=measure_index, mei_id=[note.id for note in get_notes(voice)]))

    def __eq__(self,other): 
        if not isinstance(other, MonophonicScoreTrees):
            return False
        else:
            if len(self.measuresTrees)!= len(other.measuresTrees): #chek if they have the same number of measures
                return False
            for fnt in zip (self.measuresTrees,other.measuresTrees): #check if FullNoteTree are the same for each bar
                if fnt[0] != fnt[1]:
                    return False
            return True

class ScoreTrees:
    def __init__(self,score):
        """
        Take a music21 score and store it a sequence of Full Trees
        The hierarchy is "score -> parts ->measures -> voices -> notes"
        Arguments:
            score {[music21 score]} a music21 score
        """
        self.part_list = [] #contains a FullNoteTree for each measure
        print("#parts = {}".format(len(score.parts)))
        for part_index, part in enumerate(score.parts.stream()):
            print("#measure for part {} = {}".format(part_index, len(part.getElementsByClass('Measure'))))
            tree_part = [] #tree part is a list of tree measures
            for measure_index, measure in enumerate(part.getElementsByClass('Measure')):
                tree_measure = [] #measure is a list of voices (each represented by a FNT)
                if len(measure.voices) == 0:  # there is a single Voice ( == for the library there are no voices)
                    print("Part {}, measure {}".format(part_index,measure_index))
                    tree_measure.append(FullNoteTree(measure,bar_reference=measure_index, mei_id=[note.id for note in get_notes(measure)]))
                else:  # there are multiple voices (or an array with just one voice)
                    for voice in measure.voices:
                        print("Part {}, measure {}".format(part_index,measure_index))
                        tree_measure.append(FullNoteTree(voice, bar_reference=measure_index, mei_id=[note.id for note in get_notes(voice)]))
                tree_part.append(tree_measure) #add the measures to the tree part
            self.part_list.append(tree_part) #add the complete part to part_list

    # def __eq__(self,other):
    #     if not isinstance(other, MonophonicScoreTrees):
    #         return False
    #     else:
    #         if len(self.measuresTrees)!= len(other.measuresTrees): #check if they have the same number of measures
    #             return False
    #         for fnt in zip (self.measuresTrees,other.measuresTrees): #check if FullNoteTree are the same for each bar
    #             if fnt[0] != fnt[1]:
    #                 return False
    #         return True

class ScoreTrees_single_voice:
    def __init__(self,score):
        """
        Take a music21 score and store it a sequence of Full Trees
        The hierarchy is "score -> parts ->measures -> voices -> notes"
        Arguments:
            score {[music21 score]} a music21 score
        """
        self.part_list = [] #contains a FullNoteTree for each measure
        print("#parts = {}".format(len(score.parts)))
        for part_index, part in enumerate(score.parts.stream()):
            print("#measure for part {} = {}".format(part_index, len(part.getElementsByClass('Measure'))))
            tree_part = [] #tree part is a list of single voices measures (each represented by a FNT)
            for measure_index, measure in enumerate(part.getElementsByClass('Measure')):
                if len(measure.voices) == 0:  # there is a single Voice ( == for the library there are no voices)
                    print("Part {}, measure {}".format(part_index,measure_index))
                    tree_part.append(FullNoteTree(measure,bar_reference=measure_index, mei_id=[note.id for note in get_notes(measure)]))
                else:  # there are multiple voices (or an array with just one voice)
                    for voice in measure.voices[0:1]:
                        print("Part {}, measure {}".format(part_index,measure_index))
                        tree_part.append(FullNoteTree(voice, bar_reference=measure_index, mei_id=[note.id for note in get_notes(voice)]))
            self.part_list.append(tree_part) #add the complete part to part_list
