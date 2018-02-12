import wx
import build
import os

builder = build.Build()


class ChampionList(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id,
                             style=wx.LC_ICON
                                   | wx.BORDER_NONE
                                   | wx.LC_NO_HEADER
                             )
        BMP_SIZE = 120
        self.il = wx.ImageList(BMP_SIZE, BMP_SIZE)

        self.imglistdict = {}
        for index, champ in enumerate(builder.champions.keys()):
            file = 'data/champion_squares/' + champ + '.png'
            if not os.path.isfile(file):
                continue
            image = wx.Image(file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.imglistdict[index] = self.il.Add(image)

        self.SetImageList(self.il, wx.IMAGE_LIST_NORMAL)

        self.PopulateList()

    def PopulateList(self):
        for key, value in self.imglistdict.items():
            index = self.InsertItem(key, value)
            #self.SetItemData(index, key)


class ChampionFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(800, 600))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        ChampionList(self, -1)


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