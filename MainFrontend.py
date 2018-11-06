import tkinter
import tkinter.messagebox
from tkinter.ttk import *
import tkinter.commondialog
from tkinter import *
import Python_data
from tkinter.filedialog import askopenfilenames
from tkinter import filedialog
from pathlib import Path
import threading
import _thread
import subprocess

class Window(object):

    i = 1

    def __init__(self,window):
        self.window = window

        self.window.wm_title("RS Charts ver3")


        b1 = tkinter.Button(window, text="Choose data location", width=40, command=self.data_folder)
        b1.grid(row=0, column=0)

        self.status1 = Label(window, width=5, bd=1, relief=SUNKEN, anchor=W)
        self.status1.grid(row = 0, column =1)

        b2 = tkinter.Button(window, text="Choose additional images for the slideshow", width=40, command=self.image_folder)
        b2.grid(row=1, column=0)

        self.status2 = Label(window, bd=1, width=5, relief=SUNKEN, anchor=W)
        self.status2.grid(row = 1, column =1)

        l1 = tkinter.Label(window, text="Slideshow interval(seconds)")
        l1.grid(row=2, column=0)

        self.slideshow = tkinter.StringVar()
        self.e2 = tkinter.Entry(window, textvariable=self.slideshow)
        self.e2.grid(row=3, column=0)

        l2 = tkinter.Label(window, text="Chart refresh interval(minutes)")
        l2.grid(row=2, column=1)

        self.dataRefresh = tkinter.StringVar()
        self.e2 = tkinter.Entry(window, textvariable=self.dataRefresh)
        self.e2.grid(row=3, column=1)


        b2 = tkinter.Button(window, text="Display it!", width=40,height=3, background = 'green', command=self.display_it)
        b2.grid(row=5, column=0, columnspan = 2)

        b2 = tkinter.Button(window, text="New images", width=40, background = "#85e0e0", command=self.new_images)
        b2.grid(row=7, column=0, columnspan = 2)

        b2 = tkinter.Button(window, text="Stop", width=40, background = 'red', command=self.stop_it)
        b2.grid(row=8, column=0, columnspan = 2)




    def data_folder(self):
        foldername = filedialog.askdirectory()
        Python_data.directory = Path(foldername)

        try:
            Python_data.update_target_rate()
            Python_data.makeQuoteTable()
            Python_data.runScript()
            Python_data.makeachart()
            self.status1.configure(background='green', text='OK')

        except Exception as e:
            self.status1.configure(background = 'red', text='Error')
            tkinter.messagebox.showinfo('Error', e)


    def image_folder(self):
        filenames = askopenfilenames()  # show an "Open" dialog box and return the path to the selected file
        filenameslist = list(filenames)

        try:
            Python_data.imgMaker(filenameslist)
            self.status2.configure(background='green', text='OK')
        except Exception as e:
            self.status2.configure(background='red', text='Error')
            tkinter.messagebox.showinfo('Error', e)

    def display_it(self):
        Python_data.interval = (int(self.slideshow.get()))
        Python_data.chartRefresh = (int(self.dataRefresh.get()))
        Python_data.make_index()
        #subprocess.call([])
        t = threading.Thread(name ='non-daemon', target = Python_data.ThreadExample)
        t.setDaemon(True)
        t.start()

    def new_images(self):
        Python_data.make_index()


    def stop_it(self):
        Python_data.schedule.clear('job')




window=tkinter.Tk()
Window(window)
window.mainloop()