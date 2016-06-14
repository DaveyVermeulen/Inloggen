import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import pymysql
import time

#while True:
db = pymysql.connect(host="localhost", port=3141, user="python", passwd="admin", db="inklokken")
cur = db.cursor()

class MultiColumnListbox(object):

    def __init__(self):
        self.root = None
        self.hide = 1
        self.show = 100
        self.tree = None
        self._setup_widgets()
        self._build_tree()
        
    def close(self):
        self.root.destroy()
        return

    def _setup_widgets(self):
        s = """
        Onderstaande lijst toont wie er is ingelogd, staat je naam er niet bij dan ben je niet ingelogd en moet je het opnieuw proberen. Om in te klokken moet je je schoolpas 1,5 seconden voor de scanner houden.
        """
        msg = ttk.Label(wraplength="16i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        self.tree = ttk.Treeview(columns=display_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        self.root.after(self.show*10, self.loop)
        
    def _build_tree(self):
        for col in display_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in display_list:
            self.tree.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(display_header[ix],width=None)<col_w:
                    self.tree.column(display_header[ix], width=col_w)

    def sortby(tree, col, descending):
        data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        tree.heading(col, command=lambda col=col: sortby(tree, col, \
            int(not descending)))
    
    def loop(self):
        if self.root:
            self.root.destroy()
        time.sleep(self.hide*60)
        self.(_setup_widgets)
        self.(_build_tree)
        self.(sortby)
        self.root.mainloop()
        return

root = tk.Tk()
root.title("THE KRIP")
info = []
display_header = ['Naam', 'Leerlingnummer']
display_list = info
listbox = MultiColumnListbox()


MultiColumnListbox().loop()
