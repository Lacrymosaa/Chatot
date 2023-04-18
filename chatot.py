import requests
import tkinter as tk
from tkinter import ttk
import webbrowser

def search_tracks(keyword):
    response = requests.get(f"https://api.deezer.com/search?q={keyword}")
    tracks = response.json()["data"]
    
    track_list = []
    for track in tracks:
        track_info = {
            'name': track['title'],
            'artist': track['artist']['name'],
            'url': track['link']
        }
        track_list.append(track_info)
    
    return track_list


class MusicSearcher(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Chatot")
        self.master.iconbitmap("chatot.ico")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.key_label = tk.Label(self, text="Keyword:")
        self.key_label.grid(row=0, column=0)
        self.key_entry = tk.Entry(self)
        self.key_entry.grid(row=0, column=1)
        self.search_button = tk.Button(self, text="Search", command=self.search)
        self.search_button.grid(row=0, column=2)

        self.track_table = ttk.Treeview(self, height=10)
        self.track_table["columns"] = ('name', 'artist', 'url')
        self.track_table.column("#0", width=0)  # Define largura 0 e sem stretch para a coluna de "id"
        self.track_table.heading('name', text='Name')
        self.track_table.heading('artist', text='Artist')
        self.track_table.heading('url', text='URL')
        self.track_table.column('name', width=200)
        self.track_table.column('artist', width=200)
        self.track_table.column('url', width=300)
        # Cria uma barra de rolagem e vincula-a à tabela
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.track_table.yview)
        self.track_table.configure(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=3, sticky="ns")
        self.track_table.grid(row=1, column=0, columnspan=3)


        # Bind de evento para abrir a URL correspondente no navegador ao clicar na coluna 'url'
        self.track_table.bind("<Button-1>", self.on_item_click)  

    def on_item_click(self, event):
            item_id = self.track_table.identify_row(event.y)
            if item_id:
                url = self.track_table.item(item_id, 'values')[2]
                if url:
                    webbrowser.open(url)

    def search(self):
        keyword = self.key_entry.get()
        track_list = search_tracks(keyword)

        self.track_table.delete(*self.track_table.get_children())
        for track in track_list:
            self.track_table.insert('', 'end', values=(track['name'], track['artist'], track['url']))
        self.track_table.yview_moveto(1.0)

root = tk.Tk()
app = MusicSearcher(master=root)
app.mainloop()
