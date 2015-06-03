import pdb
import os
import ConfigParser
import json
from datetime import datetime,timedelta
from optparse import OptionParser
from oauth2client.client import SignedJwtAssertionCredentials


try:
    import gspread
except ImportError:
    print "gspread lib could not be found, writing to google docs disabled."    


"""
31/04/2013 Sjoerd

Write datetime + logmessage. To be used with launchy so I can write log messages
with one keystroke. Write to Google docs directly.

"""


def init_optparse():
    """ read options from commandline
    """
    
    parser = OptionParser("Usage: %prog [options] message (string)")            
    parser.add_option("-d", "--destination", type="choice",
                      choices = ["file","googledoc"],
                      dest="destination", default="file",
                      help='Write message to this destination, configured in "write_to_log.cfg" Choices: ["file","googledoc"]')
    parser.add_option("-t", "--time_shift", dest="time_shift",default=0,
                      help='Add this many minutes to the date written. Number can be negative')

    return parser


def create_log_item(msg,options):
    time_shift = options.time_shift
    if time_shift == "" or time_shift == None:
        time_shift = 0              
    log_item = LogItem(msg,int(time_shift))    
    return log_item



def mainloop(configfile):
    parser = init_optparse()
    (options, args) = parser.parse_args()
            
    if len(args) != 1:
        print ("Expected 1 argument: the message to write. instead found %d.\n" %len(args))
        parser.print_help()

    if options.destination == "file":
        filename = "timing_test.log"
        writer = FileLogWriter(filename)            

    elif options.destination == "googledoc":        
        writer = GoogleDocLogWriter(configfile)
    
    msg = args[0]
    writer.write(create_log_item(msg,options))



class LogWriter:
    """ Writes date and message to a log just for inheritance.
    """

    def write(self,log_item):
        raise NotImplemented("This method should be implemented in inheriting classes")
        

class FileLogWriter(LogWriter):
    
    def __init__(self,filename):
        self.filename = filename
    
    def write(self,log_item):
        """ Write "datetime - message" to new line of file            
        """    
        f = open(self.filename,"a+")    
        try:            
            f.write(str(log_item)) 
        finally:
            f.close()

class GoogleDocLogWriter(LogWriter):

    def __init__(self,configfile):
        self.parse(configfile)        


    def parse(self,configfile):
        try:
            gspread
        except NameError:
            raise Exception("gspread lib could not be imported. Writing to google doc has"
                            "been disabled")

        config = ConfigParser.RawConfigParser()
        config.read(configfile)
        
        self.google_spreadsheet_name = config.get('google_spreadsheet','google_spreadsheet_name')        
        self.google_credential_file = config.get('google_spreadsheet','google_credential_file')

        self.google_timestring_column = self.get_config_or_default(config,'google_timestring_column',"A")
        self.google_message_column = self.get_config_or_default(config,'google_message_column',"B")
                

    def get_config_or_default(self,config,optionname,default):
        """ To allow setting of defaults if an optionname is not found in the config file

        """        
        try:
            return config.get('google_spreadsheet',optionname)
        except ConfigParser.NoOptionError:
            return default
        
    def write(self,log_item):
        worksheet = self.open_google_doc()
        self.write_to_worksheet(log_item,worksheet)


    def open_google_doc(self):                
        # Login with your Google account
        json_key = json.load(open(self.google_credential_file))
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
        gc = gspread.authorize(credentials)

        # get worksheet
        worksheet = gc.open(self.google_spreadsheet_name).sheet1
        return worksheet

    

    def get_next_empty_row(self,worksheet):
        """Find the highest empty row to know where you can write a new entry
        Only checks for first empty cell in column where timestring is written
        
        """        
        idx = worksheet.get_int_addr(self.google_timestring_column+"1")[1]
        return len(worksheet.col_values(idx))+1
        

    def write_to_worksheet(self,log_item,worksheet):
        row = self.get_next_empty_row(worksheet)
        
        timestring_cell = '{0}{1}'.format(self.google_timestring_column,row)
        message_cell = '{0}{1}'.format(self.google_message_column,row)        
        worksheet.update_acell(timestring_cell,log_item.get_time_string())
        worksheet.update_acell(message_cell,log_item.msg)
        

class LogItem:
    def __init__(self,msg,add_minutes=0):
        
        self.msg = msg        
        self.time = self.get_time(add_minutes)

    def __str__(self):
        datestring = self.time.strftime("%Y%m%d %H:%M:%S")        
        return '%s - "%s"\n'%(datestring, self.msg) 

    def get_time_string(self):
        return self.time.strftime("%Y%m%d %H:%M:%S")
    
    
    def get_time(self,add_minutes):
        time = datetime.now()
        if add_minutes != 0:
            delta = timedelta(minutes=add_minutes)
            time = time + delta        
        return time

    

configfile = "D:/code/scripts/timekeeping/write_to_log.cfg"
mainloop(configfile)
    
    


