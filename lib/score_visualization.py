import re
import subprocess
from music21 import mei
import verovio
from xml.etree import ElementTree as ET
import lib.NotationLinear as nlin

INS_COLOR = "green"
DEL_COLOR = "red"
SUB_COLOR = "yellow"

def oplist2annotations(operations):
    annotations1 = [] #for the score1
    annotations2 = [] #for the score2
    for op in operations:
        #bar
        if op[0] == "insbar":
            assert(type(op[2]) == nlin.VoiceLinear)
            annotations2.extend([{"id": id, "color": INS_COLOR} for voice in op[2] for id in voice.get_note_id()])
        elif op[0] == "delbar":
            assert(type(op[1]) == nlin.VoiceLinear)
            annotations1.extend([{"id": id, "color": DEL_COLOR} for voice in op[1] for id in voice.get_note_id()])
        #voices
        if op[0] == "voiceins":
            assert(type(op[2]) == nlin.VoiceLinear)
            annotations2.extend([{"id": id, "color": INS_COLOR} for id in op[2].get_note_id()])
        elif op[0] == "voicedel":
            assert(type(op[1]) == nlin.VoiceLinear)
            annotations1.extend([{"id": id, "color": DEL_COLOR} for id in op[1].get_note_id()])
        #note
        elif op[0] == "noteins":
            assert(type(op[2])==nlin.AnnotatedNote)
            annotations2.extend([{"id": id, "color": INS_COLOR} for id in op[2].get_note_id()])
        elif op[0] == "notedel":
            assert(type(op[1])==nlin.AnnotatedNote)
            annotations1.extend([{"id": id, "color": DEL_COLOR} for id in op[1].get_note_id()])
        #pitch
        elif op[0] == "pitchnameedit":
            assert(type(op[1])==nlin.AnnotatedNote)
            assert(type(op[2])==nlin.AnnotatedNote)
            annotations1.extend([{"id": id, "color": SUB_COLOR} for id in op[1].get_note_id()])
            annotations2.extend([{"id": id, "color": SUB_COLOR} for id in op[2].get_note_id()])
        #beam
        elif op[0] == "insbeam":
            assert(type(op[2])==nlin.AnnotatedNote)
            annotations2.extend([{"id": id, "color": INS_COLOR} for id in op[2].get_note_id()])
        elif op[0] == "delbeam":
            assert(type(op[1])==nlin.AnnotatedNote)
            annotations1.extend([{"id": id, "color": DEL_COLOR} for id in op[1].get_note_id()])
        #accident
        elif op[0] == "accidentins":
            assert(type(op[2])==nlin.AnnotatedNote)
            annotations2.extend([{"id": id, "color": INS_COLOR} for id in op[2].get_note_id()])
        elif op[0] == "accidentdel":
            assert(type(op[1])==nlin.AnnotatedNote)
            annotations1.extend([{"id": id, "color": DEL_COLOR} for id in op[1].get_note_id()])
        elif op[0] == "accidentedit":
            assert(type(op[1])==nlin.AnnotatedNote)
            assert(type(op[2])==nlin.AnnotatedNote)
            annotations1.extend([{"id": id, "color": SUB_COLOR} for id in op[1].get_note_id()])
            annotations2.extend([{"id": id, "color": SUB_COLOR} for id in op[2].get_note_id()])
        else:
            print("Annotation type {} not yet supported for visualization".format(op[0]))
    return annotations1, annotations2




def produce_annnot_svg(mei_file, annotations, out_path="annotated_score.svg"):
    # produce the svg string with Verovio
    tk = verovio.toolkit()
#     tk.setOption("pageHeight", "500")
#     tk.setOption("scale", "90")
#     tk.setOption("ignoreLayout", "1")
    tk.setResourcePath(r"C:\Users\fosca\Desktop\verovio\data" ) #necessary in Windows
    tk.loadFile(mei_file)
    stringSVG = tk.renderToSVG() #this will produce just the first page. To update for longer scores

    # display the annotations
    svg_tree = ET.ElementTree(ET.fromstring(stringSVG))
    
    el_dict={
        "g": "{http://www.w3.org/2000/svg}g"
    }
    for ann in annotations:
        try:
            print(ann)
            element = svg_tree.find(".//{}[@id='{}']".format(el_dict["g"],ann["id"]))
            element.set("fill", ann["color"])
        except:
            print("Could not find the id {} ".format(ann["id"]))
    with open(out_path, 'wb') as svg_file:
        svg_tree.write(svg_file)
    return True