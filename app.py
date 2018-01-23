import tkinter
import api
import base64
import os


class App:
    def __init__(self):
        self.app = tkinter.Tk()
        self.frame = tkinter.Frame(self.app)
        self.frame.grid()

    def pick(self, key):
        print(key)
        self.frame.destroy()

    def run(self):
        champions = api.get_champions()
        x = 0
        y = 0
        for key, value in champions.items():
            file = 'data/' + key + '.png'
            if not os.path.isfile(file):
                continue
            image_byt = open(file, 'rb').read()
            image_b64 = base64.encodebytes(image_byt)
            photo = tkinter.PhotoImage(data=image_b64)
            B = tkinter.Button(self.frame, width=100, height=100, command=lambda k=key: self.pick(k))
            B.config(image=photo)
            B.image = photo
            B.grid(row=x, column=y)
            y += 1
            if y % 7 == 0:
                x += 1
                y = 0
        self.app.mainloop()
