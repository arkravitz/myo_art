import Tkinter
import tkMessageBox

top = Tkinter.Tk()

C = Tkinter.Canvas(top, bg="blue", height=250, width=300)

coord = 10, 50, 240, 210
arc = C.create_oval(10, 10, 240, 240, fill="red")

C.pack()
top.mainloop()

