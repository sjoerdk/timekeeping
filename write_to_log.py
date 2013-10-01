import pdb
import os
from datetime import datetime
from optparse import OptionParser
import ConfigParser

try:
    import gspread
except ImportError:
    print "gspread lib could not be found, writing to google docs disabled."    


"""
31/04/2013 Sjoerd

Write datetime + logmessage. To be used with launchy so I can write log messages
with one keystroke. Write to Google docs directly.

"""


def get_now_string():
    return datetime.now().strftime("%Y%m%d %H:%M:%S")    
    

def write_msg_to_file(msg,filename):
    """ Write "datetime - message" to new line of file

    """    
    f = open(filename,"a+")    
    try:
        nowstr = get_now_string()        
        f.write('%s - "%s"\n'%(nowstr, msg)        ) 
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

    

def mainloop(configfile):
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


        config = ConfigParser.RawConfigParser()
        config.read(configfile)
        google_spreadsheet_name = config.get('google_spreadsheet','google_spreadsheet_name')
        google_id = config.get('google_spreadsheet','google_id')
        google_password = config.get('google_spreadsheet','google_password')
        
        
        # Login with your Google account
        gc = gspread.login(google_id,google_password)

        # Open a worksheet from spreadsheet with one shot
        wks = gc.open(google_spreadsheet_name).sheet1

        highest_row =  len(wks.col_values(1))

        nowstr = get_now_string()
        msg = args[0]
        cell_list = wks.range('A%s:B%s'%(highest_row+1,highest_row+1))
        cell_list[0].value = nowstr
        cell_list[1].value = msg
        
        wks.update_cells(cell_list)
        

configfile = "D:/code/scripts/timekeeping/timekeeping/write_to_log.cfg"
mainloop(configfile)
    
    


