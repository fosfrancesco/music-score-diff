import subprocess
import re
from pathlib import Path


#convert from music xml to mei
def musicxml2mei(musicxml_path, out_path):
    with open(musicxml_path) as musicxml_file:
        musicxml = musicxml_file.read()

    # Remove the DTD: avoids Web accesses, timeouts, etc.
    pattern = re.compile("<!DOCTYPE(.*?)>", re.DOTALL)
    mxml_without_type = re.sub(pattern, "", musicxml)
    # Write the MusicXML without DTD in the tmp area
    with open("temp_files/score.xml","w") as mxml_file: 
        mxml_file.write(mxml_without_type)
    
    try:
        # transform from partwise to timewise
        subprocess.call(['java', '-jar', 'saxon/saxon9.jar', '-versionmsg:off', '-s:temp_files/score.xml', '-xsl:saxon/partime.xsl', '-o:temp_files/timexml.xml'])
        # trasform from musicxml to MEI
        subprocess.call(['java', '-jar', 'saxon/saxon9.jar', '-versionmsg:off', '-s:temp_files/timexml.xml', '-xsl:saxon/musicxml2mei-3.0.xsl', '-o:{}'.format(out_path)])
        print("MEI file written in {}".format(out_path))
        return True
    except Exception as e:
        print("Something went wrong with the conversion. Error: {}".format(str(e)))
        return False


xml_path = Path("test_scores/musicxml/tie_score_1b.xml")
mei_path = Path("test_scores/tie_score_1b.mei")
musicxml2mei(xml_path, mei_path)


