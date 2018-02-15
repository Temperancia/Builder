import wx
import build
import os

builder = build.Build()


def make_image(file, width=None, height=None):
    image = wx.Image(file, wx.BITMAP_TYPE_ANY)
    if not width:
        width = image.GetWidth()
    if not height:
        height = image.GetHeight()
    return image.Scale(width, height).ConvertToBitmap()


class List(wx.ListCtrl):
    def __init__(self, parent, pos, size, item_size, source, source_path, display_path, image):
        wx.ListCtrl.__init__(self, parent,
                             style=wx.LC_ICON | wx.BORDER_NONE | wx.LC_NO_HEADER,
                             pos=pos,
                             size=size
                             )
        self.source_path = source_path
        self.display_path = display_path
        self.image = image
        self.il = wx.ImageList(item_size, item_size)

        self.img_list = []
        for key, value in source:
            file = source_path + key + '.png'
            if not os.path.isfile(file):
                continue
            image = make_image(file)
            name = value['name'].lower()
            self.img_list.append({'key': key, 'name': name, 'image': self.il.Add(image), 'keywords': name.split(' ')})
        self.SetImageList(self.il, wx.IMAGE_LIST_NORMAL)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_click, self)

        self.populate_list()

    def populate_list(self, selection=None):
        if selection:
            selection = selection.lower()
        self.ClearAll()
        for index, value in enumerate(self.img_list):
            if not selection or value['name'].startswith(selection) \
                    or True in map(lambda word: word.startswith(selection), value['keywords']):
                self.InsertItem(index, value['image'])

    def on_click(self, _event):
        file = self.display_path + self.img_list[self.GetFirstSelected()]['key'] + '.jpg'
        image = make_image(file, 165, 300)
        self.image.SetBitmap(image)


class ChampionList(List):
    def __init__(self, parent, pos, size, image):
        super().__init__(parent, pos, size, 120, builder.champions.items(), 'data/champion_squares/', 'data/loading_splash_arts/', image)


class ItemList(List):
    def __init__(self, parent, pos, size):
        super().__init__(parent, pos, size, 64, builder.items.items(), 'data/item_squares/', None, None)


class ChampionFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(1200, 800))

        self.__init_ui()
        # self.Centre()
        self.Show()

    def __items_selection(self, event):
        text = self.item_text.GetLineText(0)
        self.item_list.populate_list(text)

    def __init_ui(self):
        self.champion_image = wx.StaticBitmap(self, pos=(0, 400))
        self.champion_text = wx.TextCtrl(self, pos=(100, 25), size=(200, 50))
        self.champion_text.SetHint('Select a fuck champion')
        self.champion_list = ChampionList(self, (0, 50), (400, 300), self.champion_image)
        self.Bind(wx.EVT_TEXT,
                  lambda event: self.champion_list.populate_list(self.champion_text.GetLineText(0)),
                  self.champion_text)

        self.item_text = wx.TextCtrl(self, pos=(700, 25))
        self.item_text.SetHint('Select a fuck item')
        self.item_list = ItemList(self, (500, 50), (400, 200))
        self.Bind(wx.EVT_TEXT, self.__items_selection, self.item_text)

        self.save_button = wx.Button(self, pos=(950, 500))


class MDIFrame(wx.MDIParentFrame):
    def __init__(self):
        wx.MDIParentFrame.__init__(self, None, -1, "LOL Builder", size=(1200, 800))
        menu = wx.Menu()
        menu.Append(1, "&New Window")
        menu.Append(2, "&Exit")
        menubar = wx.MenuBar()
        menubar.Append(menu, "&File")

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnNewWindow, id=1)
        self.Bind(wx.EVT_MENU, self.OnExit, id=2)

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