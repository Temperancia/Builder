import tkinter  # standard UI library for python
import api
import os


class App:
    def __init__(self):
        self.app = tkinter.Tk()  # creation of a new tkinter application
        self.frame = tkinter.Frame(self.app)  # creation of a new frame FROM the application
        self.frame.grid()  # displays the empty for now frame using grid geometry , my favourite display tool
        # you 'place' items using columns and rows and it scales

    def pick(self, key):
        print(key)
        self.frame.destroy()

    def run(self):
        champions = api.get_champions()  # our great api module gives us usual dict of champs
        # api.get_champion_squares(champions) # cost a lot to refresh
        x = 0
        y = 0
        for key, value in champions.items():
            file = 'data/' + key + '.png'  # here is a thing i have decided , i have stored already all squares
            # from urls within api module
            if not os.path.isfile(file):  # standard way to check if a file exists
                continue
            image_byt = open(file, 'rb').read()  # simply storing the content of file 'r' for read 'b' for bytes
            # image_b64 = base64.encodebytes(image_byt)  # i dont rly know myself why i used b64 , example imo
            photo = tkinter.PhotoImage(data=image_byt)
            b = tkinter.Button(self.frame, width=100, height=100, command=lambda k=key: self.pick(k))
            #  creation of a button FROM the main frame with w = 100px and h = 100px with onclick the function pick
            # called with k parameter , had a weird issue when i'm not doing k=key because key gets replaced on
            # each iteration of the loop , so k=key creates specific to lambda value , dont ask me
            b.config(image=photo)  # here i dont rly know either why you require both config and image to be set
            b.image = photo
            b.grid(row=x, column=y)  # displaying finally the image button on increasing y for column
            y += 1
            if y % 14 == 0:  # if 14th column reached go back to 1st column on 2nd row , roughly making 14 x 100px
                x += 1
                y = 0
        self.app.mainloop()  # displaying the app ! # good bye python :(
