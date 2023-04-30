import tkinter as tk
import tkinter.ttk as ttk
import tkinter.dnd as dnd

class DragDropDemo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create two treeviews
        self.treeview1 = ttk.Treeview(self, columns=("name", "size"))
        self.treeview2 = ttk.Treeview(self, columns=("name", "size"))
        
        # Add items to treeview1
        self.treeview1.insert("", tk.END, text="Item 1", values=("File 1", "10 KB"))
        self.treeview1.insert("", tk.END, text="Item 2", values=("File 2", "20 KB"))
        self.treeview1.insert("", tk.END, text="Item 3", values=("File 3", "30 KB"))
        
        # Bind the <<TreeviewBeginDrag>> event to treeview1
        self.treeview1.bind("<<TreeviewBeginDrag>>", self.on_treeview1_drag_begin)
        
        # Pack the treeviews
        self.treeview1.pack(side=tk.LEFT, padx=10, pady=10)
        self.treeview2.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Define a drag and drop protocol
        dnd.make_draggable(self.treeview1, [("*", "copy")])
        dnd.make_drop_target(self.treeview2, [("text/plain", "copy")])
        
    def on_treeview1_drag_begin(self, event):
        item_id = self.treeview1.selection()[0]
        item_text = self.treeview1.item(item_id)["text"]
        item_values = self.treeview1.item(item_id)["values"]
        item_data = f"{item_text}, {item_values[0]}, {item_values[1]}"
        event.widget.selection_set(item_id)
        event.widget.focus_set()
        event.widget._drag_data = item_data
        
root = tk.Tk()
app = DragDropDemo(root)
app.pack()
root.mainloop()
