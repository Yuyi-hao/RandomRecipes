from tkinter import * 
from PIL import ImageTk
import sqlite3
import numpy as np


# To make font prettier based on operating system 
# import pyglet

# pyglet.font.add_file("fonts\Shanti-Regular.ttf")
# pyglet.font.add_file("fonts\Ubuntu-Bold.ttf")

BGCOLOR = "#3d6466"

def pre_process(table_name, table_records):
    title = table_name[:-6]
    title = "".join([char if char.islower() else " "+char for char in title])
    ingredients = []
    # ingredients 
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(f"{qty} {unit} of {name}")

    return title,ingredients

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

class App():
    def __init__(self):
        window = Tk()
        window.title("Recipe Picker")
        photo = PhotoImage(file = "assets\RRecipe_logo.png")
        window.iconphoto(False, photo)
        window.eval("tk::PlaceWindow . center") # eval method execute command in tcl language
        # place window at centre 
        # midw_of_screen = int(window.winfo_screenwidth()*0.35)
        # midh_of_screen = int(window.winfo_screenheight()*0.1)
        # window.geometry("500x600+" + str(midw_of_screen) + '+' + str(midh_of_screen))

        # create a frame
        self.frame1 = Frame(window, width = 500, height = 600, bg = BGCOLOR)
        self.frame2 = Frame(window, bg = BGCOLOR)
        for frame in (self.frame1, self.frame2):
            frame.grid(row = 0, column = 0, sticky="nesw")
        self.load_frame1()

        window.mainloop()
    
    def load_frame1(self):
        clear_widgets(self.frame2)
        self.frame1.tkraise()
        self.frame1.pack_propagate(False) # will prevent child(e.g. logo_image_wid) to change its property 

        # setting logo in frame1 using pillow library 
        logoImage = ImageTk.PhotoImage(file = "assets\RRecipe_logo.png")
        logo_image_wid = Label(self.frame1, image= logoImage, bg = BGCOLOR)
        logo_image_wid.image = logoImage
        logo_image_wid.pack()

        # displaying text 
        Label(self.frame1, text = "Ready for a random recipe?", bg = BGCOLOR, fg= "white", font= ("TkMenuFont", 14)).pack()

        # Button
        Button(self.frame1 , text = "SHUFFLE", font = ("TkHeadingFont", 20), bg= "#28393a", fg= "white", cursor="hand2", activebackground="#badee2", activeforeground="black", command = self.load_frame2).pack(pady=25)

    def load_frame2(self):
        clear_widgets(self.frame1)
        self.frame2.tkraise()
        # self.frame2.pack_propagate(False)
        table_name, table_records = self.fetch_data()
        title, ingredients = pre_process(table_name, table_records)

        # setting logo in frame2 using pillow library 
        logoImage = ImageTk.PhotoImage(file = "assets\RRecipe_logo_bottom.png")
        logo_image_wid = Label(self.frame2, image= logoImage, bg = BGCOLOR)
        logo_image_wid.image = logoImage
        logo_image_wid.pack(pady=20)
        
        # displaying title 
        Label(self.frame2, text = title, bg = BGCOLOR, fg= "white", font= ("TkHeadingFont", 20)).pack(pady = 10)

        # displaying recipes 
        for i in ingredients:
            Label(self.frame2, text = i, bg = "#28393a", fg= "white", font= ("TkMenuFont", 14)).pack(fill="both")
        
        # Button
        Button(self.frame2 , text = "BACK", font = ("TkHeadingFont", 18), bg= "#28393a", fg= "white", cursor="hand2", activebackground="#badee2", activeforeground="black", command = self.load_frame1).pack(pady=10)



    def fetch_data(self):
        # create connection 
        connection = sqlite3.connect(r"data\recipes.db")
        cursor = connection.cursor()
        # getting name of all table present in database 
        cursor.execute("SELECT * FROM sqlite_schema WHERE type = 'table';")
        all_tables = cursor.fetchall()
        random_idx = np.random.randint(0,len(all_tables)-1) # np.random.randint(a,b) both a and b included 
        table_name = all_tables[random_idx][1]
        cursor.execute(f"SELECT * FROM {table_name};")
        table_records  = cursor.fetchall()

        # terminate the connection 
        connection.close()

        return table_name, table_records
    
    

App()


