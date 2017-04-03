import pdb
import os
from datetime import datetime

"""
04/04/2013 Sjoerd

Process time log, clean it up a bit and add tag suggestions so I dont have to
type so much

"""

#==== methods ==================================================================
    
def cleantimestring(timestring):
    """time is either of the form 11:38:10.07 or 1:38:10.07 (wihtout padding)
    make it nicer.
    """    
    #pad if needed
    if len(timestring) == 10:
        timestring = "0"+timestring
    #remove milliseconds. we're logging hours here.
    return timestring[0:8]

def parse_line(line):
    """Read in a line in the log and return the interesting things: start
       and description of the event 
    """
    assert line != ""

    line = line.replace("  "," ") #remove double spaces with non padded hours
    line = line.rstrip('\n ')
    parts = line.split(" ")        

    datetimestring = parts[0] +"-"+ cleantimestring(parts[1])
    start = datetime.strptime(datetimestring[0:17],"%Y%m%d-%H:%M:%S")
    comment = " ".join(parts[3:])
    comment = clean(comment)
    
    return {"start":start,"comment":comment}

def clean(comment):
    """Texts at each time can be messy because is is just a text file. Make sure
    the comment is at least surrounded by quotes.
    """
    if comment == "":
        comment = "\"\""
    elif not comment.endswith('"'):
        comment = comment + '"'
    elif not comment.startswith('"'):
        comment = '"' +comment
    return comment

def suggest_tags(comment):
    """Return list of tags that can be added given the comment text
    E.g. if the comment contains "rdwww" or "literature" add a "rdwww" tag
    
    """

    searchfor = [("rdwww,site,marijn,server,uci,literature,pipeline,\
                   special chars,diag lib,.bib,updatepubs","rdwww"),
                 ("lola11,cause07,anode09,vessel12,evaluation,screenshots,\
                   challenge,rina","challenges"),
                 ("mail,email","email"),
                 ("planning,plannen","planning"),
                 ("lunch,eten,walk,wandeling","lunch"),
                 ("meeting,overleg,disussion,pulmo,meet ","meetings"),
                 ("gone,home,genoeg,leaving,ill\",naar huis,dinner,pick up","home"),
                 ("sarah,jean,jaap,sjoerd,sygrid,eva,haixia","helping_collegues"),
                 ("pyhon,python,django,graphs,comic,bart,marcel","COMIC"),
                 ("administratie,administration,tickets","administration"),
                 ("mevis, module, workstation","MeVisLab"),
                 ("in\",binnen,at work,taart","other")
                ]
    tags = []
    for (searchstrings,tag) in searchfor:
        for searchstring in searchstrings.split(","):
            if searchstring.lower() in comment.lower():
                tags = tags+tag.split(",")
                exit
                
    return tags


def process(inputfile,outputfile):
    rawlines = inputfile.readlines()
    lines = [parse_line(line) for line in rawlines]
    outputfile.write("%s\t%s\t%s\n"%("startdate starttime","duration (min)","comment"))
    print "processing %d lines " % len(lines)
    for i in range(len(lines)-1): #skip last because duration cannot be determined        
        comment = lines[i]["comment"]
        tags = suggest_tags(comment)
        tags_str = ",".join(tags)
        if "home" in tags: 
			duration_str = "0"	# when going home, stop counting minutes			
        else:
			start = lines[i]["start"]
			end = lines[i+1]["start"]
			duration = end - start
			duration_str = str(duration.seconds / 60)
		

        outputfile.write("%s\t%s\t%s\t%s\n"%(str(start),
                                         duration_str,
                                         comment,tags_str))



#====== main automation ========================================================
f = open("timing.log")
fp = open("timing_processed.log","w")

try:
    process(f,fp)
finally:
    f.close()
    fp.close()
