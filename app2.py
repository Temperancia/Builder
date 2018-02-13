import wx
import build
import os

builder = build.Build()


class ChampionList(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id,
                             style=wx.LC_ICON | wx.BORDER_NONE | wx.LC_NO_HEADER,
                             pos=(0, 100),
                             size=(800, 400)
                             )
        BMP_SIZE = 120
        self.il = wx.ImageList(BMP_SIZE, BMP_SIZE)

        self.imglistdict = {}
        for key, value in builder.champions.items():
            file = 'data/champion_squares/' + key + '.png'
            if not os.path.isfile(file):
                continue
            image = wx.Image(file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.imglistdict[value['name'].lower()] = self.il.Add(image)
        self.SetImageList(self.il, wx.IMAGE_LIST_NORMAL)

        self.populate_list(all=True)

    def populate_list(self, name=None, all=False):  # awkward ambivalent function called to populate the list
        if name:
            name = name.lower()
        self.ClearAll()
        for index, (key, value) in enumerate(self.imglistdict.items()):  # key is the name of champ , value its graphical representation and index just the place it will get
            if all or key.startswith(name):  # if ahri starts with 'a'
                self.InsertItem(index, value)


class ChampionFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(800, 600))

        self.__init_ui()
        self.Centre()
        self.Show()

    def change_list(self, event):
        self.list.populate_list(self.text.GetLineText(0))  # call list function and sending it string input of the widget

    def __init_ui(self):
        self.text = wx.TextCtrl(self)  # makes input line for selection
        self.Bind(wx.EVT_TEXT, self.change_list)  # binds any text input to change list func
        self.list = ChampionList(self, -1)  # creates the actual list


class MDIFrame(wx.MDIParentFrame):
    def __init__(self):
        wx.MDIParentFrame.__init__(self, None, -1, "LOL Builder", size=(1200, 800))
        menu = wx.Menu()
        menu.Append(0, "&New Window")
        menu.Append(1, "&Exit")
        menubar = wx.MenuBar()
        menubar.Append(menu, "&File")

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnNewWindow, id=0)
        self.Bind(wx.EVT_MENU, self.OnExit, id=1)

    def OnExit(self, evt):
        self.Close(True)

    def OnNewWindow(self, evt):
        ChampionFrame(self, 'Champion')


class App:
    def __init__(self):
        app = wx.App()
        frame = MDIFrame()
        frame.Show()
        app.MainLoop()