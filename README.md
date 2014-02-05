timekeeping
===========
Write messages to a log with one keystroke.

# Requirements
## python packages 
* gspread 0.1.0 for writing to google docs

## programs
* launchy (http://www.launchy.net/) launch manager, to run the python script which does the actual logging in a single keystroke. You can use any launch manager of method you want of course. Launchy works for me.

# setup 
## for writing to local file
Writing to log file works out of the box:
> python write_to_log.py "a message"
Or to write a message and set the time to 30 minutes ago
> python write_to_log.py "a message" -t -30

# for writing to google docs
* install gspread using 'pip install gspread'
* edit write_to_log.cfg to contain your google credentials and spreadsheet
* then call it like this:
> python write_to_log.py "a message" -d googledoc

# setup in launchy
* download and install launchy (http://www.launchy.net/download.php)
* in launchy settings go to 'plugins' tab and select "Runner" on the right
* In runner click '+' on the bottom and add (omit parenthesis): 
** Name : 'log'
** Program: 'C:/path/to/write_to_log_folder/write_tot_google_doc.bat' (put correct path here, .bat is needed because I could net get launchy te launch python directly)
** Arguments: '"$$" $$'  (this means 'first argument'. In launchy you can enter the first argument after pressing tab.
* To log something, open up launchy (alt-space by default) and type "log",<tab>,"some message"
* To log something to a time 10 minutes ago, open launchy and type "log",<tab>,"some message"<tab>-10

