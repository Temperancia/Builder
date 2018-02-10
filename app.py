import tkinter
from PIL import ImageTk, Image
from tkinter import ttk
import api
import os
import build
import gameplay

photos = []


def make_image(file, width=None, height=None):
    if not os.path.isfile(file):
        return None
    image = Image.open(file)
    image_width, image_height = image.size
    if not width:
        width = image_width
    if not height:
        height = image_height
    image = image.resize((width, height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    photos.append(photo)
    return photo


class ItemTree:
    def __init__(self, window, frame, map, modes):
        self.visible = False
        self.callback = window
        self.builder = window.builder
        self.build = window.build
        self.statistics = window.current_statistics
        self.photos = []
        self.items = ttk.Treeview(frame, height=3, selectmode='browse', show='tree')
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
            self.build[index].active = True
            self.build[index].configure(image=make_image('data/item_squares/' + key + '.png'))
        if self.builder.champion:
            self.callback.update_stats()


class DisplayWindow:
    def __init__(self, app):
        self.callback = app
        self.window = tkinter.Toplevel(app.app)
        self.window.protocol("WM_DELETE_WINDOW", app.quit)  # TODO too many frames => remove and test with less

        self.logo_frame = tkinter.Frame(self.window)
        self.logo_frame.grid(row=0, column=1)  # TODO try Label Frame for fun :D

        for index, window in enumerate(app.windows):
            self.message_champion_name_frame = tkinter.Frame(self.window)
            self.splash_art_frame = tkinter.Frame(self.window)
            self.build_frame = tkinter.Frame(self.window)
            self.stats_frame = tkinter.Frame(self.window)
            self.square_frame = tkinter.Frame(self.window)
            self.stats_comparison_frame = tkinter.Frame(self.window)

            self.message_champion_name_frame.grid(row=0, column=index * 4)
            self.splash_art_frame.grid(row=1, column=index * 4)
            self.build_frame.grid(row=2, column=index * 4)
            self.stats_frame.grid(row=3, column=index * 4)
            self.square_frame.grid(row=1, column=index + 1)
            self.stats_comparison_frame.grid(row=2, column=index + 1)

            message_champion_name = tkinter.Label(self.message_champion_name_frame, text=window.builder.champion.name)
            message_champion_name.grid()

            file = 'data/loading_splash_arts/' + window.builder.champion.key + '.jpg'
            splash_art = tkinter.Label(self.splash_art_frame, image=make_image(file, 165, 300))
            splash_art.grid()

            row = 0
            column = 0
            for item in window.builder.equipment.stuff:
                slot = tkinter.Label(self.build_frame, image=make_image('data/Inventory_slot_background.png'))
                slot.grid(row=row, column=column, padx=10, pady=10, stick='N')
                if item:
                    file = 'data/item_squares/' + item.key + '.png'
                    label = tkinter.Label(self.build_frame, image=make_image(file))
                    label.grid(row=row, column=column, padx=10, pady=10, sticky='N')
                column += 1
                if column % 3 == 0:
                    row += 1
                    column = 0

            champion = 1
            if index == 1:
                champion = 0
            other_stats = app.windows[champion].builder.champion.statistics
            for key, value in window.builder.champion.statistics.items():
                text = str(round(value.current_value, 2)) + ' ' + value.name
                label = tkinter.Label(self.stats_frame, text=text)
                label.grid()

                result = value.current_value - other_stats[key].current_value
                text = str(round(result, 2)) + ' ' + value.name
                if result > 0:
                    text = '+' + text
                if result < 0:
                    label = tkinter.Label(self.stats_comparison_frame, text=text, fg='red')
                elif result > 0:
                    label = tkinter.Label(self.stats_comparison_frame, text=text, fg='green')
                label.grid()

            file = 'data/champion_squares/' + window.builder.champion.key + '.png'
            square = tkinter.Label(self.square_frame, image=make_image(file))
            square.grid()


class SelectionWindow:  # TODO current item tree
    def __init__(self, app):
        self.callback = app
        self.window = tkinter.Toplevel(app.app)
        self.window.protocol("WM_DELETE_WINDOW", app.quit)

        self.previous_selections = []
        for window in app.windows:  # TODO items selected
            self.previous_selections.append(window.builder.champion.key)
        self.builder = build.Build()

        self.message_selection_champion_frame = tkinter.Frame(self.window)
        self.title_frame = tkinter.Frame(self.window)
        self.message_selection_items_frame = tkinter.Frame(self.window)

        self.item_modes_frame = tkinter.Frame(self.window)

        self.champions_frame = tkinter.Frame(self.window)
        self.stats_base_frame = tkinter.Frame(self.window)
        self.splash_art_frame = tkinter.Frame(self.window)
        self.stats_current_frame = tkinter.Frame(self.window)
        self.items_frame = tkinter.Frame(self.window)

        self.reset_frame = tkinter.Frame(self.window)
        self.build_frame = tkinter.Frame(self.window, relief='ridge', bg='yellow')
        self.save_frame = tkinter.Frame(self.window, relief='ridge', bg='yellow')

        self.__make_frame_header()
        self.__make_frame_body()
        self.__make_frame_footer()
        self.__display_frames()

    def __display_frames(self):
        self.message_selection_champion_frame.grid(row=0, column=0)
        self.title_frame.grid(row=0, column=2)
        self.message_selection_items_frame.grid(row=0, column=4)

        self.item_modes_frame.grid(row=1, column=4)

        self.champions_frame.grid(row=2, column=0)
        self.stats_base_frame.grid(row=2, column=1)
        self.splash_art_frame.grid(row=2, column=2)
        self.stats_current_frame.grid(row=2, column=3)
        self.items_frame.grid(row=2, column=4)

        self.reset_frame.grid(row=3, column=0)
        self.build_frame.grid(row=3, column=2)
        self.save_frame.grid(row=3, column=4)

    def __make_frame_header(self):

        self.message_selection_champion = tkinter.Label(  # TODO border color ??
            self.message_selection_champion_frame,
            text='Select your champion!',
            background='green',
            borderwidth=2,
            highlightcolor='green',
            highlightbackground='green',
            highlightthickness=10,
            relief='solid'
        )
        self.message_selection_champion.grid()

        self.logo = tkinter.Label(self.title_frame, image=make_image('data/logo.jpg', 100, 100))
        self.logo.grid()

        self.message_selection_items = tkinter.Label(self.message_selection_items_frame, text="Select your items!")
        self.message_selection_items.grid()

    def __make_frame_body(self):
        style = ttk.Style(self.window)
        style.configure('Treeview', rowheight=120, background='green')

        self.champions = ttk.Treeview(self.champions_frame, height=3, selectmode='browse', show='tree')
        self.champions['columns'] = 'Name'
        scrollbar = ttk.Scrollbar(self.champions_frame, command=self.champions.yview)
        scrollbar.grid(column=1, row=0, sticky='NS')
        self.champions.configure(yscrollcommand=scrollbar.set)
        self.champions.grid(column=0, row=0, sticky='N')
        self.champions.bind('<1>', self.pick_champion)
        for key, value in self.builder.champions.items():
            file = 'data/champion_squares/' + key + '.png'
            if key in self.previous_selections:
                continue
            image = make_image(file)
            if not image:
                continue
            self.champions.insert('', 'end', open=True, values=(value['name'], key), image=image)

        self.base_statistics = {}
        for key in gameplay.Champion('Aatrox', self.builder.champions['Aatrox']).statistics.keys():
            label = tkinter.Label(self.stats_base_frame)
            self.base_statistics[key] = label
            label.grid(sticky='NW')

        self.splash_art = tkinter.Label(self.splash_art_frame, image=make_image('data/question_mark.png', 300, 300))
        self.splash_art.grid()

        self.current_statistics = {}
        for key in gameplay.Champion('Aatrox', self.builder.champions['Aatrox']).statistics.keys():
            label = tkinter.Label(self.stats_current_frame)
            self.current_statistics[key] = label
            label.grid(sticky='NW')

        self.build = []
        row = 0
        column = 0
        for i in range(6):
            slot = tkinter.Label(self.build_frame, image=make_image('data/Inventory_slot_background.png'))
            slot.grid(row=row, column=column, padx=10, pady=10, stick='N')
            label = tkinter.Label(self.build_frame)
            label.active = False
            label.number = i
            label.bind('<1>', self.cmd_remove_item)
            self.build.append(label)
            label.grid(row=row, column=column, padx=10, pady=10, sticky='N')
            column += 1
            if column % 3 == 0:
                row += 1
                column = 0

        self.tags_mapping = {
            'GOLDPER': 'Gold per seconde',
            'CONSUMABLE': 'Consumable',
            'VISION': 'Vision',
            'HEALTH': 'Health',
            'HEALTHREGEN': 'Health regen',
            'ARMOR': 'Armor',
            'SPELLBLOCK': 'Magic resist',
            'LIFESTEAL': 'Life steal',
            'CRITICALSTRIKE': 'Critical strike',
            'ATTACKSPEED': 'Attack speed',
            'DAMAGE': 'Damage',
            'MANA': 'Mana',
            'SPELLDAMAGE': 'Spell damage',
            'COOLDOWNREDUCTION': 'Cooldown reduction',
            'SPELLVAMP': 'Spell vamp',
            'MAGICPENETRATION': 'Magic penetration',
            'ARMORPENETRATION': 'Armor penetration',
            'TRINKET': 'Trinket',
            'TENACITY': 'Tenacity'
        }
        self.checks = []
        self.modes = {}
        index = 0
        for stat in self.builder.tree:
            if len(stat['tags']) == 0:
                continue
            for tag in stat['tags']:
                if tag in self.tags_mapping:
                    check = tkinter.Checkbutton(self.item_modes_frame, text=self.tags_mapping[tag])
                    check.deselect()
                    check.tag = tag
                    check.bind('<1>', self.update_items)
                    check.grid(row=int(index / 4), column=index % 4, sticky='NW')
                    self.modes[tag] = False
                    self.checks.append(check)
                    index += 1

        self.items = ItemTree(self, self.items_frame, '11', self.modes)
        self.items.display()

    def __make_frame_footer(self):
        #self.reset_frame, text = 'RESET', command = self.reset_build)
        self.reset = tkinter.Button(self.reset_frame,
                                    image=make_image('data/refresh.png'),
                                    command=self.reset_build,
                                    relief='flat'
                                    )
        self.reset.grid()

        self.save = tkinter.Button(self.save_frame, text='SAVE AND CONTINUE', command=self.callback.save_selection)
        self.save.grid()

    def update_stats(self):
        self.update_base_stats()
        self.update_current_stats()

    def update_base_stats(self):
        for key, value in self.builder.champion.statistics.items():
            text = str(round(value.base_value, 2)) + ' ' + value.name
            self.base_statistics[key].configure(text=text)

    def update_current_stats(self):
        for key, value in self.builder.champion.statistics.items():
            text = str(round(value.current_value, 2)) + ' ' + value.name
            text += ' (' + str(round(value.current_value - value.base_value, 2)) + ')'

            self.current_statistics[key].configure(text=text)

    def remove_item(self, widget):
        self.builder.remove_item(widget.number)
        widget.configure(image='')

    def pick_champion(self, event):
        item = self.champions.identify_row(event.y)
        key = self.champions.item(item, 'values')[1]
        self.builder.set_champion(key)
        file = 'data/loading_splash_arts/' + key + '.jpg'
        self.splash_art.configure(image=make_image(file, 165, 300))
        self.items.update_item_tree()
        self.update_stats()

    def cmd_remove_item(self, event):
        self.remove_item(event.widget)
        if self.builder.champion:
            self.update_current_stats()

    def update_items(self, event):  # TODO anytime nothing is ticked => message instead displayed
        key = event.widget.tag  # TODO all button to tick
        if self.modes[key]:
            self.modes[key] = False
        else:
            self.modes[key] = True

        self.items.destroy()
        self.items = ItemTree(self, self.items_frame, '11', self.modes)
        self.items.display()

    def reset_build(self):
        for item in self.build:
            if item.active:
                self.remove_item(item)
                item.active = False
        if self.builder.champion:
            self.update_current_stats()


class App:
    def __init__(self):  # TODO make ref to build for champions and items from the api
        # TODO efficiency reuse trees between windows
        self.app = tkinter.Tk()
        self.app.tk_setPalette(background='grey')  # TODO invisible checkboxes from this
        self.app.title("LOL Builder")

        self.app.withdraw()

        self.windows = []
        self.current_window = SelectionWindow(self)

        # api.get_champion_squares(self.builder.champions)
        # api.get_champion_loading_splash_arts(self.builder.champions)
        # api.get_items_squares(self.builder.items)

        self.app.mainloop()

    def quit(self):
        exit(0)

    def save_selection(self):
        if not self.current_window.builder.champion:
            return
        self.windows.append(self.current_window)
        self.current_window.window.destroy()
        if len(self.windows) == 2:
            self.current_window = DisplayWindow(self)
        else:
            self.current_window = SelectionWindow(self)

