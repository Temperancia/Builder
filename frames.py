from panels import *


class ChampionFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 700))
        self.parent = parent
        self.selection = None
        self.__init_ui()
        self.Centre()
        self.Show()

    def __init_ui(self):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.AddSpacer(10)

        self.champion_panel = ChampionSelectionPanel(self)
        self.item_panel = ItemSelectionPanel(self)
        font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        button = wx.Button(self, label="Save and continue")
        button.SetFont(font1)
        button.Bind(wx.EVT_BUTTON, self.on_save)

        self.sizer.AddMany([
            (self.champion_panel, 1, wx.EXPAND),
            (self.item_panel, 1, wx.EXPAND),
            (button, 1, wx.TOP | wx.RIGHT, 10)
        ])
        self.SetSizerAndFit(self.sizer)

    def on_save(self, _event):
        self.Close(True)
        self.selection = {
            'champion': self.champion_panel.champion_list.selection,
            'items': self.item_panel.item_list.selection
        }
        self.parent.callback_new_champion()


class MDIFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='LOL Builder', size=(1000, 700))
        self.selections = []
        self.current_selection = None
        self.__init_ui()

    def __init_ui(self):
        menu = wx.Menu()
        menu.Append(1, "&New Window")
        menu.Append(2, "&Exit")
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, "&File")
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_new_champion, id=1)
        self.Bind(wx.EVT_MENU, self.on_exit, id=2)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.AddSpacer(10)

        self.selection_panel = DisplaySelectionPanel(self)

        self.sizer.AddMany([
            (self.selection_panel, 1, wx.EXPAND)
        ])
        self.SetSizerAndFit(self.sizer)

    def on_exit(self, _evt):
        self.Close(True)

    def on_new_champion(self, _evt):
        self.current_selection = ChampionFrame(self, 'Champion')

    def callback_new_champion(self):
        self.selections.append(self.current_selection.selection)
        self.selection_panel.on_new_selection()

