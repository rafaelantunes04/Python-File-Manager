import os
import os.path as path
import tkinter as tk
import tkinter.ttk as ttk
import datetime
from PIL import Image, ImageTk

root = tk.Tk()
home_dir = path.expanduser('~')
desktop_path = os.path.join(home_dir, 'Desktop')

#Images
arrow = ImageTk.PhotoImage(Image.open('images/arrow_white_theme.png'))
arrow_on = ImageTk.PhotoImage(Image.open('images/arrow_on_white_theme.png'))
fliparrow = ImageTk.PhotoImage(Image.open('images/arrow_white_theme.png').rotate(180))
fliparrow_on = ImageTk.PhotoImage(Image.open('images/arrow_on_white_theme.png').rotate(180))
uparrow = ImageTk.PhotoImage(Image.open('images/arrow_white_theme.png').rotate(-90))
darktheme = ImageTk.PhotoImage(Image.open('images/dark_theme_icon.png'))
whitetheme = ImageTk.PhotoImage(Image.open('images/dark_theme_icon.png'))

#Window Settings
root.title('File Explorer')
root.geometry('960x540')
root.minsize(640,360)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.rowconfigure(1, weight=1)

#Top setup
top_panel = tk.PanedWindow(root)
top_panel.grid(row=0, column=1, sticky='nsew', pady=10, columnspan=4)

    #Left Widgets
backarrow = tk.Button(root, image=arrow)
backarrow.grid(row=0, column=0, sticky='nsw', padx=(5,5), pady=10)
frontarrow = tk.Button(root, image=fliparrow)
frontarrow.grid(row=0, column=0, padx=(25,0), sticky='nsw', pady=10)
toparrow = tk.Button(root, image=uparrow)
toparrow.grid(row=0, column=0, padx=(50,0), sticky='nsw', pady=10)
themebutton = tk.Button(root, image=darktheme)
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
path_text_widget.pack(side='left', fill='both', expand=True, padx=5)

    #Search Text
search_text = tk.Frame(top_panel)

        #Search Text Widget
search_text_widget = tk.Entry(search_text)
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
quick_acess = tk.Frame(bottom_panel)

        #quick acess widget
quick_acess_widget = ttk.Treeview(quick_acess)
quick_acess_widget.heading('#0', text='Quick Acess', anchor='c')
quick_acess_widget.pack(side='left', fill='both',expand=True)


        #quick acess scrollbar
quick_acess_scrollbar = ttk.Scrollbar(quick_acess_widget, orient='vertical', command=quick_acess_widget.yview)
quick_acess_scrollbar.pack(side='right', fill='y')
quick_acess_widget.configure(yscrollcommand=quick_acess_scrollbar.set)

            #quick acess folder insertion
this_pc = quick_acess_widget.insert('', 'end', text='This PC', open=True)
directories = ['Desktop', 'Documents', 'Pictures', 'Music', '3D Objects', 'Downloads', 'Videos']

                #Default system folder insertion
for dir in directories:
    if path.exists(path.join(home_dir, dir)):
        subfolder = quick_acess_widget.insert(this_pc, 'end', text=dir, open=False)
        for entry in os.listdir(path.join(home_dir, dir)):
            if path.isdir(path.join(home_dir, dir, entry)):
                quick_acess_widget.insert(subfolder, 'end', text=entry, open=False)

                #Disk insertion
for i in range(65, 91):
    drive_name = chr(i) + ':'
    if os.path.exists(drive_name):
        subfolder = quick_acess_widget.insert(this_pc, 'end', text=f"Disk ({drive_name})", open=False)
        for entry in os.scandir(drive_name):
            if entry.is_dir() and not entry.stat().st_file_attributes & 2:
                quick_acess_widget.insert(subfolder, 'end', text=entry.name, open=False)



    #Right Panel
folder_view = tk.Frame(bottom_panel, relief="flat")

        #folder view widget
folder_view_widget = ttk.Treeview(folder_view)
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
for entry in os.scandir(desktop_path):
    time = datetime.datetime.fromtimestamp(path.getmtime(os.path.join(desktop_path, entry.name))).strftime('%d/%m/%Y %H:%M')
    size = path.getsize(entry)

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    size = str(round(size)) + units[unit_index]
    
    if path.isdir(os.path.join(desktop_path, entry.name)):
        type = 'File Folder'
        folder_view_widget.insert('','end',values=(entry.name, time, type, size))
    else:
        name, type = entry.name.rsplit('.', 1)
        folder_view_widget.insert('','end',values=(entry.name, time, '.' + type + ' File', size))

    #Bottom Panel Settings Setup
bottom_panel.add(quick_acess, width=200)
bottom_panel.add(folder_view)
bottom_panel.paneconfigure(quick_acess, minsize=50)
bottom_panel.paneconfigure(folder_view, minsize=50)

root.mainloop()