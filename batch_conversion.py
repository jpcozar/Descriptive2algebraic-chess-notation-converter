import tkinter
import os
from os.path import isfile,join
from os import listdir

import tkinter.filedialog

def main():
    
    
    origdir=tkinter.filedialog.askdirectory()
    destdir=tkinter.filedialog.askdirectory()
    number=0

    for f in listdir(origdir):
        absfilepath=join(origdir,f)
        if isfile(absfilepath):
            os.system("python translator.py " + '"' + absfilepath + \
                '"' + " " + '"' + f + '"' + " " + '"' + destdir + '"')
            number=number+1

    print (str(number) + " file(s) converted to SAN notation in " + '"' + destdir + '"')
main()
