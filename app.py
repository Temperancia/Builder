import tkinter
from PIL import ImageTk, Image
from tkinter import ttk
import api
import os
import build
import gameplay


class App:
    def __init__(self):
        self.builder = build.Build()
        self.photos = []
        self.champions = api.get_champions()  # TODO change champions use so build.champions replaces

        # api.get_champion_squares(self.champions)
        # api.get_champion_loading_splash_arts(self.champions)
        # api.get_items_squares(self.build.items)

        self.app = tkinter.Tk()
        self.app.title("LOL Builder")

        self.champions_frame = tkinter.Frame(self.app)
        self.splash_art_frame = tkinter.Frame(self.app)
        self.stats_frame = tkinter.Frame(self.app)
        self.build_frame = tkinter.Frame(self.app)
        self.items_frame = tkinter.Frame(self.app)

        self.champions_frame.grid(row=0, column=0, rowspan=2, sticky='N')
        self.splash_art_frame.grid(row=0, column=1, sticky='N')
        self.stats_frame.grid(row=0, column=2, pady=20, sticky='N')
        self.build_frame.grid(row=1, column=1, sticky='NS')
        self.items_frame.grid(row=0, column=3, rowspan=2, sticky='N')

        style = ttk.Style(self.app)

        style.configure('Treeview', rowheight=120, background="green")

        self.tree = ttk.Treeview(self.champions_frame, height=4, selectmode='browse', show='tree')
        self.tree["columns"] = "Name"
        scrollbar = ttk.Scrollbar(self.champions_frame, command=self.tree.yview)
        scrollbar.grid(column=1, row=0, sticky='NS')
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(column=0, row=0, sticky='N')
        self.tree.bind("<1>", self.pick_champion)
        for key, value in self.champions.items():
            file = 'data/champion_squares/' + key + '.png'
            if not os.path.isfile(file):
                continue
            photo = ImageTk.PhotoImage(Image.open(file))
            self.photos.append(photo)
            self.tree.insert('', 'end', open=True, values=(value['name'], key), image=photo)

        self.splash_art = tkinter.Label(self.splash_art_frame)
        self.splash_art.grid(sticky='N')

        self.build = []
        row = 0
        column = 0
        for i in range(6):
            photo = ImageTk.PhotoImage(Image.open('data/Inventory_slot_background.png'))
            self.photos.append(photo)
            slot = tkinter.Label(self.build_frame, image=photo)
            label = tkinter.Label(self.build_frame)
            label.number = i
            label.bind("<1>", self.remove_item)
            self.build.append(label)
            slot.grid(row=row, column=column, padx=10, pady=10, stick='N')
            label.grid(row=row, column=column, padx=10, pady=10, sticky='N')
            column += 1
            if column % 3 == 0:
                row += 1
                column = 0

        self.items = ttk.Treeview(self.items_frame, height=4, selectmode='browse', show='tree')
        self.items["columns"] = "Name"
        items_scrollbar = ttk.Scrollbar(self.items_frame, command=self.items.yview)
        items_scrollbar.grid(column=1, row=0, sticky='NS')
        self.items.configure(yscrollcommand=items_scrollbar.set)
        self.items.grid(column=0, row=0, sticky='N')
        self.items.bind("<1>", self.pick_item)

        self.items_not_displayed = {}
        for key, value in self.builder.items.items():

            tags = ''
            if value['name'] == 'Head of Kha\'Zix':
                tags += 'Rengar'

            file = 'data/item_squares/' + key + '.png'
            if not os.path.isfile(file):
                continue
            photo = ImageTk.PhotoImage(Image.open(file))
            self.photos.append(photo)
            self.items.insert('', 'end', values=(value['name'], key), tags=tags, image=photo)
            # i add all the items at first , every single one with tags
        self.__update_item_tree()

        self.statistics = {}
        for key in gameplay.Champion(self.champions['Aatrox']).statistics.keys():
            label = tkinter.Label(self.stats_frame)
            self.statistics[key] = label
            label.grid()

        self.app.mainloop()

    # this function is where it happens , called first AND each time a champion is picked
    # 2 parts of this function
    #   1 the things you remove : you take one by one each id of all the fruits to examine the tag
    #   if a tag with a special condition is identified then you save the fruit with its index inside the tree
    #   2 the things you bring : now you check your tags from the not displayed dict which contains
    #   items you have removed from prior
    #   if a tag is identified + condition then you use the temporary save from not displayed to reinsert
    #   the node with the correct position
    def __update_item_tree(self):
        champion = self.builder.champion
        for id in self.items.get_children():

            item = self.items.item(id)
            item['index'] = self.items.index(id)

            if 'Rengar' in item['tags'] and (champion is None or champion.name != 'Rengar'):
                self.items_not_displayed[id] = item
                self.items.delete(id)

        # when called by pick_champion , we look for not displayed items
        if champion is not None:
            for key, value in list(self.items_not_displayed.items()):
                if 'Rengar' in value['tags'] and champion.name == 'Rengar':
                    tmp = self.items_not_displayed[key]
                    self.items.insert('', tmp['index'], values=tmp['values'], tags=tmp['tags'], image=tmp['image'])
                    del self.items_not_displayed[key]

    def pick_champion(self, event):
        item = self.tree.identify_row(event.y)
        key = self.tree.item(item, 'values')[1]
        self.builder.set_champion(key)

        file = 'data/loading_splash_arts/' + key + '.jpg'
        if not os.path.isfile(file):
            return
        image = Image.open(file)
        image = image.resize((165, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.photos.append(photo)
        self.splash_art.configure(image=photo)

        self.__update_item_tree()

        for key, value in self.builder.champion.statistics.items():
            text = str(value.current_value) + ' ' + value.name
            self.statistics[key].configure(text=text)

    def pick_item(self, event):
        item = self.items.identify_row(event.y)
        key = self.items.item(item, 'values')[1]
        index = self.builder.add_item(key)
        if index != -1:
            file = 'data/item_squares/' + key + '.png'
            if not os.path.isfile(file):
                return
            image = Image.open(file)
            photo = ImageTk.PhotoImage(image)
            self.photos.append(photo)
            self.build[index].configure(image=photo)

    def remove_item(self, event):
        print(event.widget.number)
        self.builder.remove_item(event.widget.number)
        event.widget.configure(image='')
