from tkinter import *
import customtkinter 
from PIL import Image

customtkinter.set_appearance_mode("system")  # default
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()

app.title('Login')
app.geometry('600x400')

image1 = customtkinter.CTkImage(Image.open('/home/alberto/Downloads/pattern.png'), size=(30, 30))
I1 = customtkinter.CTkLabel(master=app, image=image1)
I1.pack()



app.mainloop()