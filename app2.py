import wx
import build
import os

builder = build.Build()


class List(wx.ListCtrl):
    def __init__(self, parent, pos, size, item_size, path):
        wx.ListCtrl.__init__(self, parent,
                             style=wx.LC_ICON | wx.BORDER_NONE | wx.LC_NO_HEADER,
                             pos=pos,
                             size=size
                             )
        self.il = wx.ImageList(item_size, item_size)

        self.imglistdict = {}
        for key, value in builder.champions.items():
            file = path + key + '.png'
            if not os.path.isfile(file):
                continue
            image = wx.Image(file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            name = value['name'].lower()
            self.imglistdict[name] = {'image': self.il.Add(image), 'keywords': name.split(' ')}
        self.SetImageList(self.il, wx.IMAGE_LIST_NORMAL)

        self.populate_list()

    def populate_list(self, selection=None):
        if selection:
            selection = selection.lower()
        self.ClearAll()
        for index, (key, value) in enumerate(self.imglistdict.items()):
            if not selection or key.startswith(selection) \
                    or True in map(lambda word: word.startswith(selection), value['keywords']):
                self.InsertItem(index, value['image'])


class ChampionList(List):
    def __init__(self, parent, pos, size):
        super().__init__(parent, pos, size, 120, 'data/champion_squares/')


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
        self.list = ChampionList(self, (0, 0), (400, 400))  # creates the actual list


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