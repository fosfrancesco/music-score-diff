# music-score-diff
A tool to compute and visualize the differences between two music scores.

<!-- The supported differences are:

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
- "subtuplet" : tuplet substitution (e.g. a "continue" tuplet with a "end" beam)  -->

## Setup

The dependencies are listed in the file [environment.yml](environment.yml).
If you use conda, you can install the dependencies with: `conda env create -f environment.yml` .

Moreover you need to setup music21 to display a musical score (e.g. with MuseScore).

## Usage
An example is available in [tutorial.ipynb](tutorial.ipynb).

## Citing
If you use this work in any research, please cite the relevant paper:

```
@inproceedings{foscarin2019diff,
  title={A diff procedure for music score files},
  author={Foscarin, Francesco and Jacquemard, Florent and Fournier-S’niehotta, Raphael},
  booktitle={6th International Conference on Digital Libraries for Musicology},
  pages={58--64},
  year={2019}
}
```

The paper is freely available [here](https://hal.inria.fr/hal-02267454v2/document)

## License
Licensed under the [MIT License](LICENSE).

## Acknowledgment
Thanks goes to [gregchapman-dev](https://github.com/gregchapman-dev) for helping with the diff visualization in music21.

