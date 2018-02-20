import wx
import os
import build

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
        self.selection = ''

    def on_click(self, _event):
        self.selection = self.img_list[self.GetFirstSelected()]['key']
        file = 'data/loading_splash_arts/' + self.selection + '.jpg'
        width, height = self.image.GetBitmap().GetSize()
        image = make_image(file, width, height, 'data/inventory_slot_background.png')
        self.image.SetBitmap(image)
        self.parent.Layout()


class ItemList(List):
    def __init__(self, parent, size, items):
        super().__init__(parent, size, 64, builder.items.items(), 'data/item_squares/')
        self.items = items
        self.selection = ['', '', '']

    def on_click(self, _event):
        for index, item in enumerate(self.items):
            if not item.active:
                self.selection[index] = self.img_list[self.GetFirstSelected()]['key']
                file = 'data/item_squares/' + self.selection[index] + '.png'
                width, height = item.GetBitmap().GetSize()
                image = make_image(file, width, height, 'data/inventory_slot_background.png')
                item.SetBitmap(image)
                item.active = True
                self.parent.Layout()
                break


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