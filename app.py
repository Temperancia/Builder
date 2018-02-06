import tkinter
from PIL import ImageTk, Image
from tkinter import ttk
import api
import os
import build
import gameplay


class ItemTree:
    def __init__(self, window, frame, map, modes):
        self.visible = False
        self.callback = window
        self.builder = window.builder
        self.build = window.build
        self.statistics = window.statistics
        self.photos = []
        self.items = ttk.Treeview(frame, height=4, selectmode='browse', show='tree')
        self.items['columns'] = 'Name'
        self.items_scrollbar = ttk.Scrollbar(frame, command=self.items.yview)  # TODO debug scrollbar
        self.items_scrollbar.grid(column=1, row=0, sticky='NS')
        self.items.configure(yscrollcommand=self.items_scrollbar.set)
        self.items.bind('<1>', self.pick_item)
        self.items_not_displayed = {}
        for key, value in self.builder.items.items():
            #tags = ''
            #if value['name'] == 'Head of Kha\'Zix':
            #    tags += 'Rengar'

            file = 'data/item_squares/' + key + '.png'  # TODO encapsulate the image making
            if not os.path.isfile(file):
                continue
            photo = ImageTk.PhotoImage(Image.open(file))
            self.photos.append(photo)

            if value['maps'][map]:
                if modes == 'all':
                    self.items.insert('', 'end', values=(value['name'], key), image=photo)
                elif 'tags' in value:
                    tags = [item.lower() for item in value['tags']]
                    for mode_key, mode_value in modes.items():
                        mode_key = mode_key.lower()
                        if mode_key in tags and mode_value:
                            self.items.insert('', 'end', values=(value['name'], key), image=photo)  # TODO adapt champion specific tags
                            break
        self.update_item_tree()

    def display(self):
        self.items.grid(row=0, column=0)

    def destroy(self):
        self.items.destroy()
        self.items_scrollbar.destroy()

    def update_item_tree(self):
        for id in self.items.get_children():
            item = self.items.item(id)
            item['index'] = self.items.index(id)

           # if 'Rengar' in item['tags'] and (self.builder.champion is None or self.builder.champion.name != 'Rengar'):
            #    self.items_not_displayed[id] = item
             #   self.items.delete(id)

        if self.builder.champion is not None:
            for key, value in list(self.items_not_displayed.items()):
                if 'Rengar' in value['tags'] and self.builder.champion.name == 'Rengar':
                    tmp = self.items_not_displayed[key]
                    self.items.insert('', tmp['index'], values=tmp['values'], tags=tmp['tags'], image=tmp['image'])
                    del self.items_not_displayed[key]

    def pick_item(self, event):
        item = self.items.identify_row(event.y)
        key = self.items.item(item, 'values')[1]
        index = self.builder.add_item(key)
        if index != -1:
            file = 'data/item_squares/' + key + '.png'
            image = Image.open(file)
            photo = ImageTk.PhotoImage(image)
            self.photos.append(photo)
            self.build[index].configure(image=photo)
        if self.builder.champion:
            self.callback.update_stats()


class DisplayWindow:
    def __init__(self, app):
        self.window = tkinter.Toplevel(app.app)
        self.photos = []

        for index, window in enumerate(app.windows):

            self.splash_art_frame = tkinter.Frame(self.window)
            self.stats_frame = tkinter.Frame(self.window)
            self.build_frame = tkinter.Frame(self.window)

            self.splash_art_frame.grid(row=0, column=index * 2, sticky='N')
            self.stats_frame.grid(row=0, column=index * 2 + 1, pady=20, sticky='N')
            self.build_frame.grid(row=1, column=index * 2, sticky='NS')

            self.splash_art = tkinter.Label(self.splash_art_frame)
            self.splash_art.grid(sticky='N')
            file = 'data/loading_splash_arts/' + window.builder.champion.key + '.jpg'
            image = Image.open(file)
            image = image.resize((165, 300), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.photos.append(photo)
            self.splash_art.configure(image=photo)

            for key, value in window.builder.champion.statistics.items():
                text = str(value.current_value) + ' ' + value.name
                label = tkinter.Label(self.stats_frame, text=text)
                label.grid()

            row = 0
            column = 0
            for item in window.builder.equipment.stuff:
                photo = ImageTk.PhotoImage(Image.open('data/Inventory_slot_background.png'))
                self.photos.append(photo)
                slot = tkinter.Label(self.build_frame, image=photo)
                slot.grid(row=row, column=column, padx=10, pady=10, stick='N')

                if item:
                    file = 'data/item_squares/' + item.key + '.png'
                    image = Image.open(file)
                    photo = ImageTk.PhotoImage(image)
                    self.photos.append(photo)
                    label = tkinter.Label(self.build_frame, image=photo)
                    label.grid(row=row, column=column, padx=10, pady=10, sticky='N')
                column += 1
                if column % 3 == 0:
                    row += 1
                    column = 0


class SelectionWindow:  # TODO current item tree
    def __init__(self, app):
        self.callback = app
        self.window = tkinter.Toplevel(app.app)
        self.previous_selections = []
        for window in app.windows:  # TODO items selected
            self.previous_selections.append(window.builder.champion.key)
        self.builder = build.Build()
        self.photos = []

        self.champions_frame = tkinter.Frame(self.window)
        self.splash_art_frame = tkinter.Frame(self.window)
        self.stats_frame = tkinter.Frame(self.window)
        self.build_frame = tkinter.Frame(self.window)
        self.save_frame = tkinter.Frame(self.window)
        self.item_modes_frame = tkinter.Frame(self.window)
        self.items_frame = tkinter.Frame(self.window)

        self.champions_frame.grid(row=1, column=0, rowspan=2, sticky='N')
        self.splash_art_frame.grid(row=1, column=1, sticky='N')
        self.stats_frame.grid(row=1, column=2, pady=20, sticky='N')
        self.build_frame.grid(row=2, column=1)
        self.save_frame.grid(row=2, column=2)
        self.item_modes_frame.grid(row=0, column=3)
        self.items_frame.grid(row=1, column=3, rowspan=2, sticky='N')

        style = ttk.Style(self.window)
        style.configure('Treeview', rowheight=120, background='green')

        self.champions = ttk.Treeview(self.champions_frame, height=4, selectmode='browse', show='tree')
        self.champions['columns'] = 'Name'
        scrollbar = ttk.Scrollbar(self.champions_frame, command=self.champions.yview)
        scrollbar.grid(column=1, row=0, sticky='NS')
        self.champions.configure(yscrollcommand=scrollbar.set)
        self.champions.grid(column=0, row=0, sticky='N')
        self.champions.bind('<1>', self.pick_champion)
        for key, value in self.builder.champions.items():
            file = 'data/champion_squares/' + key + '.png'
            if not os.path.isfile(file) or key in self.previous_selections:
                continue
            photo = ImageTk.PhotoImage(Image.open(file))
            self.photos.append(photo)
            self.champions.insert('', 'end', open=True, values=(value['name'], key), image=photo)

        self.splash_art = tkinter.Label(self.splash_art_frame)
        self.splash_art.grid(sticky='N')

        self.statistics = {}
        for key in gameplay.Champion('Aatrox', self.builder.champions['Aatrox']).statistics.keys():
            label = tkinter.Label(self.stats_frame)
            self.statistics[key] = label
            label.grid(sticky='NW')

        self.build = []
        row = 0
        column = 0
        for i in range(6):
            photo = ImageTk.PhotoImage(Image.open('data/Inventory_slot_background.png'))
            self.photos.append(photo)
            slot = tkinter.Label(self.build_frame, image=photo)
            label = tkinter.Label(self.build_frame)
            label.number = i
            label.bind('<1>', self.remove_item)
            self.build.append(label)
            slot.grid(row=row, column=column, padx=10, pady=10, stick='N')
            label.grid(row=row, column=column, padx=10, pady=10, sticky='N')
            column += 1
            if column % 3 == 0:
                row += 1
                column = 0

        self.save = tkinter.Button(self.save_frame, text='OK', command=self.callback.save_selection)
        self.save.grid(sticky='NS')

        self.modes = {}
        index = 0
        for stat in self.builder.tree:  # TODO make dict with actual names instead of tags
            if len(stat['tags']) == 0:
                continue
            for tag in stat['tags']:
                self.check = tkinter.Checkbutton(self.item_modes_frame, text=tag)
                self.check.tag = tag
                self.check.bind('<1>', self.update_items)
                self.check.grid(row=int(index / 4), column=index % 4, sticky='NW')
                self.modes[tag] = False
                index += 1

        self.items = ItemTree(self, self.items_frame, '11', self.modes)
        self.items.display()

    def update_stats(self):
        for key, value in self.builder.champion.statistics.items():  # TODO round values
            text = str(value.current_value) + ' ' + value.name
            self.statistics[key].configure(text=text)

    def pick_champion(self, event):
        item = self.champions.identify_row(event.y)
        key = self.champions.item(item, 'values')[1]
        self.builder.set_champion(key)
        file = 'data/loading_splash_arts/' + key + '.jpg'
        image = Image.open(file)
        image = image.resize((165, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.photos.append(photo)
        self.splash_art.configure(image=photo)
        self.items.update_item_tree()
        self.update_stats()

    def remove_item(self, event):
        self.builder.remove_item(event.widget.number)
        event.widget.configure(image='')
        if self.builder.champion:
            self.update_stats()

    def update_items(self, event):  # TODO anytime nothing is ticked => message instead displayed
        key = event.widget.tag  # TODO all button to tick
        if self.modes[key]:
            self.modes[key] = False
        else:
            self.modes[key] = True

        self.items.destroy()
        self.items = ItemTree(self, self.items_frame, '11', self.modes)
        self.items.display()


class App:
    def __init__(self):  # TODO make ref to build for champions and items from the api
        self.app = tkinter.Tk()
        self.app.title("LOL Builder")
        self.app.withdraw()

        self.windows = []
        self.current_window = SelectionWindow(self)

        # api.get_champion_squares(self.builder.champions)
        # api.get_champion_loading_splash_arts(self.builder.champions)
        # api.get_items_squares(self.builder.items)

        self.app.mainloop()

    def save_selection(self):
        if not self.current_window.builder.champion:
            return
        self.windows.append(self.current_window)
        self.current_window.window.destroy()
        if len(self.windows) == 2:
            self.current_window = DisplayWindow(self)
        else:
            self.current_window = SelectionWindow(self)

