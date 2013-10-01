import pdb
import os
from datetime import datetime
from optparse import OptionParser

try:
    import gspread
except ImportError:
    print "gspread lib could not be found, writing to google docs disabled."    

"""
31/04/2013 Sjoerd

Write datetime + logmessage. To be used with launchy so I can write log messages
with one keystroke. Write to Google docs directly.

"""


#====== main automation ========================================================


def write_msg_to_file(msg,filename):
    """ Write "datetime - message" to new line of file

    """    
    f = open(filename,"a+")    
    try:
        now = datetime.now().strftime("%Y%m%d %H:%M:%S")    
        f.write('%s - "%s"\n'%(now, msg))        
    finally:
        f.close()
        
    
    
def init_optparse():
    """ read options from commandline
    """
    
    parser = OptionParser("Usage: %prog [options] message (string)")            
    parser.add_option("-d", "--destination", type="choice",
                      choices = ["file","googledoc"],
                      dest="destination", default="file",
                      help='Write message to this destination. Choices: ["file","googledoc"]')

    return parser
    

def mainloop():
    parser = init_optparse()
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        print ("Expected 1 argument: the message to write. instead found %d.\n" %len(args))
        parser.print_help()

    if options.destination == "file":
        write_msg_to_file(args[0],"timing_test.log")

    elif options.destination == "googledoc":
        try:
            gspread
        except NameError:
            raise Exception("gspread lib could not be imported. Writing to google doc has"
                            "been disabled")

        
        raise NotImplementedError ("make this!")


    
mainloop()
    
    


