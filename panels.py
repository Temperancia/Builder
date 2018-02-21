from widgets import *


class ChampionSelectionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #self.sizer.AddSpacer(10)

        image = make_image(
            file='data/question_mark2.png',
            mask='data/inventory_slot_background.png'
        )
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


class ItemSelectionPanel(wx.Panel):
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


class DisplaySelectionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.sizer = wx.GridSizer(rows=8, cols=5, hgap=2, vgap=2)

        champion_image = make_image(
            file='data/question_mark2.png',
            width=50,
            height=150,
            mask='data/inventory_slot_background.png'
        )
        item_image = make_image(
            file='data/inventory_slot_background.png',
            width=52,
            height=52,
            mask='data/inventory_slot_background.png'
        )
        self.selected = [[False, False, False, False, False], [False, False, False, False, False]]
        self.images = []
        for row in range(8):
            self.images.append([])
            if row % 4 == 0:
                for column in range(5):
                    image = wx.StaticBitmap(self, bitmap=champion_image)
                    self.images[row].append(image)
                    self.sizer.Add(image, 1, wx.ALIGN_CENTRE)
            else:
                for column in range(5):
                    image = ItemBitmap(self, bitmap=item_image)
                    self.images[row].append(image)
                    self.sizer.Add(image, 1, wx.ALIGN_CENTRE)

        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

    def on_new_selection(self):
        champion = 0
        for index, selected in enumerate(self.selected[0]):
            if not selected:
                champion = index
                self.selected[0][index] = True
                break
        file = 'data/loading_splash_arts/' + self.parent.selections[champion]['champion'] + '.jpg'
        image = make_image(file=file, width=50, height=150, mask='data/inventory_slot_background.png')
        self.images[0][champion].SetBitmap(image)
        for index, key in enumerate(self.parent.selections[champion]['items']):
            file = 'data/item_squares/' +  key + '.png'
            image = make_image(file=file, width=52, height=52, mask='data/inventory_slot_background.png')
            self.images[index + 1][champion].SetBitmap(image)

        return
        for image in self.images[0]:
            for index, item in enumerate(self.parent.selections[0]['items']):
                file = 'data/item_squares/' + item + '.png'
                image = make_image(file=file, width=52, height=52, mask='data/inventory_slot_background.png')
                item_set[index].SetBitmap(image)

        self.Layout()

