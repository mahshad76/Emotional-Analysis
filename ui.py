import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from classrbf_new import RBF
from naive_class import Naive
from knn_class import KNN

def open_file():
    file = askopenfile(mode ='r', filetypes =[('Python Files', '*.py')])
    if file is not None:
        content = file.read()
        print(content)

master=tkinter.Tk()
master.title("place() method")
master.geometry("450x350")


button1=tkinter.Button(master, text="sample_tweets",command = lambda:open_file())
button1.place(x=0, y=200)



def setTextInput(text):
    textExample.delete(1.0,"end")
    textExample.insert(1.0, text)

textExample = tkinter.Text(master, height=10)
textExample.pack()

txtfld1 = Entry(master, width=20)
def knn1():
    txtfld1.place(x=200, y=230)
    p1 = KNN(textExample.get("1.0","end-1c"))
    c = p1.knn()
    #txtfld1.insert(INSERT, "RBF outcome : ")
    txtfld1.insert(INSERT, c)
    #txtfld1.pack()

txtfld2 = Entry(master, width=20)
def naive1():
    txtfld2.place(x=200, y=260)
    p1 = Naive(textExample.get("1.0","end-1c"))
    c = p1.naive()
    #txtfld1.insert(INSERT, "RBF outcome : ")
    txtfld2.insert(INSERT, c)

txtfld3 = Entry(master, width=20)
def rbf1():
    txtfld3.place(x=200, y=290)
    p1 = RBF(textExample.get("1.0","end-1c"))
    c = p1.rbf()
    #txtfld1.insert(INSERT, "RBF outcome : ")
    txtfld3.insert(INSERT, c)

def delete():
    txtfld1.delete(0, "end")
    txtfld2.delete(0, "end")
    txtfld3.delete(0, "end")
    textExample.delete("1.0", "end")

button2=tkinter.Button(master, text="KNN",command = knn1)
button2.place(x=0, y=230)

button3=tkinter.Button(master, text="NAIVE BAYES",command = naive1)
button3.place(x=0, y=260)

button4=tkinter.Button(master, text="RBF",command = rbf1)
button4.place(x=0, y=290)

button5=tkinter.Button(master, text="clear",command = delete)
button5.place(x=0, y=320)

master.resizable(0,0)
master.mainloop()