import wx
import build
import os
import copy

builder = build.Build()


def make_image(file, width=None, height=None, mask=None):
    image = wx.Image(file, wx.BITMAP_TYPE_ANY)
    if not width:
        width = image.GetWidth()
    if not height:
        height = image.GetHeight()
    if mask:
        image = image.Scale(width - 20, height - 20)
        border = wx.Image(mask, wx.BITMAP_TYPE_ANY).Scale(width, height)
        border.Paste(image, 10, 10)
        return border.ConvertToBitmap()
    return image.Scale(width, height).ConvertToBitmap()


class List(wx.ListCtrl):
    def __init__(self, parent, size, item_size, source, source_path):
        wx.ListCtrl.__init__(self, parent,
                             style=wx.LC_ICON | wx.BORDER_NONE | wx.LC_NO_HEADER,
                             size=size
                             )
        self.parent = parent
        self.selection = []
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
        pass


class ChampionList(List):
    def __init__(self, parent, size, image):
        super().__init__(parent, size, 120, builder.champions.items(), 'data/champion_squares/')
        self.image = image

    def on_click(self, _event):
        file = 'data/loading_splash_arts/' + self.img_list[self.GetFirstSelected()]['key'] + '.jpg'
        width, height = self.image.GetBitmap().GetSize()
        image = make_image(file, width, height, 'data/inventory_slot_background.png')
        self.image.SetBitmap(image)
        self.parent.Layout()


class ItemList(List):
    def __init__(self, parent, size, items):
        super().__init__(parent, size, 64, builder.items.items(), 'data/item_squares/')
        self.items = items

    def on_click(self, _event):
        file = 'data/item_squares/' + self.img_list[self.GetFirstSelected()]['key'] + '.png'
        for item in self.items:
            if not item.active:
                width, height = item.GetBitmap().GetSize()
                image = make_image(file, 148, 148, 'data/inventory_slot_background.png')
                item.SetBitmap(image)
                item.active = True
                self.parent.Layout()
                break


class ChampionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #self.sizer.AddSpacer(10)

        #image = make_image('data/question_mark2.png', 229, 400, 'data/inventory_slot_background.png')
        image = make_image('data/question_mark2.png', 'data/inventory_slot_background.png')
        self.champion_image = wx.StaticBitmap(self, bitmap=image)

        self.champion_text = wx.TextCtrl(self, style=wx.TE_CENTRE)
        self.champion_text.SetHint('Select a fuck champion')
        font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.champion_text.SetFont(font1)

        self.champion_list = ChampionList(self, size=(400, 150), image=self.champion_image)
        self.Bind(wx.EVT_TEXT,
                  lambda event: self.champion_list.populate_list(self.champion_text.GetLineText(0)),
                  self.champion_text)

        self.sizer.AddMany([
            (self.champion_text, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 10),
            (self.champion_list, 2, wx.SHAPED),
            (self.champion_image, 12, wx.ALIGN_CENTRE)
        ])
        self.SetSizer(self.sizer)


class ItemBitmap(wx.StaticBitmap):
    def __init__(self, parent, bitmap):
        wx.StaticBitmap.__init__(self, parent, bitmap=bitmap)
        self.parent = parent
        self.default_bitmap = bitmap
        self.active = False
        self.Bind(wx.EVT_LEFT_DOWN, self.__cmd_remove_item)

    def __cmd_remove_item(self, _event):
        if self.active:
            self.active = False
            self.SetBitmap(self.default_bitmap)


class ItemPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddSpacer(10)

        image = make_image('data/inventory_slot_background.png', 148, 148)
        self.items = [
            ItemBitmap(self, bitmap=image),
            ItemBitmap(self, bitmap=image),
            ItemBitmap(self, bitmap=image)
        ]

        self.item_text = wx.TextCtrl(self)
        self.item_text.SetHint('Select a fuck item')
        font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.item_text.SetFont(font1)

        self.item_list = ItemList(self, size=(400, 150), items=self.items)
        self.Bind(wx.EVT_TEXT, self.__cmd_items_selection, self.item_text)

        self.sizer.AddMany([
            (self.item_text, 1, wx.SHAPED),
            (self.item_list, 1, wx.SHAPED),
            (self.items[0], 2, wx.ALIGN_CENTRE),
            (self.items[1], 2, wx.ALIGN_CENTRE),
            (self.items[2], 2, wx.ALIGN_CENTRE)
        ])
        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)
        self.Show()

    def __cmd_items_selection(self, _event):
        text = self.item_text.GetLineText(0)
        self.item_list.populate_list(text)


class ChampionFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1200, 800))
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.AddSpacer(10)
        self.__init_ui()
        self.Centre()
        self.Show()

    def __init_ui(self):
        font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        button = wx.Button(self, label="Save and continue")
        button.SetFont(font1)
        self.sizer.AddMany([
            (ChampionPanel(self), 1, wx.GROW),
            (ItemPanel(self), 1, wx.GROW),
            (button, 1, wx.TOP | wx.RIGHT, 10)
        ])
        self.SetSizerAndFit(self.sizer)


class MDIFrame(wx.MDIParentFrame):
    def __init__(self):
        wx.MDIParentFrame.__init__(self, None, title="LOL Builder", size=(1200, 800))
        menu = wx.Menu()
        menu.Append(1, "&New Window")
        menu.Append(2, "&Exit")
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, "&File")

        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_new_champion, id=1)
        self.Bind(wx.EVT_MENU, self.on_exit, id=2)

    def on_exit(self, _evt):
        self.Close(True)

    def on_new_champion(self, _evt):
        ChampionFrame(self, 'Champion')


class App:
    def __init__(self):
        app = wx.App()
        frame = MDIFrame()
        frame.Show()
        app.MainLoop()