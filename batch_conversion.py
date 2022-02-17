import tkinter
import os
from os.path import isfile,join
from os import listdir

import tkinter.filedialog

def main():
    
    
    origdir=tkinter.filedialog.askdirectory()
    destdir=tkinter.filedialog.askdirectory()
    
    for f in listdir(origdir):
        absfilepath=join(origdir,f)
        if isfile(absfilepath):
            print(absfilepath)
            print("translator.py " + "'" + absfilepath + "'")
            os.system("python translator.py " + '"' + absfilepath + '"' + " " + '"' + f + '"' + " " + destdir)

main()
