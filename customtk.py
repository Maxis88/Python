from customtkinter import *

root = CTk()
root.geometry("800x600")
print()
frame = CTkFrame(root, width=200, height=590,)
frame.grid(column=0, row=0, padx=10)

frame_tresc = CTkFrame(root, width=600, height=590)
frame_tresc.grid(column=1, row=0)

label = CTkLabel(frame, text='Menu')
label.pack(anchor='n', fill='x', expand=1)
root.mainloop()