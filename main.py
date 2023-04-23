import os
import os.path as path
import tkinter as tk
import tkinter.ttk as ttk
import datetime
from PIL import Image, ImageTk

#Vars
root = tk.Tk()
home_dir = path.expanduser('~')
desktop_path = os.path.join(home_dir, 'Desktop')
    #Images
arrow = ImageTk.PhotoImage(Image.open('images/arrow_white_theme.png'))
arrow_on = ImageTk.PhotoImage(Image.open('images/arrow_on_white_theme.png'))
fliparrow = ImageTk.PhotoImage(Image.open('images/arrow_white_theme.png').rotate(180))
fliparrow_on = ImageTk.PhotoImage(Image.open('images/arrow_on_white_theme.png').rotate(180))
uparrow = ImageTk.PhotoImage(Image.open('images/arrow_white_theme.png').rotate(-90))

    #Window Settings
root.title('File Explorer')
root.geometry('960x540')
root.minsize(640,360)

#Bottom setup
paned = tk.PanedWindow(root)
paned.grid(row=1, column=0, columnspan=5, sticky='nsew')

frame1 = tk.Frame(paned)
treeview = ttk.Treeview(frame1)
treeview.heading('#0', text='Quick Acess', anchor='w')
treeview.pack(side='left', fill='both',expand=True)

scrollbar1 = ttk.Scrollbar(frame1, orient='vertical', command=treeview.yview)
scrollbar1.pack(side='right', fill='y')

treeview.configure(yscrollcommand=scrollbar1.set)

node = treeview.insert('', 'end', text='This PC', open=True)

for i in os.listdir(home_dir):
    match i:
        case "Desktop":
            node2 = treeview.insert(node, 'end', text=i, open=False)
            for entry in os.listdir(home_dir + "/" + i):
                if path.isdir(path.join(home_dir, i, entry)):
                    treeview.insert(node2, 'end', text=entry, open=False)
        case "Documents":
            node2 = treeview.insert(node, 'end', text=i, open=False)
            for entry in os.listdir(home_dir + "/" + i):
                if path.isdir(path.join(home_dir, i, entry)):
                    treeview.insert(node2, 'end', text=entry, open=False)
        case "Pictures":
            node2 = treeview.insert(node, 'end', text=i, open=False)
            for entry in os.listdir(home_dir + "/" + i):
                if path.isdir(path.join(home_dir, i, entry)):
                    treeview.insert(node2, 'end', text=entry, open=False)
        case "Music":
            node2 = treeview.insert(node, 'end', text=i, open=False)
            for entry in os.listdir(home_dir + "/" + i):
                if path.isdir(path.join(home_dir, i, entry)):
                    treeview.insert(node2, 'end', text=entry, open=False)
        case "3D Objects":
            node2 = treeview.insert(node, 'end', text=i, open=False)
            for entry in os.listdir(home_dir + "/" + i):
                if path.isdir(path.join(home_dir, i, entry)):
                    treeview.insert(node2, 'end', text=entry, open=False)
        case "Downloads":
            node2 = treeview.insert(node, 'end', text=i, open=False)
            for entry in os.listdir(home_dir + "/" + i):
                if path.isdir(path.join(home_dir, i, entry)):
                    treeview.insert(node2, 'end', text=entry, open=False)
        case "Videos":
            node2 = treeview.insert(node, 'end', text=i, open=False)
            for entry in os.listdir(home_dir + "/" + i):
                if path.isdir(path.join(home_dir, i, entry)):
                    treeview.insert(node2, 'end', text=entry, open=False)

for i in range(65, 91):
    drive_name = chr(i) + ':'
    if os.path.exists(drive_name):
        node2 = treeview.insert(node, 'end', text=f"Disk ({drive_name})", open=False)
        for entry in os.scandir(drive_name):
            if entry.is_dir() and not entry.stat().st_file_attributes & 2:
                treeview.insert(node2, 'end', text=entry.name, open=False)

frame2 = tk.Frame(paned, relief="flat")
tree = ttk.Treeview(frame2)
tree.pack(side='left', fill='both',expand=True)

scrollbar = ttk.Scrollbar(tree, orient='vertical', command=tree.yview)
scrollbar.pack(side='right', fill='y')

tree.configure(yscrollcommand=scrollbar.set)

tree['columns'] = ('1', '2', '3', '4')
tree['show'] = 'headings'
tree.column('1', anchor='w', stretch=0, minwidth=50)
tree.column('2', anchor='w', stretch=0, minwidth=50)
tree.column('3', anchor='w', stretch=0, minwidth=50, width=120)
tree.column('4', anchor='e', stretch=0, minwidth=50)
tree.heading('1', text='Name', anchor='w')
tree.heading('2', text='Date of Modification', anchor='w')
tree.heading('3', text='Type', anchor='w')
tree.heading('4', text='Size', anchor='w')

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
        tree.insert('','end',values=(entry.name, time, type, size))
    else:
        name, type = entry.name.rsplit('.', 1)
        tree.insert('','end',values=(entry.name, time, '.' + type + ' File', size))

paned.add(frame1)
paned.add(frame2)

paned.paneconfigure(frame1, minsize=50)
paned.paneconfigure(frame2, minsize=50)

paned1 = tk.PanedWindow(root)
paned1.grid(row=0, column=1, sticky='nsew', pady=10, columnspan=4)

frame3 = tk.Frame(paned1)
frame4 = tk.Frame(paned1)

backarrow = tk.Button(root, image=arrow)
backarrow.grid(row=0, column=0, sticky='nsw', padx=(10,5), pady=10)

frontarrow = tk.Button(root, image=fliparrow)
frontarrow.grid(row=0, column=0, padx=(30,0), sticky='nsw', pady=10)

toparrow = tk.Button(root, image=uparrow)
toparrow.grid(row=0, column=0, padx=(55,5), sticky='nsw', pady=10)

input1 = tk.Entry(frame3, width=100)
input1.pack(side='left', fill='both', expand=True, padx=5)

input2 = tk.Entry(frame4)
input2.pack(side='right', fill='both',expand=True, padx=5)

backarrow.configure(relief='flat')
frontarrow.configure(relief='flat')
toparrow.configure(relief='flat')

paned1.add(frame3)
paned1.add(frame4)

paned1.paneconfigure(frame3, minsize=200)
paned1.paneconfigure(frame4, minsize=200)

root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()