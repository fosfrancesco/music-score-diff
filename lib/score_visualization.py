import re
import subprocess
import music21 as m21
import verovio
from xml.etree import ElementTree as ET
import operator
from collections import Counter
import copy
import re
import subprocess

import lib.NotationLinear as nlin

INS_COLOR = "green"
DEL_COLOR = "red"
SUB_COLOR = "yellow"
#dictionary of useful tags
el_dict={
    "g": "{http://www.w3.org/2000/svg}g",
    "polygon" : "{http://www.w3.org/2000/svg}polygon",
    "use" : "{http://www.w3.org/2000/svg}use"
}

def oplist2annotations(operations):
    annotations1 = [] #for the score1
    annotations2 = [] #for the score2
    for op in operations:
        #bar
        if op[0] == "insbar":
            assert(type(op[2]) == list)
            id_list = [id for voice in op[2] for id in voice.get_note_id()]
            annotations2.extend([{"id": id_list, "color": INS_COLOR, "target": "bar"}])
        elif op[0] == "delbar":
            assert(type(op[1]) == list)
            id_list = [id for voice in op[1] for id in voice.get_note_id()]
            annotations1.extend([{"id": id_list, "color": INS_COLOR, "target": "bar"}])
        #voices
        if op[0] == "voiceins":
            assert(type(op[2]) == nlin.VoiceLinear)
            annotations2.extend([{"id": id, "color": INS_COLOR, "target": "note"} for id in op[2].get_note_id()])
        elif op[0] == "voicedel":
            assert(type(op[1]) == nlin.VoiceLinear)
            annotations1.extend([{"id": id, "color": DEL_COLOR, "target": "note"} for id in op[1].get_note_id()])
        #note
        elif op[0] == "noteins":
            assert(type(op[2])==nlin.AnnotatedNote)
            annotations2.extend([{"id": id, "color": INS_COLOR, "target": "note"} for id in op[2].get_note_id()])
        elif op[0] == "notedel":
            assert(type(op[1])==nlin.AnnotatedNote)
            annotations1.extend([{"id": id, "color": DEL_COLOR, "target": "note"} for id in op[1].get_note_id()])
        #pitch
        elif op[0] == "pitchnameedit":
            assert(type(op[1])==nlin.AnnotatedNote)
            assert(type(op[2])==nlin.AnnotatedNote)
            assert(len(op)==5) #the indices must be there
            annotations1.extend([{"id": id, "color": SUB_COLOR, "target": "notehead","head_id":op[4][0]} for id in op[1].get_note_id()])
            annotations2.extend([{"id": id, "color": SUB_COLOR, "target": "notehead","head_id":op[4][1]} for id in op[2].get_note_id()])
        elif op[0] == "inspitch":
            assert(type(op[2])==nlin.AnnotatedNote)
            assert(len(op)==5) #the indices must be there
            annotations2.extend([{"id": id, "color": INS_COLOR, "target": "notehead","head_id":op[4][1]} for id in op[2].get_note_id()])
        elif op[0] == "delpitch":
            assert(type(op[1])==nlin.AnnotatedNote)
            assert(len(op)==5) #the indices must be there
            annotations1.extend([{"id": id, "color": DEL_COLOR, "target": "notehead","head_id":op[4][0]} for id in op[1].get_note_id()])
        #beam
        elif op[0] == "insbeam":
            assert(type(op[2])==nlin.AnnotatedNote)
            annotations2.extend([{"id": id, "color": INS_COLOR, "target":"beam"} for id in op[2].get_note_id()])
        elif op[0] == "delbeam":
            assert(type(op[1])==nlin.AnnotatedNote)
            annotations1.extend([{"id": id, "color": DEL_COLOR, "target":"beam"} for id in op[1].get_note_id()])
        #accident
        elif op[0] == "accidentins":
            assert(type(op[2])==nlin.AnnotatedNote)
            annotations2.extend([{"id": id, "color": INS_COLOR, "target":"accidental","head_id":op[4][1]} for id in op[2].get_note_id()])
        elif op[0] == "accidentdel":
            assert(type(op[1])==nlin.AnnotatedNote)
            annotations1.extend([{"id": id, "color": DEL_COLOR,"target":"accidental","head_id":op[4][0]} for id in op[1].get_note_id()])
        elif op[0] == "accidentedit":
            assert(type(op[1])==nlin.AnnotatedNote)
            assert(type(op[2])==nlin.AnnotatedNote)
            annotations1.extend([{"id": id, "color": SUB_COLOR, "target":"accidental","head_id":op[4][0]} for id in op[1].get_note_id()])
            annotations2.extend([{"id": id, "color": SUB_COLOR, "target":"accidental","head_id":op[4][1]} for id in op[2].get_note_id()])
        elif op[0] == "dotins":
            assert(type(op[2])==nlin.AnnotatedNote)
            annotations2.extend([{"id": id, "color": INS_COLOR, "target":"dot"} for id in op[2].get_note_id()])
        elif op[0] == "dotdel":
            assert(type(op[1])==nlin.AnnotatedNote)
            annotations1.extend([{"id": id, "color": DEL_COLOR, "target":"dot"} for id in op[1].get_note_id()])
        else:
            print("Annotation type {} not yet supported for visualization".format(op[0]))
    return annotations1, annotations2


def produce_annnot_svg(mei_file, annotations, out_path="annotated_score.svg"):
    #necessary for windows
    m21.environment.set('musescoreDirectPNGPath', 'C:\\Program Files\\MuseScore 3\\bin\\MuseScore3.exe')
    # produce the svg string with Verovio
    tk = verovio.toolkit()
#     tk.setOption("pageHeight", "500")
#     tk.setOption("scale", "90")
#     tk.setOption("ignoreLayout", "1")
    tk.setResourcePath(r"C:\Users\fosca\Desktop\verovio\data" ) #necessary in Windows
    tk.loadFile(mei_file._str)

    #TODO: display of multiple pages
    stringSVG = tk.renderToSVG() #this will produce just the first page. To update for longer scores
    svg_tree = ET.ElementTree(ET.fromstring(stringSVG))
    #build the parent map
    parent_map = {c:p for p in svg_tree.iter() for c in p}
    # display the annotations
    for ann in annotations:
        if ann["target"] == "bar":
            #find the lower common element
            lce= find_lce(ann["id"], svg_tree, parent_map)
            #color the common element
            lce.set("fill", ann["color"])  
        elif ann["target"] == "note":
            # print(ann)
            element = svg_tree.find(".//{}[@id='{}']".format(el_dict["g"],ann["id"]))
            element.set("fill", ann["color"])
        elif ann["target"] == "notehead":
            # try to extract the notehead
            notehead = find_notehead(ann["id"], svg_tree, ann["head_id"])
            #color the notehead
            notehead.set("fill", ann["color"])  
        elif ann["target"] == "beam":
            stem = find_stem(ann["id"], svg_tree)
            #color the stem
            stem.set("fill", ann["color"])  
        elif ann["target"] == "tuplet":
            #TODO: to implement
            print("tuplet not visualized")
        elif ann["target"] == "accidental":
            #find accident
            accident = find_accident(ann["id"],svg_tree,ann["head_id"])
            #color the corresponding accident
            accident.set("fill", ann["color"])
        elif ann["target"] == "dot":
            #find dots
            dots = find_dots(ann["id"],svg_tree)
            #color the corresponding beam
            dots.set("fill", ann["color"])
        else:
            raise TypeError("Unsupported annotation target: {}".format(ann["target"]))
    with open(out_path, 'wb') as svg_file:
        svg_tree.write(svg_file)
    return True


def find_accident(note_id, svg_tree,head_id):
    #take note element
    note = svg_tree.find(".//{}[@id='{}']".format(el_dict["g"],note_id))
    #find the accident
    accident = note.find("{}[@class='{}']".format(el_dict["g"],"accid"))
    if accident is None: #we are dealing with a chord
        n_list= note.findall("{}[@class='{}']".format(el_dict["g"],"note"))
        n = n_list[head_id]
        accident = n.find("{}[@class='{}']".format(el_dict["g"],"accid"))
    return accident

def find_dots(note_id, svg_tree):
    #take note element
    note = svg_tree.find(".//{}[@id='{}']".format(el_dict["g"],note_id))
    #find the accident
    dots = note.find("{}[@class='{}']".format(el_dict["g"],"dots"))
    return dots

def find_stem(note_id, svg_tree):
    #take note element
    note = svg_tree.find(".//{}[@id='{}']".format(el_dict["g"],note_id))
    #find the stem
    stem = note.find("{}[@class='{}']".format(el_dict["g"],"stem"))
    return stem

def find_notehead(note_id, svg_tree,head_id):
    #take note element
    note = svg_tree.find(".//{}[@id='{}']".format(el_dict["g"],note_id))
    #try find the notehead (not Null if we have a single note)
    notehead = note.find("{}".format(el_dict["use"]))

    if notehead is None: #we are dealing with a chord
        n_list= note.findall("{}[@class='{}']".format(el_dict["g"],"note"))
        n = n_list[head_id]
        notehead = n.find("{}".format(el_dict["use"]))
    return notehead

def find_lce(notes_id_list, svg_tree, parent_map):
    #build the ancestor list for each note
    ancestors= [] #a list of ancestors for each element
    for index, id in enumerate(notes_id_list):
        element = svg_tree.find(".//{}[@id='{}']".format(el_dict["g"],id))
        ancestors.append([])
        ancestors[index].append(element) #append the note element to have at least one differenct element
        while element in parent_map:   
            element = parent_map[element]
            ancestors[index].append(element)
    #now find the lowest common element
    found = False
    level = 0
    while not found:
        level +=1 #start from 1 because that is the first parent
        if all(el[level].attrib == ancestors[0][level].attrib for el in ancestors):
            found = True
    lce = ancestors[0][level]
    return lce