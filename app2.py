from frames import *


class App:
    def __init__(self):
        app = wx.App()
        frame = MDIFrame()
        frame.Show()
        app.MainLoop()
