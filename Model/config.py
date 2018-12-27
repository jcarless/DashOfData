#!/usr/bin/python
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
    
import os

def config(filename='database.ini', section='postgresql'):
    if os.path.isfile(filename):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
        
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    else:
        raise Exception(f"Config file {filename} not found")
 
    return db