import pyGHDL.libghdl     as libghdl
import glob
import os
import time
def AnalyzeFile(fichier):
    libghdl.initialize()
    libghdl.analyze_init()
    libghdl.analyze_file(fichier)



def AnalyzeAllFiles():
    #list all vhd file
    listfiles=glob.glob("*.vhd")
    print(listfiles)
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

AnalyzeAllFiles()