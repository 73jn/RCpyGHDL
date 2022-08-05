import glob
import sys
import os
import RCpyGHDL
import logging
import time
class LogFile(object):
    """File-like object to log text using the `logging` module."""

    def __init__(self, name=None):
        self.logger = logging.getLogger(name)

    def write(self, msg, level=logging.INFO):
        self.logger.log(level, msg)

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()


def AnalyzeFile(fichier):
   print('INFO:Analyze ',  fichier)
   time.sleep(1)
   Rule = RCpyGHDL.RCpyGHDL("--std=08",fichier)
   time.sleep(1)
   print("INFO: Rule CNE_02500 : list all entity ports")
   time.sleep(1)
   Rule.CNE_02500()
   time.sleep(1)
   print("INFO: Rule CNE_02600 : list all signals")
   time.sleep(1)
   Rule.CNE_02600()
   time.sleep(1)
   print("----------------") 
   time.sleep(1)
   os._exit(0)  



def AnalyzeAllFiles():
    #list all vhd file
    print(1)
    listfiles=glob.glob("*.vhd")
    time.sleep(1)
    print(2)
    print(listfiles)
    time.sleep(1)


    #apply rules on files
    for fichier in listfiles:
        print(fichier)
        try:
            newpid = os.fork()
            if newpid == 0:
                #fork to execute analysis (this is the only solution to avoid program crash due to libghdl scann error)
                AnalyzeFile(fichier)
            else:
                os.waitpid(newpid, 0)  # wait for fork to finish
        finally:
            pass


#initilize log file
#logging.basicConfig(level=logging.DEBUG, filename='analysis.log')
#logging.basicConfig(format='%(message)s', level=logging.DEBUG)


# Redirect stdout and stderr
#sys.stdout = LogFile('stdout')
#sys.stderr = LogFile('stderr')

#launch analysis
AnalyzeAllFiles()