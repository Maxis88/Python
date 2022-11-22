from customtkinter import *

root = CTk()
frame = CTkFrame(root, )
frame.pack(fill='both', expand=1)

label = CTkLabel(frame, text='Zawartosc ramki')
label.pack()
root.mainloop()