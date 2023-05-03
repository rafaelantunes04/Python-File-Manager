try:
    import os
    import os.path as path
    import tkinter as tk
    import tkinter.ttk as ttk
    import datetime
    import subprocess
    import traceback
    from PIL import Image, ImageTk

    root = tk.Tk()
    home_dir = path.expanduser('~')
    current_path = path.join(home_dir, 'Desktop')
    current_location = 0
    paths_map = []
    state = "up"

    #Images
    arrow = ImageTk.PhotoImage(Image.open('images/arrow.png'))
    arrow_on = ImageTk.PhotoImage(Image.open('images/arrow_on.png'))
    fliparrow = ImageTk.PhotoImage(Image.open('images/arrow.png').rotate(180))
    fliparrow_on = ImageTk.PhotoImage(Image.open('images/arrow_on.png').rotate(180))
    uparrow = ImageTk.PhotoImage(Image.open('images/arrow.png').rotate(-90))
    reload = ImageTk.PhotoImage(Image.open('images/reload.png'))

    #Window Settings
    root.title('File Explorer')
    root.geometry('960x540')
    root.minsize(640,360)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)
    root.columnconfigure(4, weight=1)
    root.rowconfigure(1, weight=1)

    #Functions

    def show_menu(event):
        if event.widget.selection():
            menusel.post(event.x_root, event.y_root)
        else:
            menudesel.post(event.x_root, event.y_root)

    def size_format(size):
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        unit_index = 0
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024.0
            unit_index += 1
        return str(round(size)) + units[unit_index]

    def load_folders(cur_path):
        global current_path, paths_map, current_location, state
        cur_path = cur_path.rstrip()
        if not cur_path.endswith("\\"):
            cur_path += "\\"

        #To Watch
        if current_path != cur_path and state == "up":
            try:
                if paths_map[current_location+1] == cur_path:
                    current_location += 1
                else:
                    paths_map = paths_map[:current_location]
                    paths_map.append(cur_path)
                    current_location += 1
            except:
                paths_map = paths_map[:current_location]
                paths_map.append(cur_path)
                current_location += 1

        current_path = cur_path

        for item in folder_view_widget.get_children():
            folder_view_widget.delete(item)

        for entry in os.scandir(current_path):
            time = datetime.datetime.fromtimestamp(path.getmtime(path.join(current_path, entry.name))).strftime('%d/%m/%Y %H:%M')
            size = size_format(entry.stat().st_size)

            if path.isdir(path.join(current_path, entry.name)):
                type = 'File Folder'
                folder_view_widget.insert('','end',values=(entry.name, time, type, size))
            else:
                name, type = entry.name.rsplit('.', 1)
                folder_view_widget.insert('','end',values=(entry.name, time, '.' + type + ' File', size))

        if current_location == 1:
            backarrow.config(state="disabled")
        else:
            backarrow.config(state="normal")

        if len(paths_map) == current_location:
            frontarrow.config(state="disabled")
        else:
            frontarrow.config(state="normal")

        path_text_widget.delete(0, 'end')    
        path_text_widget.insert(0, current_path)

    def on_path_changed(event):
        global current_path
        if path.exists(path_text_widget.get()):
            current_path = path_text_widget.get()
            load_folders(current_path)
        else:
            path_text_widget.delete(0, 'end')    
            path_text_widget.insert(0, current_path)

    def on_folder_doubleclick(event):
        selection = event.widget.selection()
        if selection:
            item = event.widget.item(selection)
            name = item["values"][0]
            if path.isdir(path.join(current_path, name)):
                load_folders(path.join(current_path, name))
            else:
                subprocess.Popen([path.join(current_path, name)], shell=True)

    def on_folderview_click(event):
        item = folder_view_widget.identify('item', event.x, event.y)
        if not item:
            folder_view_widget.selection_remove(folder_view_widget.selection())

    def on_quickaccess_click(event):
        item_id = event.widget.identify_row(event.y)
        name = event.widget.item(event.widget.identify_row(event.y))['text']
        parent_folder = event.widget.item(event.widget.parent(item_id))['text']
        if not item_id:
            quick_access_widget.selection_remove(quick_access_widget.selection())
        else:
            if name == "This PC":
                load_folders(home_dir)
            elif name in directories or parent_folder in directories:
                if path.exists(path.join(home_dir, name)):
                    load_folders(path.join(home_dir, name))
                else:
                    load_folders(path.join(home_dir, parent_folder, name))
            else:
                try:
                    if path.exists(parent_folder[parent_folder.index('(')+1:parent_folder.index(')')] + "\\" + name):
                        load_folders(parent_folder[parent_folder.index('(')+1:parent_folder.index(')')] + "\\" + name)
                except:
                    load_folders(name[name.index('(')+1:name.index(')')])

    def search(search_term):
        global current_path
        load_folders(current_path)
        results = []
        for item in folder_view_widget.get_children():
            item = folder_view_widget.item(item)
            item = item["values"][0]
            if search_term.lower() in item.lower():
                results.append(item)
        return results

    def on_search(event):
        global current_path
        results = search(search_text_widget.get()) 

        for item in folder_view_widget.get_children():
            folder_view_widget.delete(item)

        if search_text_widget.get() == '':
            load_folders(current_path)
        else:
            for each in results:
                for entry in os.scandir(current_path):
                    if entry.name.lower() == each.lower():
                        time = datetime.datetime.fromtimestamp(path.getmtime(path.join(current_path, entry.name))).strftime('%d/%m/%Y %H:%M')
                        size = size_format(entry.stat().st_size)

                        if path.isdir(path.join(current_path, entry.name)):
                            type = 'File Folder'
                            folder_view_widget.insert('','end',values=(entry.name, time, type, size))
                        else:
                            name, type = entry.name.rsplit('.', 1)
                            folder_view_widget.insert('','end',values=(entry.name, time, '.' + type + ' File', size))

    def travel_path(direction):
        global current_location, paths_map, state
        if direction == "down":
            current_location -= 1
            state = "down"
            load_folders(paths_map[current_location-1])
        if direction == "up":
            current_location += 1
            state = "up"
            load_folders(paths_map[current_location-1])




    #Top setup
    top_panel = tk.PanedWindow(root)
    top_panel.grid(row=0, column=1, sticky='nsew', pady=10, columnspan=4)

        #Left Widgets
    backarrow = tk.Button(root, image=arrow, command=lambda: travel_path("down"))
    backarrow.grid(row=0, column=0, sticky='nsw', padx=(5,5), pady=10)
    frontarrow = tk.Button(root, image=fliparrow, command=lambda: travel_path("up"))
    frontarrow.grid(row=0, column=0, padx=(25,0), sticky='nsw', pady=10)
    toparrow = tk.Button(root, image=uparrow)
    toparrow.grid(row=0, column=0, padx=(50,0), sticky='nsw', pady=10)
    themebutton = tk.Button(root, image=reload)
    themebutton.grid(row=0, column=0, padx=(75,5), sticky='nsw', pady=10)

            #Left Widgets Settings

    backarrow.configure(relief='flat')
    frontarrow.configure(relief='flat')
    toparrow.configure(relief='flat')
    themebutton.configure(relief='flat')


        #Path Text
    path_text = tk.Frame(top_panel)

            #Path Text Widget
    path_text_widget = tk.Entry(path_text, width=100)
    path_text_widget.bind("<Return>", on_path_changed)
    path_text_widget.pack(side='left', fill='both', expand=True, padx=5)

        #Search Text
    search_text = tk.Frame(top_panel)

            #Search Text Widget
    search_text_widget = tk.Entry(search_text)
    search_text_widget.bind("<Return>", on_search)
    search_text_widget.pack(side='right', fill='both',expand=True, padx=5)

            #Top Panel Settings
    top_panel.add(path_text)
    top_panel.add(search_text)
    top_panel.paneconfigure(path_text, minsize=200)
    top_panel.paneconfigure(search_text, minsize=200)





    #Bottom setup
    bottom_panel = tk.PanedWindow(root)
    bottom_panel.grid(row=1, column=0, columnspan=5, sticky='nsew')

        #Left panel
    quick_access = tk.Frame(bottom_panel)

            #quick access widget
    quick_access_widget = ttk.Treeview(quick_access)
    quick_access_widget.heading('#0', text='Quick access', anchor='c')
    quick_access_widget.bind('<Button-1>', on_quickaccess_click)
    quick_access_widget.pack(side='left', fill='both',expand=True)


            #quick access scrollbar
    quick_access_scrollbar = ttk.Scrollbar(quick_access_widget, orient='vertical', command=quick_access_widget.yview)
    quick_access_scrollbar.pack(side='right', fill='y')
    quick_access_widget.configure(yscrollcommand=quick_access_scrollbar.set)

                #quick access folder insertion
    this_pc = quick_access_widget.insert('', 'end', text='This PC', open=True)
    directories = ['Desktop', 'Documents', 'Pictures', 'Music', '3D Objects', 'Downloads', 'Videos']

                    #Default system folder insertion
    for dir in directories:
        if path.exists(path.join(home_dir, dir)):
            subfolder = quick_access_widget.insert(this_pc, 'end', text=dir, open=False)
            for entry in os.listdir(path.join(home_dir, dir)):
                if path.isdir(path.join(home_dir, dir, entry)):
                    quick_access_widget.insert(subfolder, 'end', text=entry, open=False)

                    #Disk insertion
    for i in range(65, 91):
        drive_name = chr(i) + ':'
        if path.exists(drive_name):
            subfolder = quick_access_widget.insert(this_pc, 'end', text=f"Disk ({drive_name})", open=False)
            for entry in os.listdir(path.join(drive_name, '\\')):
                if path.isdir(path.join(path.join(drive_name, '\\'), entry)):
                    quick_access_widget.insert(subfolder, 'end', text=entry, open=False)



        #Right Panel
    folder_view = tk.Frame(bottom_panel, relief="flat")

            #folder view widget
    folder_view_widget = ttk.Treeview(folder_view, selectmode="browse")
    folder_view_widget.bind("<Double-Button-1>", on_folder_doubleclick)
    folder_view_widget.bind('<Button-1>', on_folderview_click)
    folder_view_widget.bind("<Button-3>", show_menu)
    folder_view_widget.pack(side='left', fill='both',expand=True)

            #folder view scrollbar
    folder_view_scrollbar = ttk.Scrollbar(folder_view_widget, orient='vertical', command=folder_view_widget.yview)
    folder_view_scrollbar.pack(side='right', fill='y')
    folder_view_widget.configure(yscrollcommand=folder_view_scrollbar.set)

                #folder view folders setup

                    #columns
    folder_view_widget['columns'] = ('1', '2', '3', '4')
    folder_view_widget['show'] = 'headings'
    folder_view_widget.column('1', anchor='w', stretch=0, minwidth=50)
    folder_view_widget.column('2', anchor='w', stretch=0, minwidth=50)
    folder_view_widget.column('3', anchor='w', stretch=0, minwidth=50, width=120)
    folder_view_widget.column('4', anchor='e', stretch=0, minwidth=50)
    folder_view_widget.heading('1', text='Name', anchor='w')
    folder_view_widget.heading('2', text='Date of Modification', anchor='w')
    folder_view_widget.heading('3', text='Type', anchor='w')
    folder_view_widget.heading('4', text='Size', anchor='w')

                    #folders
    load_folders(current_path)

        #Bottom Panel Settings Setup
    bottom_panel.add(quick_access, width=200)
    bottom_panel.add(folder_view)
    bottom_panel.paneconfigure(quick_access, minsize=50)
    bottom_panel.paneconfigure(folder_view, minsize=50)

    #Menu selected
    menusel = tk.Menu(folder_view_widget, tearoff=0)
    menusel.add_command(label="Open")
    menusel.add_separator()
    menusel.add_command(label="Cut")
    menusel.add_command(label="Copy")
    menusel.add_separator()
    menusel.add_command(label="Rename")
    menusel.add_command(label="Delete")

    #Menu deselected/createnew
    menudesel = tk.Menu(folder_view_widget, tearoff=0)

    createnewmenu = tk.Menu(menudesel, tearoff=0)

    menudesel.add_command(label="Reload", command=lambda: load_folders(current_path))
    menudesel.add_cascade(label="Create New", menu=createnewmenu)
    menudesel.add_command(label="Paste")

    createnewmenu.add_command(label="Folder")
    createnewmenu.add_command(label="Text Document")

    root.mainloop()
except Exception as e:
    print(e)
    input(traceback.format_exc())