# music-score-diff
A tool to compute and visualize the differences between two music scores in MEI format.

The supported differences are:

1. Bar level:
- "insbar": bar insertion 
- "delbar": bar deletion
2. Voice level:
- "insvoice": voice insertion
- "delvoice": voice deletion
3. General-note level:
- "insnote" : general-note insertion
- "delnote" : general-note deletion
- "subhead" : head substitution (e.g. a white note becoming a black note)
4. Pitch level:
- "inspitch" : pitch insetion (e.g. a 2-note chord that become a 3-note chord)
- "delpitch" : pitch deletion
- "subpitchnam" : substitution of the pitch name (e.g. a G3 that become a F3)
- "insaccidental" : accidental insertion
- "delaccidental" : accidental deletion
- "subaccidental" : accidental substitution
- "insdot" : dot insertion
- "deldot" : dot deletion
- "instie" : tie insertion
- "deltie": tie deletion
5. Beam level:
- "insbeam" : beam insertion
- "delbeam" : beam deletion
- "subbeam" : beam substitution (e.g. a "continue" beam with a "end" beam) 
6. Tuplet level: 
- "instuplet" : tuplet insertion
- "deltuplet" : tuplet deletion
- "subtuplet" : tuplet substitution (e.g. a "continue" tuplet with a "end" beam) 


