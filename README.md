# Underwatch
Underwatch is a utility for tracking changes to the ini and save files for Undertale.
Underwatch uses Python 3.4 and the Clint module for coloured output.

By default, Underwatch prints out any changes to the terminal in the following format:

    file9 changed
    (54) 4  >> 5  (Spared count)
    (56) 81  >> 83  (Skipped count)
    (549) 23374  >> 24727  (Play time)
    
    undertale.ini changed
    [General]
    Room: 312.000000 >> 12.000000
    Time: 23374.000000 >> 24727.000000

Changes to the save file include the line number and a description if one is known.
I've taken my descriptions from the Traveler's Guide to the Underland:
https://docs.google.com/document/d/1h_vdEFZMtefD-nkCZ7ODzArp7BRbGgN0_7HQ1XjTT8Y/edit#heading=h.a5d6q4uvp7b8
and from some experimentation.
The descriptions for save file lines are stored in _saveFile and can be modified and added to, the -u switch allows the descriptions to be updated while Underwatch is running.

Timestamps can be added to the output with the -t switch, the format for the timestamp can optionally be supplied as an argument, or will default to [%H:%M:%S]
All python time format codes can be used, a full list is included at the end of this readme

On first run, Underwatch will confirm the directory for Undertale data (usually C:\\Users\\<username>\\AppData\\Local\\UNDERTALE), once set the _path file is created and used in future.
The -p option allows a custom path to be supplied, overriding the _path file or skipping its creation

The -f or -s switch can be used to output changes to files. -f stores all changes in a single log file, while -s stores each set of changes in a new timestamped file.
By default the timestamp format is %Y-%m-%d %H.%M.%S, this can be overridden by supplying a format with -t

By default, Underwatch closes when Undertale closes, this behaviour can be overridden with -x

    usage: underwatch [-h] [-p PATH] [-f | -s] [-m] [-o PATH] [-t [FORMAT]] [-u] [-q]
                   [-x]
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PATH, --path PATH  explicitly set the Undertale save folder, overrides
                            _path file
      -f, --file            output all changes to Underwatch.log.
      -s, --sequence        output each change to a timestamped file. The format
                            is %Y-%m-%d %H.%M.%S by default, and can be changed
                            with -t
      -m, --multiple        output changes to multiple files (save0.log,
                            undertale.ini.log, etc.)
      -o PATH, --out PATH   explicitly set the output directory, default is the
                            working directory
      -t [FORMAT], --time [FORMAT]
                            output a timestamp with each change. The default
                            format is [%H:%M:%S], see readme.txt for format
                            options
      -u, --update          monitor _saveFile, allows updating of descriptions
                            without restarting
      -q, --quiet           don't ouput to the screen.
      -x, --no-exit         prevent Underwatch from closing when Undertale closes
                            (CRTL+C to kill Underwatch)
						
						
Python datetime format codes

    %a  Locale’s abbreviated weekday name.
    %A  Locale’s full weekday name.      
    %b  Locale’s abbreviated month name.     
    %B  Locale’s full month name.
    %c  Locale’s appropriate date and time representation.   
    %d  Day of the month as a decimal number [01,31].    
    %f  Microsecond as a decimal number [0,999999], zero-padded on the left
    %H  Hour (24-hour clock) as a decimal number [00,23].    
    %I  Hour (12-hour clock) as a decimal number [01,12].    
    %j  Day of the year as a decimal number [001,366].   
    %m  Month as a decimal number [01,12].   
    %M  Minute as a decimal number [00,59].      
    %p  Locale’s equivalent of either AM or PM.
    %S  Second as a decimal number [00,61].
    %U  Week number of the year (Sunday as the first day of the week)
    %w  Weekday as a decimal number [0(Sunday),6].   
    %W  Week number of the year (Monday as the first day of the week)
    %x  Locale’s appropriate date representation.    
    %X  Locale’s appropriate time representation.    
    %y  Year without century as a decimal number [00,99].    
    %Y  Year with century as a decimal number.   
    %z  UTC offset in the form +HHMM or -HHMM.
    %Z  Time zone name (empty string if the object is naive).    
    %%  A literal '%' character.
